"""Добавление таблицы удобств в номерах

Revision ID: 697355229137
Revises: b4d9c1693a30
Create Date: 2025-06-21 20:03:02.162253

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "697355229137"
down_revision: Union[str, None] = "b4d9c1693a30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms_facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rooms_id", sa.Integer(), nullable=False),
        sa.Column("facilities_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facilities_id"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["rooms_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms_facilities")
    op.drop_table("facilities")
