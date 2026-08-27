"""create gold_prices table

Revision ID: 3ef923206dd8
Revises: 
Create Date: 2026-08-27 12:00:51.087860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ef923206dd8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "gold_prices",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("symbol", sa.String(), nullable=False, index=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("unit", sa.String(), nullable=False),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("gold_prices")
