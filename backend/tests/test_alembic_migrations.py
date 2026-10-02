import os
import json
import sqlalchemy as sa
import tempfile
import pytest
from sqlalchemy import create_engine, inspect
from alembic.config import Config
from alembic import command
from alembic.migration import MigrationContext
from alembic.autogenerate import compare_metadata
from backend.app.db.models import Base


@pytest.fixture
def temp_alembic_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db_url = f"sqlite:///{path}"
    yield path, db_url
    if os.path.exists(path):
        os.remove(path)


def test_alembic_migration_upgrade_and_downgrade(temp_alembic_db):
    db_path, db_url = temp_alembic_db
    
    # Path to alembic.ini
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    alembic_ini_path = os.path.join(repo_root, "backend", "alembic.ini")
    assert os.path.exists(alembic_ini_path), f"alembic.ini not found at {alembic_ini_path}"
    
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    alembic_cfg.set_main_option("script_location", os.path.join(repo_root, "backend", "alembic"))
    
    # 1. Upgrade to head
    command.upgrade(alembic_cfg, "head")
    
    # Inspect tables
    engine = create_engine(db_url)
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    
    expected_tables = {
        "startup_templates", "startup_template_versions", "browser_installations",
        "game_sessions", "game_rounds", "monthly_ledger", "alembic_version",
    }
    assert expected_tables == tables
    assert not any(name.startswith(("ai_", "admin_")) for name in tables)

    # Strict metadata parity check: zero differences between migration and Base.metadata
    with engine.connect() as conn:
        ctx = MigrationContext.configure(conn)
        diff = compare_metadata(ctx, Base.metadata)
        assert diff == [], f"Schema divergence detected between Base.metadata and Alembic migrations: {diff}"
    
    engine.dispose()


def test_upgrade_preserves_resolved_financial_history_and_resets_open_round(temp_alembic_db):
    import uuid
    from datetime import datetime, timezone
    from sqlalchemy import MetaData, Table

    db_path, db_url = temp_alembic_db
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    cfg = Config(os.path.join(repo_root, "backend", "alembic.ini"))
    cfg.set_main_option("sqlalchemy.url", db_url)
    cfg.set_main_option("script_location", os.path.join(repo_root, "backend", "alembic"))
    command.upgrade(cfg, "0001_initial_schema")
    engine = create_engine(db_url)
    meta = MetaData()
    with engine.begin() as conn:
        meta.reflect(bind=conn)
        tables = {name: Table(name, meta, autoload_with=conn) for name in meta.tables}
        now = datetime.now(timezone.utc)
        template_id, install_a, install_b = str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())
        sess_a, sess_b = str(uuid.uuid4()), str(uuid.uuid4())
        resolved_id, pending_id = str(uuid.uuid4()), str(uuid.uuid4())
        conn.execute(tables["startup_templates"].insert().values(
            id=template_id, slug="coffeebot", is_enabled=True, current_version=1, created_at=now,
        ))
        conn.execute(tables["startup_template_versions"].insert().values(
            template_id=template_id, version=1, name="CoffeeBot", industry="food",
            public_profile={}, private_profile={}, finance_config={}, asset_key="coffeebot",
            baseline_series=[], baseline_cash_m9_kopeks=0, content_sha256="0"*64,
            engine_version="economy-v1", created_at=now,
        ))
        for install_id, session_id, status, next_round, elapsed in [
            (install_a, sess_a, "result_pending", 2, 3),
            (install_b, sess_b, "processing", 2, 3),
        ]:
            conn.execute(tables["browser_installations"].insert().values(
                id=install_id, token_hash=str(install_id).replace("-", "")[:64].ljust(64,"a"),
                created_at=now, last_seen_at=now,
            ))
            conn.execute(tables["game_sessions"].insert().values(
                id=session_id, browser_installation_id=install_id, startup_template_id=template_id,
                startup_version=1, nickname="Player", status=status, next_round=next_round,
                elapsed_months=elapsed, template_snapshot={"slug":"coffeebot"},
                state={"cash_kopeks": 500}, engine_version="economy-v1", prompt_version="prompt-v1",
                scoring_version="scoring-v1", version=1, ranking_eligible=True,
                created_at=now, updated_at=now,
            ))
        outcome = {"event":{"title":"old generated title","narrative":"private raw AI text"},
                   "defense":{"type":"none"},"deltas":{"cash_kopeks":-7},
                   "state_after":{"cash_kopeks":493}}
        conn.execute(tables["game_rounds"].insert().values(
            id=resolved_id, session_id=sess_a, round_number=1, idempotency_key=str(uuid.uuid4()),
            request_sha256="1"*64, attack_text="raw free text attack", hint_id="secret-hint",
            status="resolved", input_snapshot={"attack":"raw free text attack"},
            ai_analysis={"private":"raw AI JSON"}, outcome=outcome, event_title="old generated title",
            event_narrative="private raw AI text", defense_summary="defense", new_circumstance="old",
            created_at=now, resolved_at=now,
        ))
        conn.execute(tables["monthly_ledger"].insert().values(
            id=str(uuid.uuid4()), session_id=sess_a, round_id=resolved_id, month_no=1,
            opening_cash_kopeks=500, revenue_by_stream={"kiosks":100}, variable_cost_kopeks=20,
            fixed_cost_kopeks=30, incident_cost_kopeks=0, defense_cost_kopeks=0,
            closing_cash_kopeks=493, unpaid_obligations_kopeks=0, reputation_after=70,
            applied_effects=[], created_at=now,
        ))
        conn.execute(tables["game_rounds"].insert().values(
            id=pending_id, session_id=sess_b, round_number=1, idempotency_key=str(uuid.uuid4()),
            request_sha256="2"*64, attack_text="unfinished attack", status="queued",
            input_snapshot={"attack":"unfinished attack"}, created_at=now,
        ))
        conn.execute(tables["ai_jobs"].insert().values(
            id=str(uuid.uuid4()), round_id=pending_id, status="queued", primary_model="legacy",
            attempt_count=0, prompt_version="prompt-v1", policy_version=1,
            available_at=now, created_at=now,
        ))
    command.upgrade(cfg, "head")
    with engine.connect() as conn:
        assert conn.execute(sa.text("SELECT round_id FROM monthly_ledger")).all() == [(str(resolved_id),)]
        result = conn.execute(sa.text("SELECT status, elapsed_months, attack_choices_snapshot FROM game_sessions WHERE id=:id"), {"id": str(sess_b)}).one()
        assert result.status == "ready" and result.elapsed_months == 3
        assert len(json.loads(result.attack_choices_snapshot)) == 12
        assert conn.execute(sa.text("SELECT count(*) FROM game_rounds WHERE id=:id"), {"id": str(pending_id)}).scalar_one() == 0
        cleaned = conn.execute(sa.text("SELECT outcome FROM game_rounds WHERE id=:id"), {"id": str(resolved_id)}).scalar_one()
        cleaned = json.loads(cleaned)
        assert cleaned["deltas"]["cash_kopeks"] == -7
        assert cleaned["event"]["narrative"] == ""
        narrative_columns = conn.execute(sa.text(
            "SELECT event_title, event_narrative, new_circumstance FROM game_rounds WHERE id=:id"
        ), {"id": str(resolved_id)}).one()
        assert narrative_columns == (None, None, None)
        assert "attack_text" not in inspect(conn).get_columns("game_rounds")
    engine.dispose()
