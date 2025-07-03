"""Добавление триггера в таблицу users для поля created_at

Revision ID: 8a86ef1529a7
Revises: 019f2544a3d3
Create Date: 2025-06-15 11:23:27.322163

"""

from typing import Sequence, Union

from alembic import op

from src.migrations.triggers import (
    create_trigger_function,
    create_update_trigger,
)

# revision identifiers, used by Alembic.
revision: str = "8a86ef1529a7"
down_revision: Union[str, None] = "019f2544a3d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = "users"
column = "created_at"
type_before = "INSERT"


def upgrade() -> None:
    op.execute(create_trigger_function(table_name, column))
    op.execute(create_update_trigger(table_name, column, type_before))


def downgrade() -> None:
    op.execute(
        f"DROP TRIGGER IF EXISTS {table_name}_{type_before}_timestamp ON {table_name};"
    )
    op.execute(f"DROP FUNCTION IF EXISTS set_{table_name}_{column};")
