"""Изменение в таблице users поля created_at

Revision ID: 7b6b20b5dc5e
Revises: fb9aec375f55
Create Date: 2025-06-15 10:40:49.953181

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7b6b20b5dc5e"
down_revision: Union[str, None] = "fb9aec375f55"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
    )
