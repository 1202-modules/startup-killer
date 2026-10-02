import uuid
import hashlib
from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.session import Base, get_db
from backend.app.db.models import (
    StartupTemplate,
    StartupTemplateVersion,
    BrowserInstallation,
    GameSession,
    GameRound,
    SessionStatus,
    RoundStatus,
    FinalStatus,
)
from backend.app.db.seed import seed_startups
from backend.app.main import app


@pytest.fixture
def db_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    from sqlalchemy import event

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()
    seed_startups(session)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_engine, db_session):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

    def override_get_db():
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_live_health_endpoint(client):
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_bootstrap_sets_cookie_and_returns_payload(client):
    response = client.get("/api/v1/bootstrap")
    assert response.status_code == 200
    assert "sk_browser" in response.cookies
    cookie_value = response.cookies["sk_browser"]
    assert len(cookie_value) > 20

    data = response.json()
    assert "csrf_token" in data
    assert len(data["csrf_token"]) == 64
    assert data["existing_session_id"] is None
    assert data["game_rules"]["max_rounds"] == 3
    assert data["game_rules"]["months_per_round"] == 3
    assert data["game_rules"]["one_attempt_per_browser"] is True
    assert data["features"]["sound_default"] is False


def test_bootstrap_preserves_existing_cookie(client):
    r1 = client.get("/api/v1/bootstrap")
    cookie_1 = client.cookies.get("sk_browser")
    csrf_1 = r1.json()["csrf_token"]

    # Call bootstrap again with the same cookie
    r2 = client.get("/api/v1/bootstrap")
    cookie_2 = client.cookies.get("sk_browser")
    csrf_2 = r2.json()["csrf_token"]

    assert cookie_1 == cookie_2
    assert csrf_1 == csrf_2


def test_me_session_without_session_and_without_cookie(client):
    # Without cookie, returns null session
    r1 = client.get("/api/v1/me/session")
    assert r1.status_code == 200
    assert r1.json() == {"session_id": None, "status": None}

    # After bootstrap, still returns null session
    client.get("/api/v1/bootstrap")
    r2 = client.get("/api/v1/me/session")
    assert r2.status_code == 200
    assert r2.json() == {"session_id": None, "status": None}


def test_create_session_requires_csrf_and_idempotency(client):
    bootstrap_res = client.get("/api/v1/bootstrap")
    csrf_token = bootstrap_res.json()["csrf_token"]
    idempotency_key = str(uuid.uuid4())

    # Missing CSRF
    r_no_csrf = client.post(
        "/api/v1/sessions",
        headers={"Idempotency-Key": idempotency_key},
        json={"nickname": "TestUser"},
    )
    assert r_no_csrf.status_code == 403
    assert r_no_csrf.json()["error"]["code"] == "CSRF_INVALID"

    # Missing Idempotency-Key
    r_no_idemp = client.post(
        "/api/v1/sessions",
        headers={"X-CSRF-Token": csrf_token},
        json={"nickname": "TestUser"},
    )
    assert r_no_idemp.status_code in (400, 422)

    # Invalid nickname (< 2 characters)
    r_short = client.post(
        "/api/v1/sessions",
        headers={"X-CSRF-Token": csrf_token, "Idempotency-Key": idempotency_key},
        json={"nickname": "a"},
    )
    assert r_short.status_code == 422
    assert r_short.json()["error"]["code"] == "INVALID_NICKNAME"

    # Invalid nickname (> 24 characters)
    r_long = client.post(
        "/api/v1/sessions",
        headers={"X-CSRF-Token": csrf_token, "Idempotency-Key": idempotency_key},
        json={"nickname": "a" * 25},
    )
    assert r_long.status_code == 422
    assert r_long.json()["error"]["code"] == "INVALID_NICKNAME"


def test_create_session_success_and_reuse_idempotency(client):
    bootstrap_res = client.get("/api/v1/bootstrap")
    csrf_token = bootstrap_res.json()["csrf_token"]
    idempotency_key = str(uuid.uuid4())

    # First session creation: 201 Created
    r_create = client.post(
        "/api/v1/sessions",
        headers={"X-CSRF-Token": csrf_token, "Idempotency-Key": idempotency_key},
        json={"nickname": "  StartupKiller  "},
    )
    assert r_create.status_code == 201
    data = r_create.json()
    session_id = data["session_id"]
    assert session_id is not None
    assert data["status"] == "ready"
    assert data["next_round"] == 1
    assert data["elapsed_months"] == 0
    assert "startup" in data
    assert "id" in data["startup"]
    assert "tagline" in data["startup"]
    assert "state" in data
    assert data["state"]["cash_kopeks"] > 0
    assert data["reused_existing_session"] is None or data["reused_existing_session"] is False

    # Second session creation from same browser: returns 200 OK and reused_existing_session: True
    new_idemp = str(uuid.uuid4())
    r_reuse = client.post(
        "/api/v1/sessions",
        headers={"X-CSRF-Token": csrf_token, "Idempotency-Key": new_idemp},
        json={"nickname": "DifferentNick"},
    )
    assert r_reuse.status_code == 200
    data_reuse = r_reuse.json()
    assert data_reuse["session_id"] == session_id
    assert data_reuse["reused_existing_session"] is True

    # Check /me/session now reflects the created session
    r_me = client.get("/api/v1/me/session")
    assert r_me.status_code == 200
    assert r_me.json()["session_id"] == session_id
    assert r_me.json()["status"] == "ready"

    # Check /bootstrap now reflects existing_session_id
    r_boot2 = client.get("/api/v1/bootstrap")
    assert r_boot2.json()["existing_session_id"] == session_id


def test_get_session_details_and_ownership(client, db_engine):
    b1 = client.get("/api/v1/bootstrap")
    csrf1 = b1.json()["csrf_token"]
    r_create = client.post(
        "/api/v1/sessions",
        headers={"X-CSRF-Token": csrf1, "Idempotency-Key": str(uuid.uuid4())},
        json={"nickname": "OwnerPlayer"},
    )
    session_id = r_create.json()["session_id"]

    # Owner GET /sessions/{id} -> 200 OK
    r_get = client.get(f"/api/v1/sessions/{session_id}")
    assert r_get.status_code == 200
    detail = r_get.json()
    assert detail["session_id"] == session_id
    assert detail["status"] == "ready"
    assert detail["can_attack"] is True
    assert detail["can_continue"] is False
    assert detail["completed"] is False
    assert "private_profile" not in detail
    assert "weaknesses" not in detail["startup"]

    # Non-existent session -> 404
    r_404 = client.get(f"/api/v1/sessions/{uuid.uuid4()}")
    assert r_404.status_code == 404
    assert r_404.json()["error"]["code"] == "SESSION_NOT_FOUND"

    # Different browser installation trying to access owner's session -> 403
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

    def override_get_db():
        s = SessionLocal()
        try:
            yield s
        finally:
            s.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as another_client:
        another_client.get("/api/v1/bootstrap")
        r_forbidden = another_client.get(f"/api/v1/sessions/{session_id}")
        assert r_forbidden.status_code == 403
        assert r_forbidden.json()["error"]["code"] == "SESSION_FORBIDDEN"


def _new_game(client, nickname="ChoicePlayer"):
    bootstrap = client.get("/api/v1/bootstrap")
    csrf = bootstrap.json()["csrf_token"]
    created = client.post(
        "/api/v1/sessions",
        headers={"X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4())},
        json={"nickname": nickname},
    )
    assert created.status_code == 201
    session_id = created.json()["session_id"]
    detail = client.get(f"/api/v1/sessions/{session_id}")
    return session_id, csrf, detail.json()


def test_choice_resolves_round_synchronously_and_replays_idempotently(client):
    session_id, csrf, detail = _new_game(client)
    assert len(detail["available_choices"]) == 4
    choice = detail["available_choices"][0]
    headers = {"X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4())}
    url = f"/api/v1/sessions/{session_id}/choices"

    first = client.post(url, headers=headers, json={"choice_id": choice["id"]})
    assert first.status_code == 200
    result = first.json()
    assert result["status"] == "resolved"
    assert result["round_number"] == 1
    assert result["new_circumstance"] is None
    from backend.app.api.routes import attack_catalog
    catalog_choice = next(item for item in attack_catalog().choices if item.id == choice["id"])
    assert result["selected_choice"]["title"] == catalog_choice.title
    assert result["defense"]["company_response"] == catalog_choice.narrative["company_response"]
    assert "job_id" not in result
    assert "attack_text" not in result

    replay = client.post(url, headers=headers, json={"choice_id": choice["id"]})
    assert replay.status_code == 200
    assert replay.json() == result
    assert client.get(f"/api/v1/sessions/{session_id}").json()["status"] == "result_pending"


def test_choice_request_rejects_unknown_id_and_extra_fields(client):
    session_id, csrf, _ = _new_game(client)
    url = f"/api/v1/sessions/{session_id}/choices"
    headers = {"X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4())}
    unknown = client.post(url, headers=headers, json={"choice_id": "not-a-real-choice"})
    assert unknown.status_code == 404
    assert unknown.json()["error"]["code"] == "CHOICE_NOT_FOUND"

    extra = client.post(
        url,
        headers={"X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4())},
        json={"choice_id": "choice", "severity": "critical", "target_stream_ids": ["x"]},
    )
    assert extra.status_code == 422


def test_choice_request_rejects_reused_key_with_different_choice(client):
    session_id, csrf, detail = _new_game(client)
    choices = detail["available_choices"]
    headers = {"X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4())}
    url = f"/api/v1/sessions/{session_id}/choices"
    first = client.post(url, headers=headers, json={"choice_id": choices[0]["id"]})
    assert first.status_code == 200
    conflict = client.post(url, headers=headers, json={"choice_id": choices[1]["id"]})
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "IDEMPOTENCY_CONFLICT"



def test_choice_rejects_other_startup_or_round(client):
    from backend.app.api.routes import attack_catalog
    session_id, csrf, detail = _new_game(client, "WrongChoice")
    startup_slug = detail["startup"]["id"]
    catalog = attack_catalog()
    other_startup = next(c for c in catalog.choices if c.startup_slug != startup_slug and c.round_number == 1)
    later_round = next(c for c in catalog.choices if c.startup_slug == startup_slug and c.round_number == 2)
    url = f"/api/v1/sessions/{session_id}/choices"
    for choice_id in (other_startup.id, later_round.id):
        response = client.post(url, headers={
            "X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4()),
        }, json={"choice_id": choice_id})
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "CHOICE_NOT_FOUND"


def test_session_choice_snapshot_is_used_after_catalog_source_changes(client, db_session):
    session_id, _, detail = _new_game(client, "PinnedCatalog")
    session = db_session.get(GameSession, uuid.UUID(session_id))
    snapshots = [dict(item) for item in session.attack_choices_snapshot]
    snapshots[0]["title"] = "Pinned title"
    pinned_description = "Pinned description"
    snapshots[0]["short_description"] = pinned_description
    session.attack_choices_snapshot = snapshots
    choice_id = snapshots[0]["id"]
    db_session.commit()
    refreshed = client.get(f"/api/v1/sessions/{session_id}").json()
    choice = next(c for c in refreshed["available_choices"] if c["id"] == choice_id)
    assert choice["title"] == "Pinned title"
    assert choice["short_description"] == pinned_description


def test_same_attack_type_choices_keep_distinct_public_titles():
    from backend.app.api.routes import attack_catalog, choice_snapshot, public_choice

    catalog = attack_catalog()
    choices = [
        choice for choice in catalog.choices
        if choice.startup_slug == "cloudkitchen" and choice.round_number == 2
        and choice.attack_type == "competition"
    ]
    assert len(choices) == 3
    titles = [public_choice(choice_snapshot(choice)).title for choice in choices]
    assert len(set(titles)) == len(titles)
    assert titles == [choice.title for choice in choices]

def test_round_result_is_available_immediately_after_choice(client):
    session_id, csrf, detail = _new_game(client)
    choice = detail["available_choices"][0]
    result = client.post(
        f"/api/v1/sessions/{session_id}/choices",
        headers={"X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4())},
        json={"choice_id": choice["id"]},
    )
    assert result.status_code == 200
    round_id = result.json()["round_id"]
    resumed = client.get(f"/api/v1/rounds/{round_id}")
    assert resumed.status_code == 200
    assert resumed.json()["status"] == "resolved"
    assert resumed.json()["round_number"] == 1

def test_get_result_not_ready_and_completed(client, db_session):
    b = client.get("/api/v1/bootstrap")
    csrf = b.json()["csrf_token"]
    r_create = client.post(
        "/api/v1/sessions",
        headers={"X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4())},
        json={"nickname": "ResultPlayer"},
    )
    session_id = r_create.json()["session_id"]

    # When not completed, returns 409 RESULT_NOT_READY
    r_res_not_ready = client.get(f"/api/v1/sessions/{session_id}/result")
    assert r_res_not_ready.status_code == 409
    assert r_res_not_ready.json()["error"]["code"] == "RESULT_NOT_READY"

    # Mark session as completed
    session_obj = db_session.get(GameSession, uuid.UUID(session_id))
    session_obj.status = SessionStatus.completed
    session_obj.final_status = FinalStatus.near_bankruptcy
    session_obj.final_score = 464
    session_obj.completed_at = datetime.now(timezone.utc)
    session_obj.ranking_eligible = True
    session_obj.state = {
        "cash_kopeks": 234000000,
        "monthly_revenue_kopeks": 180000000,
        "monthly_fixed_cost_kopeks": 200000000,
        "variable_cost_bps": 3000,
        "reputation": 65,
    }
    db_session.commit()

    # Now returns 200 with score and rank details
    r_result = client.get(f"/api/v1/sessions/{session_id}/result")
    assert r_result.status_code == 200
    res_data = r_result.json()
    assert res_data["session_id"] == session_id
    assert res_data["final_status"] == "near_bankruptcy"
    assert res_data["score"] == 464
    assert res_data["rank"] == 1
    assert res_data["total_ranked"] == 1
    assert "startup" in res_data
    assert "score_breakdown" in res_data
    assert "final_metrics" in res_data
    assert res_data["summary"] != ""


def test_leaderboard_endpoint(client, db_session):
    # Create several installations and sessions with different scores
    inst1 = BrowserInstallation(token_hash="1" * 64)
    inst2 = BrowserInstallation(token_hash="2" * 64)
    inst3 = BrowserInstallation(token_hash="3" * 64)
    inst4_demo = BrowserInstallation(token_hash="4" * 64)
    db_session.add_all([inst1, inst2, inst3, inst4_demo])
    db_session.commit()

    template = db_session.scalars(select(StartupTemplate)).first()

    # 1. Score 850
    s1 = GameSession(
        browser_installation_id=inst1.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="TopPlayer",
        status=SessionStatus.completed,
        final_status=FinalStatus.survived,
        final_score=850,
        ranking_eligible=True,
        completed_at=datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        template_snapshot={"name": template.slug},
        state={},
    )
    # 2. Score 850 (Tie: must receive same rank 1)
    s2 = GameSession(
        browser_installation_id=inst2.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="TiedPlayer",
        status=SessionStatus.completed,
        final_status=FinalStatus.survived,
        final_score=850,
        ranking_eligible=True,
        completed_at=datetime(2026, 1, 1, 11, 0, 0, tzinfo=timezone.utc),
        template_snapshot={"name": template.slug},
        state={},
    )
    # 3. Score 500 (Rank 3)
    s3 = GameSession(
        browser_installation_id=inst3.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="ThirdPlayer",
        status=SessionStatus.completed,
        final_status=FinalStatus.deep_crisis,
        final_score=500,
        ranking_eligible=True,
        completed_at=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        template_snapshot={"name": template.slug},
        state={},
    )
    # 4. Demo session (ranking_eligible=False, MUST NOT appear)
    s4 = GameSession(
        browser_installation_id=inst4_demo.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="DemoPlayer",
        status=SessionStatus.completed,
        final_status=FinalStatus.bankrupt,
        final_score=999,
        ranking_eligible=False,
        completed_at=datetime(2026, 1, 1, 13, 0, 0, tzinfo=timezone.utc),
        template_snapshot={"name": template.slug},
        state={},
    )
    db_session.add_all([s1, s2, s3, s4])
    db_session.commit()

    r_lb = client.get("/api/v1/leaderboard")
    assert r_lb.status_code == 200
    lb_data = r_lb.json()
    assert lb_data["total"] == 3
    assert len(lb_data["items"]) == 3

    # Check ties and ranking
    item0 = lb_data["items"][0]
    item1 = lb_data["items"][1]
    item2 = lb_data["items"][2]

    assert item0["score"] == 850
    assert item1["score"] == 850
    assert item0["rank"] == 1
    assert item1["rank"] == 1

    assert item2["score"] == 500
    assert item2["rank"] == 3
    assert item2["nickname"] == "ThirdPlayer"


def test_missing_cookie_on_protected_endpoints_returns_401(client, db_session):
    # Create a session directly in DB
    inst = BrowserInstallation(token_hash="z" * 64)
    db_session.add(inst)
    db_session.commit()
    template = db_session.scalars(select(StartupTemplate)).first()
    sess = GameSession(
        browser_installation_id=inst.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="PlayerZ",
        template_snapshot={},
        state={},
    )
    db_session.add(sess)
    db_session.commit()

    # Client without cookies trying to access /sessions/{id}
    # Clear client cookies
    client.cookies.clear()
    r = client.get(f"/api/v1/sessions/{sess.id}")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "UNAUTHORIZED"


def test_invalid_idempotency_key_format_returns_422(client):
    b = client.get("/api/v1/bootstrap")
    csrf = b.json()["csrf_token"]
    r = client.post(
        "/api/v1/sessions",
        headers={"X-CSRF-Token": csrf, "Idempotency-Key": "not-a-valid-uuid"},
        json={"nickname": "ValidNick"},
    )
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "INVALID_IDEMPOTENCY_KEY"



def test_get_round_without_cookie_returns_401(client, db_session):
    # Setup session and round
    inst = BrowserInstallation(token_hash="round_user" * 6)
    db_session.add(inst)
    db_session.commit()
    template = db_session.scalars(select(StartupTemplate)).first()
    sess = GameSession(
        browser_installation_id=inst.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="RoundUser",
        template_snapshot={},
        state={},
    )
    db_session.add(sess)
    db_session.commit()
    round_obj = GameRound(
        session_id=sess.id,
        round_number=1,
        idempotency_key=uuid.uuid4(),
        request_sha256="0" * 64,
        status=RoundStatus.resolved,
    )
    db_session.add(round_obj)
    db_session.commit()

    # Client without cookies trying to access /rounds/{id}
    client.cookies.clear()
    r = client.get(f"/api/v1/rounds/{round_obj.id}")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "UNAUTHORIZED"


def test_post_session_without_cookie_returns_401(client):
    client.cookies.clear()
    r = client.post(
        "/api/v1/sessions",
        headers={"Idempotency-Key": str(uuid.uuid4()), "X-CSRF-Token": "some-token"},
        json={"nickname": "NoCookiePlayer"},
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "UNAUTHORIZED"


def test_continue_rejected_after_round_3(client, db_session):
    b = client.get("/api/v1/bootstrap")
    csrf = b.json()["csrf_token"]
    r_create = client.post(
        "/api/v1/sessions",
        headers={"X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4())},
        json={"nickname": "Round3Player"},
    )
    session_id = r_create.json()["session_id"]
    sess_obj = db_session.get(GameSession, uuid.UUID(session_id))
    sess_obj.next_round = 3
    sess_obj.status = SessionStatus.result_pending

    r3 = GameRound(
        session_id=sess_obj.id,
        round_number=3,
        idempotency_key=uuid.uuid4(),
        request_sha256="3" * 64,
        status=RoundStatus.resolved,
    )
    db_session.add(r3)
    db_session.commit()

    r_cont3 = client.post(
        f"/api/v1/sessions/{session_id}/continue",
        headers={"X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4())},
        json={"resolved_round_id": str(r3.id)},
    )
    assert r_cont3.status_code == 409
    assert r_cont3.json()["error"]["code"] == "CONTINUE_NOT_AVAILABLE"


def test_v2_snapshot_combo_and_damage_response(client, monkeypatch):
    from backend.app.api import routes
    monkeypatch.setattr(routes.random, 'choice', lambda templates: next(t for t in templates if t.slug == 'petmind'))
    csrf = client.get('/api/v1/bootstrap').json()['csrf_token']
    headers = {'X-CSRF-Token': csrf, 'Idempotency-Key': str(uuid.uuid4())}
    created = client.post('/api/v1/sessions', headers=headers, json={'nickname': 'V2Player'})
    assert created.status_code == 201
    session_id = created.json()['session_id']
    choices = client.get(f'/api/v1/sessions/{session_id}').json()['available_choices']
    assert all(not choice['combo_available'] for choice in choices)
    headers['Idempotency-Key'] = str(uuid.uuid4())
    result = client.post(f'/api/v1/sessions/{session_id}/choices', headers=headers,
                         json={'choice_id': 'petmind_r1_b'})
    assert result.status_code == 200
    body = result.json()
    assert body['impact']['baseline_cash_kopeks'] - body['state_after']['cash_kopeks'] == body['impact']['player_damage_kopeks']
    assert body['defense']['reason']
    headers['Idempotency-Key'] = str(uuid.uuid4())
    continued = client.post(f'/api/v1/sessions/{session_id}/continue', headers=headers,
                            json={'resolved_round_id': body['round_id']})
    assert continued.status_code == 200
    choices = client.get(f'/api/v1/sessions/{session_id}').json()['available_choices']
    assert [choice['id'] for choice in choices if choice['combo_available']] == ['petmind_r2_b']
