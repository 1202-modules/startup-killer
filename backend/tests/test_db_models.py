import uuid
from datetime import datetime, timezone
import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from backend.app.config import Settings
from backend.app.db.session import Base
from backend.app.db.models import (
    StartupTemplate,
    StartupTemplateVersion,
    BrowserInstallation,
    GameSession,
    GameRound,
    MonthlyLedger,
    SessionStatus,
    FinalStatus,
    RoundStatus,
)
from backend.app.db.seed import seed_startups


@pytest.fixture
def db_session():
    # In-memory SQLite with foreign keys enabled
    engine = create_engine("sqlite:///:memory:")
    
    # Enable foreign keys for SQLite connection
    from sqlalchemy import event
    from sqlalchemy.engine import Engine

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_config_settings():
    settings = Settings()
    assert settings.COOKIE_NAME == "sk_browser"
    assert settings.SECRET_KEY is not None
    assert len(settings.SECRET_KEY) >= 16
    assert settings.sync_database_url is not None
    assert settings.async_database_url is not None


def test_seed_startups_and_idempotency(db_session):
    # Initial seed
    templates = seed_startups(db_session)
    assert len(templates) == 10

    # Query templates
    all_templates = db_session.scalars(select(StartupTemplate)).all()
    assert len(all_templates) == 10

    all_versions = db_session.scalars(select(StartupTemplateVersion)).all()
    assert len(all_versions) == 10

    # Check coffeebot template and version
    coffeebot = db_session.scalar(select(StartupTemplate).where(StartupTemplate.slug == "coffeebot"))
    assert coffeebot is not None
    assert coffeebot.is_enabled is True
    assert coffeebot.current_version == 2

    cb_version = db_session.scalar(
        select(StartupTemplateVersion).where(
            StartupTemplateVersion.template_id == coffeebot.id,
            StartupTemplateVersion.version == 2,
        )
    )
    assert cb_version is not None
    assert cb_version.name == "CoffeeBot"
    assert cb_version.industry == "Food robotics"
    assert cb_version.asset_key == "coffeebot"
    assert cb_version.baseline_cash_m9_kopeks == 472385682
    assert cb_version.content_sha256 is not None
    assert len(cb_version.content_sha256) == 64
    assert len(cb_version.finance_config["revenue_streams"]) == 2

    coffeebot.current_version = 1
    db_session.commit()
    seed_startups(db_session)
    assert coffeebot.current_version == 2

    # Check idempotency: run seed again
    seed_again = seed_startups(db_session)
    assert len(seed_again) == 10
    total_templates = db_session.scalars(select(StartupTemplate)).all()
    assert len(total_templates) == 10
    total_versions = db_session.scalars(select(StartupTemplateVersion)).all()
    assert len(total_versions) == 10


def test_create_full_game_hierarchy(db_session):
    seed_startups(db_session)
    template = db_session.scalar(select(StartupTemplate).where(StartupTemplate.slug == "petmind"))
    assert template is not None

    # 1. Browser Installation
    installation = BrowserInstallation(
        token_hash="a" * 64,
        created_at=datetime.now(timezone.utc),
        last_seen_at=datetime.now(timezone.utc),
    )
    db_session.add(installation)
    db_session.commit()
    db_session.refresh(installation)
    assert installation.id is not None

    # 2. Game Session
    session = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="TestPlayer",
        status=SessionStatus.ready,
        next_round=1,
        elapsed_months=0,
        template_snapshot={"name": "PetMind", "slug": "petmind"},
        state={"cash_kopeks": 800000000, "reputation": 76},
        engine_version="economy-v1",
        scoring_version="scoring-v1",
        version=1,
        ranking_eligible=True,
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    assert session.id is not None
    assert session.status == SessionStatus.ready
    assert session.ranking_eligible is True

    # 3. Game Round
    idempotency_key = uuid.uuid4()
    game_round = GameRound(
        session_id=session.id,
        round_number=1,
        idempotency_key=idempotency_key,
        request_sha256="b" * 64,
        selected_choice_id="petmind-r1-c1",
        choice_snapshot={"id": "petmind-r1-c1"},
        status=RoundStatus.resolved,
        event_title="Ценовая война",
        event_narrative="Конкурент снизил цены на умные ошейники на 40%.",
    )
    db_session.add(game_round)
    db_session.commit()
    db_session.refresh(game_round)
    assert game_round.id is not None

    # 5. Monthly Ledger
    ledger_m1 = MonthlyLedger(
        session_id=session.id,
        round_id=game_round.id,
        month_no=1,
        opening_cash_kopeks=800000000,
        revenue_by_stream={"collars": 150000000, "subs": 50000000},
        variable_cost_kopeks=60000000,
        fixed_cost_kopeks=150000000,
        incident_cost_kopeks=0,
        defense_cost_kopeks=0,
        closing_cash_kopeks=740000000,
        unpaid_obligations_kopeks=0,
        reputation_after=76,
        applied_effects=[],
    )
    db_session.add(ledger_m1)
    db_session.commit()
    db_session.refresh(ledger_m1)
    assert ledger_m1.id is not None
    assert ledger_m1.closing_cash_kopeks == 740000000

    # Verify relationships
    assert len(session.rounds) == 1
    assert session.rounds[0].id == game_round.id
    assert len(session.ledgers) == 1
    assert session.ledgers[0].id == ledger_m1.id


def test_unique_constraint_browser_installation_session(db_session):
    seed_startups(db_session)
    template = db_session.scalar(select(StartupTemplate).where(StartupTemplate.slug == "petmind"))

    installation = BrowserInstallation(token_hash="c" * 64)
    db_session.add(installation)
    db_session.commit()

    # Session 1
    s1 = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="PlayerOne",
        template_snapshot={},
        state={},
    )
    db_session.add(s1)
    db_session.commit()

    # Session 2 for the same browser installation must fail
    s2 = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="PlayerTwo",
        template_snapshot={},
        state={},
    )
    db_session.add(s2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_unique_constraint_game_round_number(db_session):
    seed_startups(db_session)
    template = db_session.scalar(select(StartupTemplate).where(StartupTemplate.slug == "petmind"))

    installation = BrowserInstallation(token_hash="d" * 64)
    db_session.add(installation)
    db_session.commit()

    session = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="PlayerRoundTest",
        template_snapshot={},
        state={},
    )
    db_session.add(session)
    db_session.commit()

    r1 = GameRound(
        session_id=session.id,
        round_number=1,
        idempotency_key=uuid.uuid4(),
        request_sha256="1" * 64,
    )
    db_session.add(r1)
    db_session.commit()

    # Same round_number in the same session must fail
    r2 = GameRound(
        session_id=session.id,
        round_number=1,
        idempotency_key=uuid.uuid4(),
        request_sha256="2" * 64,
    )
    db_session.add(r2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_unique_constraint_game_round_idempotency_key(db_session):
    seed_startups(db_session)
    template = db_session.scalar(select(StartupTemplate).where(StartupTemplate.slug == "petmind"))

    installation = BrowserInstallation(token_hash="e" * 64)
    db_session.add(installation)
    db_session.commit()

    session = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="PlayerIdemTest",
        template_snapshot={},
        state={},
    )
    db_session.add(session)
    db_session.commit()

    same_key = uuid.uuid4()
    r1 = GameRound(
        session_id=session.id,
        round_number=1,
        idempotency_key=same_key,
        request_sha256="1" * 64,
    )
    db_session.add(r1)
    db_session.commit()

    # Same idempotency_key in the same session must fail
    r2 = GameRound(
        session_id=session.id,
        round_number=2,
        idempotency_key=same_key,
        request_sha256="2" * 64,
    )
    db_session.add(r2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_unique_constraint_monthly_ledger_month(db_session):
    seed_startups(db_session)
    template = db_session.scalar(select(StartupTemplate).where(StartupTemplate.slug == "petmind"))

    installation = BrowserInstallation(token_hash="f" * 64)
    db_session.add(installation)
    db_session.commit()

    session = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="PlayerLedgerTest",
        template_snapshot={},
        state={},
    )
    db_session.add(session)
    db_session.commit()

    round1 = GameRound(
        session_id=session.id,
        round_number=1,
        idempotency_key=uuid.uuid4(),
        request_sha256="1" * 64,
    )
    db_session.add(round1)
    db_session.commit()

    m1_a = MonthlyLedger(
        session_id=session.id,
        round_id=round1.id,
        month_no=1,
        opening_cash_kopeks=800000000,
        revenue_by_stream={},
        variable_cost_kopeks=0,
        fixed_cost_kopeks=0,
        incident_cost_kopeks=0,
        defense_cost_kopeks=0,
        closing_cash_kopeks=800000000,
        unpaid_obligations_kopeks=0,
        reputation_after=70,
        applied_effects=[],
    )
    db_session.add(m1_a)
    db_session.commit()

    # Same month_no for the same session must fail
    m1_b = MonthlyLedger(
        session_id=session.id,
        round_id=round1.id,
        month_no=1,
        opening_cash_kopeks=800000000,
        revenue_by_stream={},
        variable_cost_kopeks=0,
        fixed_cost_kopeks=0,
        incident_cost_kopeks=0,
        defense_cost_kopeks=0,
        closing_cash_kopeks=800000000,
        unpaid_obligations_kopeks=0,
        reputation_after=70,
        applied_effects=[],
    )
    db_session.add(m1_b)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_check_constraints_game_session(db_session):
    seed_startups(db_session)
    template = db_session.scalar(select(StartupTemplate).where(StartupTemplate.slug == "petmind"))
    installation = BrowserInstallation(token_hash="g" * 64)
    db_session.add(installation)
    db_session.commit()

    # Invalid next_round (> 3)
    s_invalid_round = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="InvalidRound",
        next_round=4,
        template_snapshot={},
        state={},
    )
    db_session.add(s_invalid_round)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # Invalid elapsed_months (> 9)
    s_invalid_months = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="InvalidMonths",
        elapsed_months=10,
        template_snapshot={},
        state={},
    )
    db_session.add(s_invalid_months)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # Invalid final_score (> 1000)
    s_invalid_score = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="InvalidScore",
        final_score=1001,
        template_snapshot={},
        state={},
    )
    db_session.add(s_invalid_score)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_check_constraints_game_round(db_session):
    seed_startups(db_session)
    template = db_session.scalar(select(StartupTemplate).where(StartupTemplate.slug == "petmind"))
    installation = BrowserInstallation(token_hash="h" * 64)
    db_session.add(installation)
    db_session.commit()

    session = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="RoundCheckTest",
        template_snapshot={},
        state={},
    )
    db_session.add(session)
    db_session.commit()

    # Invalid round_number (> 3)
    r_invalid = GameRound(
        session_id=session.id,
        round_number=4,
        idempotency_key=uuid.uuid4(),
        request_sha256="4" * 64,
    )
    db_session.add(r_invalid)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_check_constraints_monthly_ledger(db_session):
    seed_startups(db_session)
    template = db_session.scalar(select(StartupTemplate).where(StartupTemplate.slug == "petmind"))
    installation = BrowserInstallation(token_hash="i" * 64)
    db_session.add(installation)
    db_session.commit()

    session = GameSession(
        browser_installation_id=installation.id,
        startup_template_id=template.id,
        startup_version=template.current_version,
        nickname="LedgerCheckTest",
        template_snapshot={},
        state={},
    )
    db_session.add(session)
    db_session.commit()

    r = GameRound(
        session_id=session.id,
        round_number=1,
        idempotency_key=uuid.uuid4(),
        request_sha256="1" * 64,
    )
    db_session.add(r)
    db_session.commit()

    # Invalid month_no (> 9)
    ledger_invalid_month = MonthlyLedger(
        session_id=session.id,
        round_id=r.id,
        month_no=10,
        opening_cash_kopeks=100,
        revenue_by_stream={},
        variable_cost_kopeks=0,
        fixed_cost_kopeks=0,
        incident_cost_kopeks=0,
        defense_cost_kopeks=0,
        closing_cash_kopeks=100,
        unpaid_obligations_kopeks=0,
        reputation_after=50,
        applied_effects=[],
    )
    db_session.add(ledger_invalid_month)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # Invalid closing_cash_kopeks (< 0)
    ledger_invalid_cash = MonthlyLedger(
        session_id=session.id,
        round_id=r.id,
        month_no=1,
        opening_cash_kopeks=100,
        revenue_by_stream={},
        variable_cost_kopeks=0,
        fixed_cost_kopeks=0,
        incident_cost_kopeks=0,
        defense_cost_kopeks=0,
        closing_cash_kopeks=-1,
        unpaid_obligations_kopeks=0,
        reputation_after=50,
        applied_effects=[],
    )
    db_session.add(ledger_invalid_cash)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # Invalid reputation_after (> 100)
    ledger_invalid_rep = MonthlyLedger(
        session_id=session.id,
        round_id=r.id,
        month_no=1,
        opening_cash_kopeks=100,
        revenue_by_stream={},
        variable_cost_kopeks=0,
        fixed_cost_kopeks=0,
        incident_cost_kopeks=0,
        defense_cost_kopeks=0,
        closing_cash_kopeks=100,
        unpaid_obligations_kopeks=0,
        reputation_after=101,
        applied_effects=[],
    )
    db_session.add(ledger_invalid_rep)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_session_generator_and_context_managers():
    from backend.app.db.session import get_db, db_session

    gen = get_db()
    s = next(gen)
    assert s is not None
    s.close()

    with db_session() as s2:
        assert s2 is not None


@pytest.mark.asyncio
async def test_async_session_generator_and_context_managers():
    from backend.app.db.session import get_async_db, async_db_session

    async for s in get_async_db():
        assert s is not None
        break

    async with async_db_session() as s2:
        assert s2 is not None
