"""Replace AI jobs and free-text attacks with immutable deterministic choices."""
from pathlib import Path
import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_deterministic_attack_choices"
down_revision: Union[str, None] = "0001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    root = Path(__file__).resolve().parents[3]
    catalog = json.loads((root / "data" / "attack_choices.json").read_text(encoding="utf-8"))
    choices_by_slug = {}
    for choice in catalog["choices"]:
        choices_by_slug.setdefault(choice["startup_slug"], []).append(choice)

    with op.batch_alter_table("game_sessions") as batch:
        batch.add_column(sa.Column("attack_catalog_version", sa.String(length=32), nullable=False, server_default="attack-choices-v1"))
        batch.add_column(sa.Column("attack_choices_snapshot", sa.JSON(), nullable=False, server_default="[]"))

    sessions = sa.Table("game_sessions", sa.MetaData(), autoload_with=bind)
    rows = bind.execute(sa.select(sessions.c.id, sessions.c.template_snapshot, sessions.c.status)).all()
    for row in rows:
        slug = (row.template_snapshot or {}).get("slug")
        snapshots = choices_by_slug.get(slug)
        if not snapshots:
            raise RuntimeError(f"No deterministic attack choices for legacy session startup {slug!r}")
        bind.execute(sessions.update().where(sessions.c.id == row.id).values(
            status="ready" if row.status == "processing" else row.status,
            attack_catalog_version=catalog["catalog_version"],
            attack_choices_snapshot=snapshots,
        ))

    rounds = sa.Table("game_rounds", sa.MetaData(), autoload_with=bind)
    ledger = sa.Table("monthly_ledger", sa.MetaData(), autoload_with=bind)
    # Unresolved rounds have no applied financial result. Drop them and reopen the round.
    bind.execute(sa.text("DELETE FROM game_rounds WHERE status <> 'resolved'"))
    bind.execute(sa.text("UPDATE game_sessions SET status = 'ready' WHERE status = 'processing'"))
    for row in bind.execute(sa.select(rounds.c.id, rounds.c.outcome)).all():
        outcome = row.outcome or {}
        outcome["event"] = {"title": "Исторический раунд", "narrative": "", "scene_type": "demand"}
        outcome.pop("new_circumstance", None)
        bind.execute(rounds.update().where(rounds.c.id == row.id).values(
            outcome=outcome,
            event_title=None,
            event_narrative=None,
            new_circumstance=None,
        ))

    # SQLite batch table rebuilds can cascade-delete dependent rows. PostgreSQL
    # applies these batch alterations in place, so reinserting there would duplicate PKs.
    preserve_for_sqlite_rebuild = bind.dialect.name == "sqlite"
    resolved_rows = ([dict(row._mapping) for row in bind.execute(
        sa.select(rounds).where(rounds.c.status == "resolved")
    )] if preserve_for_sqlite_rebuild else [])
    ledger_rows = ([dict(row._mapping) for row in bind.execute(sa.select(ledger))]
                   if preserve_for_sqlite_rebuild else [])
    for row in resolved_rows:
        row["selected_choice_id"] = None
        row["choice_snapshot"] = None
        for name in ("attack_text", "hint_id", "input_snapshot", "ai_analysis"):
            row.pop(name, None)
        row["event_title"] = None
        row["event_narrative"] = None
        row["new_circumstance"] = None

    with op.batch_alter_table("game_rounds") as batch:
        batch.add_column(sa.Column("selected_choice_id", sa.String(length=80), nullable=True))
        batch.add_column(sa.Column("choice_snapshot", sa.JSON(), nullable=True))
        batch.drop_column("attack_text")
        batch.drop_column("hint_id")
        batch.drop_column("input_snapshot")
        batch.drop_column("ai_analysis")

    with op.batch_alter_table("game_sessions") as batch:
        batch.drop_column("prompt_version")
    with op.batch_alter_table("game_sessions") as batch:
        batch.alter_column("attack_catalog_version", server_default=None)
        batch.alter_column("attack_choices_snapshot", server_default=None)

    restored_meta = sa.MetaData()
    restored_rounds = sa.Table("game_rounds", restored_meta, autoload_with=bind)
    restored_ledger = sa.Table("monthly_ledger", restored_meta, autoload_with=bind)
    if preserve_for_sqlite_rebuild and resolved_rows:
        bind.execute(restored_rounds.insert(), resolved_rows)
    if preserve_for_sqlite_rebuild and ledger_rows:
        bind.execute(restored_ledger.insert(), ledger_rows)

    for table in ("ai_key_tests", "ai_usage_events", "ai_provider_runtime", "ai_jobs",
                  "ai_credentials", "admin_settings", "admin_sessions"):
        op.drop_table(table)


def downgrade() -> None:
    raise RuntimeError(
        "0002 removes provider keys, prompt data, and unresolved jobs permanently; restore from backup to return to 0001"
    )
