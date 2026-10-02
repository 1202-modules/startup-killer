import hashlib
import json
import random
import unicodedata
import uuid
from functools import lru_cache
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db.models import (
    BrowserInstallation,
    FinalStatus,
    GameRound,
    GameSession,
    MonthlyLedger,
    RoundStatus,
    SessionStatus,
    StartupTemplate,
    StartupTemplateVersion,
)
from backend.app.db.session import get_db
from backend.app.api.deps import (
    generate_csrf_token,
    get_current_installation,
    get_optional_installation,
    get_or_create_installation,
    get_session_with_ownership,
    require_csrf,
    require_idempotency_key,
)
from backend.app.api.schemas import (
    AttackChoicePublic,
    AttackChoiceRequest,
    BootstrapFeatures,
    BootstrapGameRules,
    BootstrapResponse,
    ContinueRequest,
    ContinueResponse,
    CreateSessionRequest,
    CreateSessionResponse,
    GameResultResponse,
    LeaderboardEntry,
    LeaderboardResponse,
    ResultFinalMetrics,
    ResultRoundSummary,
    ResultScoreBreakdown,
    ResultStartupPublic,
    RoundDefensePublic,
    RoundDeltasPublic,
    RoundEventPublic,
    RoundResultResponse,
    RoundSummaryPublic,
    SessionDetailResponse,
    SessionMeResponse,
    SessionStateAfterPublic,
    SessionStatePublic,
    StartupPublicProfile,
)
from backend.app.db.seed import find_default_startups_json_path
from backend.app.engine.attack_choices import (
    AttackChoice,
    AttackCatalog,
    choices_for,
    load_attack_catalog,
    to_validated_attack,
    validate_attack_catalog,
)
from backend.app.engine.calculator import simulate_round
from backend.app.engine.loader import build_startup_template_from_version, load_startups
from backend.app.engine.types import (
    ActiveDefenseModifier,
    ActiveEffect,
    AttackType,
    DefenseType,
    Duration,
    GameState,
)

router = APIRouter(prefix="/api/v1")
ROOT = Path(__file__).resolve().parents[3]


def _active_session(db: Session, installation_id: uuid.UUID) -> Optional[GameSession]:
    return db.scalar(
        select(GameSession)
        .where(
            GameSession.browser_installation_id == installation_id,
            GameSession.status != SessionStatus.completed,
        )
        .order_by(GameSession.created_at.desc())
        .limit(1)
    )


@lru_cache(maxsize=1)
def attack_catalog() -> AttackCatalog:
    catalog = load_attack_catalog(ROOT / "data" / "attack_choices.json")
    validate_attack_catalog(catalog, load_startups(find_default_startups_json_path()))
    return catalog


def choice_snapshot(choice: AttackChoice) -> dict:
    return {
        "id": choice.id,
        "startup_slug": choice.startup_slug,
        "round_number": choice.round_number,
        "title": choice.title,
        "short_description": choice.short_description,
        "result_headline": choice.result_headline,
        "attack_type": choice.attack_type,
        "severity": choice.severity,
        "scale": choice.scale,
        "feasibility": choice.feasibility,
        "target_stream_ids": list(choice.target_stream_ids),
        "weakness_id": choice.weakness_id,
        "weakness_match": choice.weakness_match,
        "evidence_fact_ids": list(choice.evidence_fact_ids),
        "duration": choice.duration,
        "stack_group": choice.stack_group,
        "scene_type": choice.scene_type,
        "narrative": dict(choice.narrative),
        "v2_effect": dict(choice.v2_effect) if choice.v2_effect else None,
    }


def public_choice(snapshot: dict, flags: list[str] | None = None) -> AttackChoicePublic:
    combo = (snapshot.get("v2_effect") or {}).get("combo") or {}
    return AttackChoicePublic(
        id=snapshot["id"], round_number=snapshot["round_number"],
        title=snapshot["title"],
        short_description=snapshot["short_description"],
        attack_narrative=snapshot["narrative"]["attack"],
        combo_available=bool(combo and set(combo.get("requires_all", [])).issubset(flags or [])),
    )


def session_choices(session: GameSession, round_number: int) -> list[AttackChoicePublic]:
    flags = session.state.get("v2_data", {}).get("flags", [])
    return [public_choice(choice, flags) for choice in session.attack_choices_snapshot
            if choice["round_number"] == round_number]


def current_round_id(session: GameSession) -> uuid.UUID | None:
    if session.status != SessionStatus.result_pending:
        return None
    latest = max((r for r in session.rounds if r.status == RoundStatus.resolved),
                 key=lambda r: r.round_number, default=None)
    return latest.id if latest else None


def serialize_effect(effect: ActiveEffect) -> dict:
    return {
        "stack_group": effect.stack_group, "target_stream_id": effect.target_stream_id,
        "magnitude_bps": effect.magnitude_bps, "duration_type": effect.duration_type.value,
        "months_remaining": effect.months_remaining, "decay_bps": effect.decay_bps,
        "source_round": effect.source_round, "origin_attack_type": effect.origin_attack_type.value,
    }


def serialize_defense_modifier(modifier: ActiveDefenseModifier) -> dict:
    return {
        "defense_type": modifier.defense_type.value, "activated_round": modifier.activated_round,
        "activated_month": modifier.activated_month, "target_stream_id": modifier.target_stream_id,
    }


def build_startup_public_profile(
    template_snapshot: dict,
) -> StartupPublicProfile:
    """Builds a sanitized public profile for a startup."""
    pub = template_snapshot.get("public_profile", {})
    facts_raw = pub.get("facts", [])
    public_facts = [
        f["text"] if isinstance(f, dict) and "text" in f else str(f)
        for f in facts_raw
    ]
    asset_key = template_snapshot.get("asset_key", template_snapshot.get("slug", ""))
    return StartupPublicProfile(
        id=template_snapshot.get("slug", ""),
        name=template_snapshot.get("name", ""),
        tagline=pub.get("tagline", ""),
        description=pub.get("description", ""),
        public_facts=public_facts,
        hero_asset=f"/assets/startups/{asset_key}-hero.webp",
    )


def build_session_state_public(state: dict) -> SessionStatePublic:
    """Builds a sanitized public view of session economic state."""
    return SessionStatePublic(
        cash_kopeks=state.get("cash_kopeks", 0),
        monthly_revenue_kopeks=state.get("monthly_revenue_kopeks", 0),
        monthly_fixed_cost_kopeks=state.get("monthly_fixed_cost_kopeks", 0),
        variable_cost_bps=state.get("variable_cost_bps", 0),
        reputation=state.get("reputation", 0),
        active_effects_public=state.get("active_effects_public", []),
    )


# -----------------------------------------------------------------------------
# 1. Health Endpoints
# -----------------------------------------------------------------------------
@router.get("/health/live", tags=["health"])
def health_live() -> dict:
    return {"status": "ok"}


# -----------------------------------------------------------------------------
# 2. Bootstrap & Recovery
# -----------------------------------------------------------------------------
@router.get("/bootstrap", response_model=BootstrapResponse, tags=["session"])
def bootstrap(
    installation: BrowserInstallation = Depends(get_or_create_installation),
    db: Session = Depends(get_db),
) -> BootstrapResponse:
    csrf_token = generate_csrf_token(installation.id)
    existing_session = _active_session(db, installation.id)
    return BootstrapResponse(
        csrf_token=csrf_token,
        existing_session_id=existing_session.id if existing_session else None,
        game_rules=BootstrapGameRules(),
        features=BootstrapFeatures(),
    )


@router.get("/me/session", response_model=SessionMeResponse, tags=["session"])
def get_me_session(
    installation: Optional[BrowserInstallation] = Depends(get_optional_installation),
    db: Session = Depends(get_db),
) -> SessionMeResponse:
    if not installation:
        return SessionMeResponse(session_id=None, status=None)

    session = db.scalar(
        select(GameSession)
        .where(GameSession.browser_installation_id == installation.id)
        .order_by(GameSession.created_at.desc())
        .limit(1)
    )
    if not session:
        return SessionMeResponse(session_id=None, status=None)

    return SessionMeResponse(
        session_id=session.id,
        status=session.status.value,
    )


# -----------------------------------------------------------------------------
# 3. Sessions
# -----------------------------------------------------------------------------
@router.post("/sessions", response_model=CreateSessionResponse, tags=["session"])
def create_session(
    payload: CreateSessionRequest,
    response: Response,
    installation: BrowserInstallation = Depends(get_current_installation),
    _: None = Depends(require_csrf),
    idempotency_key: uuid.UUID = Depends(require_idempotency_key),
    db: Session = Depends(get_db),
) -> CreateSessionResponse:
    # 1. Validate and normalize nickname (2..24 characters)
    nickname = unicodedata.normalize("NFKC", payload.nickname).strip()
    if len(nickname) < 2 or len(nickname) > 24:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "INVALID_NICKNAME",
                "message": "Никнейм должен содержать от 2 до 24 видимых символов",
                "retryable": False,
            },
        )
    if any(unicodedata.category(c)[0] == "C" for c in nickname):
        raise HTTPException(
            status_code=422,
            detail={
                "code": "INVALID_NICKNAME",
                "message": "Никнейм не должен содержать управляющих символов",
                "retryable": False,
            },
        )

    # Serialize new-session attempts per installation and reuse any unfinished game.
    db.scalar(
        select(BrowserInstallation)
        .where(BrowserInstallation.id == installation.id)
        .with_for_update()
    )
    existing_session = _active_session(db, installation.id)
    if existing_session:
        response.status_code = 200
        startup_pub = build_startup_public_profile(existing_session.template_snapshot)
        state_pub = build_session_state_public(existing_session.state)
        return CreateSessionResponse(
            session_id=existing_session.id,
            status=existing_session.status.value,
            next_round=existing_session.next_round,
            elapsed_months=existing_session.elapsed_months,
            startup=startup_pub,
            state=state_pub,
            available_choices=session_choices(existing_session, existing_session.next_round)
            if existing_session.status == SessionStatus.ready else [],
            current_round_id=current_round_id(existing_session),
            can_attack=existing_session.status == SessionStatus.ready,
            can_continue=existing_session.status == SessionStatus.result_pending,
            completed=existing_session.status == SessionStatus.completed,
            ranking_eligible=existing_session.ranking_eligible,
            reused_existing_session=True,
        )

    # 3. Create a new session with a random available startup template
    templates = db.scalars(
        select(StartupTemplate).where(StartupTemplate.is_enabled == True)
    ).all()
    if not templates:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "NO_STARTUPS_AVAILABLE",
                "message": "Нет доступных шаблонов стартапов для начала партии",
                "retryable": True,
            },
        )

    selected_template = random.choice(templates)
    template_version = db.scalar(
        select(StartupTemplateVersion).where(
            StartupTemplateVersion.template_id == selected_template.id,
            StartupTemplateVersion.version == selected_template.current_version,
        )
    )
    if not template_version:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "STARTUP_VERSION_NOT_FOUND",
                "message": "Версия шаблона стартапа не найдена",
                "retryable": False,
            },
        )

    # 4. Prepare initial state & snapshot
    finance = template_version.finance_config
    initial_cash = finance.get("initial_cash_kopeks", 0)
    initial_fixed = finance.get("initial_fixed_cost_kopeks", 0)
    initial_reputation = finance.get("initial_reputation", 75)
    streams = finance.get("revenue_streams", [])
    total_rev = sum(s.get("initial_monthly_revenue_kopeks", 0) for s in streams)
    total_weight = sum(s.get("weight_bps", 0) for s in streams)
    weighted_var_cost = (
        sum(s.get("variable_cost_bps", 0) * s.get("weight_bps", 0) for s in streams) // total_weight
        if total_weight > 0
        else 0
    )

    state = {
        "cash_kopeks": initial_cash,
        "monthly_revenue_kopeks": total_rev,
        "monthly_fixed_cost_kopeks": initial_fixed,
        "variable_cost_bps": weighted_var_cost,
        "reputation": initial_reputation,
        "active_effects": [],
        "used_defenses": [],
        "active_defense_modifiers": [],
        "active_effects_public": [],
        "v2_data": {},
    }

    template_snapshot = {
        "slug": selected_template.slug,
        "name": template_version.name,
        "industry": template_version.industry,
        "asset_key": template_version.asset_key,
        "public_profile": template_version.public_profile,
        "finance_config": template_version.finance_config,
    }
    selected_choices = [
        choice_snapshot(choice)
        for round_number in range(1, 4)
        for choice in choices_for(attack_catalog(), selected_template.slug, round_number)
    ]

    session = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=selected_template.id,
        startup_version=selected_template.current_version,
        nickname=nickname,
        status=SessionStatus.ready,
        next_round=1,
        elapsed_months=0,
        template_snapshot=template_snapshot,
        state=state,
        attack_catalog_version=attack_catalog().catalog_version,
        attack_choices_snapshot=selected_choices,
        engine_version=template_version.engine_version,
        version=1,
        ranking_eligible=True,
    )
    try:
        db.add(session)
        db.commit()
        db.refresh(session)
    except IntegrityError:
        db.rollback()
        # Handle concurrent creation for the same browser installation
        existing_session = _active_session(db, installation.id)
        if existing_session:
            response.status_code = 200
            startup_pub = build_startup_public_profile(existing_session.template_snapshot)
            state_pub = build_session_state_public(existing_session.state)
            return CreateSessionResponse(
                session_id=existing_session.id,
                status=existing_session.status.value,
                next_round=existing_session.next_round,
                elapsed_months=existing_session.elapsed_months,
                startup=startup_pub,
                state=state_pub,
                available_choices=session_choices(existing_session, existing_session.next_round)
                if existing_session.status == SessionStatus.ready else [],
                current_round_id=current_round_id(existing_session),
                can_attack=existing_session.status == SessionStatus.ready,
                can_continue=existing_session.status == SessionStatus.result_pending,
                completed=existing_session.status == SessionStatus.completed,
                ranking_eligible=existing_session.ranking_eligible,
                reused_existing_session=True,
            )
        raise

    response.status_code = 201
    startup_pub = build_startup_public_profile(template_snapshot)
    state_pub = build_session_state_public(state)
    return CreateSessionResponse(
        session_id=session.id,
        status=session.status.value,
        next_round=session.next_round,
        elapsed_months=session.elapsed_months,
        startup=startup_pub,
        state=state_pub,
        available_choices=session_choices(session, session.next_round),
        can_attack=True,
        can_continue=False,
        completed=False,
        ranking_eligible=session.ranking_eligible,
        reused_existing_session=False,
    )


@router.get("/sessions/{session_id}", response_model=SessionDetailResponse, tags=["session"])
def get_session_detail(
    response: Response,
    session: GameSession = Depends(get_session_with_ownership),
) -> SessionDetailResponse:
    response.headers["Cache-Control"] = "no-store"
    startup_pub = build_startup_public_profile(session.template_snapshot)
    state_pub = build_session_state_public(session.state)

    resolved_rounds = [
        RoundSummaryPublic(
            round_number=r.round_number,
            event_title=r.event_title,
            defense_summary=r.defense_summary,
            new_circumstance=r.new_circumstance,
        )
        for r in session.rounds
        if r.status == RoundStatus.resolved
    ]

    can_attack = session.status == SessionStatus.ready and session.next_round <= 3
    can_continue = session.status == SessionStatus.result_pending
    completed = session.status == SessionStatus.completed

    return SessionDetailResponse(
        session_id=session.id,
        status=session.status.value,
        next_round=session.next_round,
        elapsed_months=session.elapsed_months,
        startup=startup_pub,
        state=state_pub,
        rounds=resolved_rounds,
        current_round_id=current_round_id(session),
        available_choices=session_choices(session, session.next_round)
        if session.status == SessionStatus.ready else [],
        can_attack=can_attack,
        can_continue=can_continue,
        completed=completed,
        ranking_eligible=session.ranking_eligible,
    )


# -----------------------------------------------------------------------------
# 4. Deterministic choices
# -----------------------------------------------------------------------------
def _round_result(round_obj: GameRound) -> RoundResultResponse:
    outcome = round_obj.outcome or {}
    narrative = (round_obj.choice_snapshot or {}).get("narrative", {})
    defense = dict(outcome["defense"])
    defense["company_response"] = narrative.get("company_response")
    return RoundResultResponse(
        status="resolved", round_id=round_obj.id, round_number=round_obj.round_number,
        selected_choice=public_choice(round_obj.choice_snapshot) if round_obj.choice_snapshot else None,
        months_simulated=outcome.get("months_simulated", []),
        event=RoundEventPublic(**outcome["event"]),
        defense=RoundDefensePublic(**defense),
        deltas=RoundDeltasPublic(**outcome["deltas"]),
        state_after=SessionStateAfterPublic(**outcome["state_after"]),
        new_circumstance=outcome.get("new_circumstance"),
        game_completed=outcome["game_completed"], next_action=outcome["next_action"],
        impact=outcome.get("impact"),
    )


@router.post("/sessions/{session_id}/choices", response_model=RoundResultResponse, tags=["attacks"])
def submit_choice(
    session_id: uuid.UUID,
    payload: AttackChoiceRequest,
    session: GameSession = Depends(get_session_with_ownership),
    _: None = Depends(require_csrf),
    idempotency_key: uuid.UUID = Depends(require_idempotency_key),
    db: Session = Depends(get_db),
) -> RoundResultResponse:
    statement = select(GameSession).where(GameSession.id == session.id)
    if db.get_bind().dialect.name == "postgresql":
        statement = statement.with_for_update()
    session = db.scalar(statement)
    canonical = json.dumps({"choice_id": payload.choice_id}, sort_keys=True)
    request_sha256 = hashlib.sha256(canonical.encode()).hexdigest()
    existing = db.scalar(select(GameRound).where(
        GameRound.session_id == session.id, GameRound.idempotency_key == idempotency_key
    ))
    if existing:
        if existing.request_sha256 != request_sha256:
            raise HTTPException(409, detail={"code": "IDEMPOTENCY_CONFLICT", "message": "Idempotency-Key уже использован с другим выбором", "retryable": False})
        return _round_result(existing)
    if session.status != SessionStatus.ready:
        raise HTTPException(409, detail={"code": "INVALID_SESSION_STATE", "message": "Сессия не готова к выбору", "retryable": False})
    choice_data = next((item for item in session.attack_choices_snapshot
                        if item["id"] == payload.choice_id
                        and item["round_number"] == session.next_round), None)
    if choice_data is None:
        raise HTTPException(404, detail={"code": "CHOICE_NOT_FOUND", "message": "Вариант не найден для текущего раунда", "retryable": False})
    choice = AttackChoice(**{**choice_data,
        "target_stream_ids": tuple(choice_data["target_stream_ids"]),
        "evidence_fact_ids": tuple(choice_data["evidence_fact_ids"]),
    })
    template_version = db.scalar(select(StartupTemplateVersion).where(
        StartupTemplateVersion.template_id == session.startup_template_id,
        StartupTemplateVersion.version == session.startup_version,
    ))
    startup = build_startup_template_from_version(template_version, session.template_snapshot["slug"])
    old = session.state
    state = GameState(
        session_id=str(session.id), template_slug=startup.slug, round_number=session.next_round,
        elapsed_months=session.elapsed_months, cash_kopeks=old["cash_kopeks"],
        fixed_cost_kopeks=old["monthly_fixed_cost_kopeks"], reputation=old["reputation"],
        active_effects=[ActiveEffect(
            stack_group=e["stack_group"], target_stream_id=e["target_stream_id"],
            magnitude_bps=e["magnitude_bps"], duration_type=Duration(e["duration_type"]),
            months_remaining=e["months_remaining"], decay_bps=e["decay_bps"],
            source_round=e["source_round"], origin_attack_type=AttackType(e["origin_attack_type"]),
        ) for e in old.get("active_effects", [])],
        used_defenses=[DefenseType(d) for d in old.get("used_defenses", [])],
        active_defense_modifiers=[ActiveDefenseModifier(
            defense_type=DefenseType(m["defense_type"]), activated_round=m["activated_round"],
            activated_month=m["activated_month"], target_stream_id=m.get("target_stream_id"),
        ) for m in old.get("active_defense_modifiers", [])],
        v2_data=old.get("v2_data", {}),
    )
    outcome = simulate_round(state, startup, to_validated_attack(choice, startup))
    game_round = GameRound(
        session_id=session.id, round_number=session.next_round, idempotency_key=idempotency_key,
        request_sha256=request_sha256, selected_choice_id=choice.id,
        choice_snapshot=choice_data, status=RoundStatus.resolved,
    )
    db.add(game_round)
    current_cash = state.cash_kopeks
    for row in outcome.monthly_ledger:
        db.add(MonthlyLedger(
            session_id=session.id, round=game_round, month_no=row.month,
            opening_cash_kopeks=current_cash,
            revenue_by_stream={stream.id: stream.revenue_kopeks for stream in row.streams},
            variable_cost_kopeks=row.variable_cost_kopeks, fixed_cost_kopeks=row.fixed_cost_kopeks,
            incident_cost_kopeks=row.incident_cost_kopeks, defense_cost_kopeks=row.defense_cost_kopeks,
            closing_cash_kopeks=row.closing_cash_kopeks,
            unpaid_obligations_kopeks=row.unpaid_obligations_kopeks,
            reputation_after=outcome.state_after.reputation,
            applied_effects=[serialize_effect(e) for e in outcome.state_after.active_effects],
        ))
        current_cash = row.closing_cash_kopeks
    final_row = outcome.monthly_ledger[-1]
    new_state = outcome.state_after
    var_bps = final_row.variable_cost_kopeks * 10000 // final_row.revenue_kopeks if final_row.revenue_kopeks else old.get("variable_cost_bps", 0)
    session.state = {
        "cash_kopeks": new_state.cash_kopeks,
        "monthly_revenue_kopeks": final_row.revenue_kopeks,
        "monthly_fixed_cost_kopeks": new_state.fixed_cost_kopeks,
        "variable_cost_bps": var_bps, "reputation": new_state.reputation,
        "active_effects": [serialize_effect(e) for e in new_state.active_effects],
        "used_defenses": [d.value for d in new_state.used_defenses],
        "active_defense_modifiers": [serialize_defense_modifier(m) for m in new_state.active_defense_modifiers],
        "active_effects_public": [f"{e.origin_attack_type.value} (-{e.magnitude_bps // 100}%)" for e in new_state.active_effects],
        "v2_data": new_state.v2_data,
    }
    session.elapsed_months += len(outcome.monthly_ledger)
    session.version += 1
    completed = new_state.is_bankrupt or session.next_round >= 3
    if new_state.is_bankrupt or completed:
        session.status = SessionStatus.completed
        session.final_status = FinalStatus(new_state.score_breakdown.final_status.value if new_state.score_breakdown else outcome.final_status.value)
        session.final_score = outcome.score_breakdown.score if outcome.score_breakdown else 0
        session.bankruptcy_month = new_state.bankruptcy_month
        session.completed_at = datetime.now(timezone.utc)
    else:
        session.status = SessionStatus.result_pending
    outcome_data = {
        "event": {"title": choice.result_headline, "narrative": choice.narrative["result"], "scene_type": choice.scene_type},
        "defense": {"type": outcome.defense.defense_type.value, "summary": outcome.defense.detail,
                    "cost_kopeks": outcome.defense.cost_kopeks, "reason": outcome.defense.reason},
        "deltas": {"cash_kopeks": outcome.cash_delta_kopeks, "monthly_revenue_kopeks": outcome.revenue_delta_kopeks, "reputation": outcome.reputation_delta},
        "state_after": {"cash_kopeks": new_state.cash_kopeks, "monthly_revenue_kopeks": final_row.revenue_kopeks, "reputation": new_state.reputation},
        "months_simulated": [row.month for row in outcome.monthly_ledger],
        "new_circumstance": None, "game_completed": completed,
        "next_action": "result" if completed else "continue",
        "impact": outcome.details or None,
    }
    game_round.outcome = outcome_data
    game_round.event_title = choice.result_headline
    game_round.event_narrative = choice.narrative["result"]
    game_round.defense_summary = outcome.defense.detail
    game_round.new_circumstance = None
    game_round.resolved_at = datetime.now(timezone.utc)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.scalar(select(GameRound).where(
            GameRound.session_id == session.id, GameRound.idempotency_key == idempotency_key
        ))
        if existing and existing.request_sha256 == request_sha256:
            return _round_result(existing)
        raise HTTPException(409, detail={"code": "ROUND_ALREADY_SUBMITTED", "message": "Раунд уже обработан", "retryable": False})
    db.refresh(game_round)
    return _round_result(game_round)


@router.get("/rounds/{round_id}", response_model=RoundResultResponse, tags=["attacks"])
def get_round_result(
    round_id: uuid.UUID,
    response: Response,
    installation: BrowserInstallation = Depends(get_current_installation),
    db: Session = Depends(get_db),
) -> RoundResultResponse:
    round_obj = db.scalar(select(GameRound).where(GameRound.id == round_id))
    if not round_obj:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "ROUND_NOT_FOUND",
                "message": "Раунд не найден",
                "retryable": False,
            },
        )

    if round_obj.session.browser_installation_id != installation.id:
        raise HTTPException(
            status_code=403,
            detail={
                "code": "SESSION_FORBIDDEN",
                "message": "Доступ к раунду чужой сессии запрещён",
                "retryable": False,
            },
        )

    return _round_result(round_obj)


# -----------------------------------------------------------------------------
# 5. Continue & Finalization
# -----------------------------------------------------------------------------
@router.post("/sessions/{session_id}/continue", response_model=ContinueResponse, tags=["session"])
def continue_session(
    payload: ContinueRequest,
    session: GameSession = Depends(get_session_with_ownership),
    _: None = Depends(require_csrf),
    idempotency_key: uuid.UUID = Depends(require_idempotency_key),
    db: Session = Depends(get_db),
) -> ContinueResponse:
    # 1. If session is already completed
    if session.status == SessionStatus.completed:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "SESSION_ALREADY_COMPLETED",
                "message": "Партия уже завершена",
                "retryable": False,
            },
        )

    # 2. If session is already in ready status (idempotency check)
    resolved_round = db.scalar(
        select(GameRound).where(
            GameRound.id == payload.resolved_round_id,
            GameRound.session_id == session.id,
        )
    )
    if not resolved_round:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "ROUND_NOT_FOUND",
                "message": "Указанный раунд не найден",
                "retryable": False,
            },
        )
    if resolved_round.status != RoundStatus.resolved:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "ROUND_NOT_RESOLVED",
                "message": "Раунд ещё не завершён обработкой",
                "retryable": False,
            },
        )

    if session.status == SessionStatus.ready and session.next_round > resolved_round.round_number:
        # Already continued idempotently
        return ContinueResponse(
            session_id=session.id,
            status=session.status.value,
            next_round=session.next_round,
        )

    # 3. Session must be in result_pending
    if session.status != SessionStatus.result_pending:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "INVALID_SESSION_STATE",
                "message": f"Продолжение возможно только из статуса result_pending. Текущий статус: {session.status.value}",
                "retryable": False,
            },
        )

    # 4. Check that round is < 3 (continuation after round 3 is not available)
    if resolved_round.round_number >= 3 or session.next_round >= 3:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "CONTINUE_NOT_AVAILABLE",
                "message": "Продолжение после 3-го раунда недоступно. Партия завершена.",
                "retryable": False,
            },
        )

    # Advance next_round without changing finances
    session.next_round += 1
    session.status = SessionStatus.ready

    db.commit()
    db.refresh(session)

    return ContinueResponse(
        session_id=session.id,
        status=session.status.value,
        next_round=session.next_round,
    )


@router.get("/sessions/{session_id}/result", response_model=GameResultResponse, tags=["result"])
def get_session_result(
    session: GameSession = Depends(get_session_with_ownership),
    db: Session = Depends(get_db),
) -> GameResultResponse:
    if session.status != SessionStatus.completed:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "RESULT_NOT_READY",
                "message": "Результаты партии доступны только после её завершения",
                "retryable": False,
            },
        )

    score_val = session.final_score if session.final_score is not None else 0
    final_status_val = (
        session.final_status.value if session.final_status else FinalStatus.survived.value
    )

    # Compute rank on the fly among completed, ranking_eligible sessions
    if session.ranking_eligible:
        higher_count = db.scalar(
            select(func.count(GameSession.id)).where(
                GameSession.status == SessionStatus.completed,
                GameSession.ranking_eligible == True,
                GameSession.final_score > score_val,
            )
        ) or 0
        rank = higher_count + 1

        total_ranked = db.scalar(
            select(func.count(GameSession.id)).where(
                GameSession.status == SessionStatus.completed,
                GameSession.ranking_eligible == True,
            )
        ) or 1
    else:
        rank = None
        total_ranked = None

    cash_kopeks = session.state.get("cash_kopeks", 0)
    rev = session.state.get("monthly_revenue_kopeks", 0)
    fixed = session.state.get("monthly_fixed_cost_kopeks", 0)
    var_bps = session.state.get("variable_cost_bps", 0)
    burn = fixed + (rev * var_bps // 10000) - rev
    runway = round(cash_kopeks / burn, 1) if burn > 0 else None

    # Score breakdown details
    score_breakdown = ResultScoreBreakdown(
        damage=min(700, score_val),
        solvency=min(200, max(0, score_val - 700)),
        bankruptcy_bonus=100 if final_status_val == FinalStatus.bankrupt.value else 0,
    )

    startup_name = session.template_snapshot.get("name", "Стартап")
    startup_id = session.template_snapshot.get("slug", "")

    summary_map = {
        FinalStatus.survived.value: "Компания преодолела давление и сохранила финансовую устойчивость.",
        FinalStatus.deep_crisis.value: "Компания пережила кризис, но понесла тяжёлые финансовые потери.",
        FinalStatus.near_bankruptcy.value: "Компания выжила, но находится на грани банкротства.",
        FinalStatus.bankrupt.value: "Стартап исчерпал финансовые резервы и обанкротился.",
    }
    summary = summary_map.get(final_status_val, "Партия завершена.")

    rounds_summary = [
        ResultRoundSummary(
            round_number=r.round_number,
            event_title=r.event_title or f"Раунд {r.round_number}",
        )
        for r in session.rounds
        if r.status == RoundStatus.resolved
    ]

    return GameResultResponse(
        session_id=session.id,
        startup_name=startup_name,
        nickname=session.nickname,
        final_status=final_status_val,
        score=score_val,
        final_score=score_val,
        rank=rank,
        total_ranked=total_ranked,
        total_cash_kopeks=cash_kopeks,
        baseline_cash_m9_kopeks=session.template_snapshot.get("finance_config", {}).get("initial_cash_kopeks", 0),
        startup=ResultStartupPublic(id=startup_id, name=startup_name),
        final_metrics=ResultFinalMetrics(cash_kopeks=cash_kopeks, runway_months=runway),
        score_breakdown=score_breakdown,
        score_details=score_breakdown,
        rounds=rounds_summary,
        summary=summary,
        ranking_eligible=session.ranking_eligible,
    )


# -----------------------------------------------------------------------------
# 6. Leaderboard
# -----------------------------------------------------------------------------
@router.get("/leaderboard", response_model=LeaderboardResponse, tags=["leaderboard"])
def get_leaderboard(
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    installation: Optional[BrowserInstallation] = Depends(get_optional_installation),
    db: Session = Depends(get_db),
) -> LeaderboardResponse:
    # 1. Total count of ranked completed sessions
    total_count = db.scalar(
        select(func.count(GameSession.id)).where(
            GameSession.status == SessionStatus.completed,
            GameSession.ranking_eligible == True,
        )
    ) or 0

    if total_count == 0:
        return LeaderboardResponse(total=0, items=[], my_entry=None)

    # 2. Query with window function RANK() OVER (ORDER BY final_score DESC)
    # Order for display: final_score DESC, completed_at ASC
    rank_func = func.rank().over(order_by=GameSession.final_score.desc()).label("rank")
    stmt = (
        select(GameSession, rank_func)
        .where(
            GameSession.status == SessionStatus.completed,
            GameSession.ranking_eligible == True,
        )
        .order_by(GameSession.final_score.desc(), GameSession.completed_at.asc())
    )
    all_rows = db.execute(stmt).all()

    # 3. Find my_entry if current browser installation has a completed ranked game
    my_entry: Optional[LeaderboardEntry] = None
    items: List[LeaderboardEntry] = []

    for idx, (sess, rnk) in enumerate(all_rows):
        is_me = bool(installation and sess.browser_installation_id == installation.id)
        startup_name = sess.template_snapshot.get("name", "Стартап")
        entry = LeaderboardEntry(
            rank=int(rnk),
            nickname=sess.nickname,
            startup_name=startup_name,
            score=sess.final_score or 0,
            final_score=sess.final_score,
            final_status=sess.final_status.value if sess.final_status else "survived",
            completed_at=sess.completed_at or sess.created_at,
            is_me=is_me,
        )
        if is_me and my_entry is None:
            my_entry = entry

        # Apply limit & offset pagination
        if offset <= idx < offset + limit:
            items.append(entry)

    return LeaderboardResponse(
        total=total_count,
        items=items,
        my_entry=my_entry,
    )
