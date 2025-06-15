"""Добавление пользователей

Revision ID: 8a93a40d24a9
Revises: f50c81a97ba7
Create Date: 2025-06-15 09:10:55.655670

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8a93a40d24a9"
down_revision: Union[str, None] = "f50c81a97ba7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("login", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("age >= 0 AND age <= 150", name="age_range_check"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
