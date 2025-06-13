"""Добавление номеров в БД

Revision ID: 277ced62e04c
Revises: 2cc9735fdf6e
Create Date: 2025-06-13 10:04:43.384827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '277ced62e04c'
down_revision: Union[str, None] = '2cc9735fdf6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hotel_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('rooms')
