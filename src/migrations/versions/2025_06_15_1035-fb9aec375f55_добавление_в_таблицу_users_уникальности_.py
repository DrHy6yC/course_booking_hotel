"""Добавление в таблицу users уникальности полей login, email

Revision ID: fb9aec375f55
Revises: f06da7f02ce7
Create Date: 2025-06-15 10:35:06.972709

"""

from typing import Sequence, Union


from alembic import op


revision: str = "fb9aec375f55"
down_revision: Union[str, None] = "f06da7f02ce7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["login"])
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "users", type_="unique")
