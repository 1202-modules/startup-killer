"""Allow a browser installation to create a new game after completing one."""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_multiple_browser_sessions"
down_revision: Union[str, None] = "0002_deterministic_attack_choices"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_game_sessions_browser_installation_id", table_name="game_sessions")
    op.create_index(
        "ix_game_sessions_browser_installation_id",
        "game_sessions",
        ["browser_installation_id"],
        unique=False,
    )


def downgrade() -> None:
    duplicates = op.get_bind().execute(sa.text(
        "SELECT 1 FROM game_sessions GROUP BY browser_installation_id HAVING COUNT(*) > 1 LIMIT 1"
    )).first()
    if duplicates:
        raise RuntimeError("Cannot restore one-session-per-browser while repeated games exist")
    op.drop_index("ix_game_sessions_browser_installation_id", table_name="game_sessions")
    op.create_index(
        "ix_game_sessions_browser_installation_id",
        "game_sessions",
        ["browser_installation_id"],
        unique=True,
    )
