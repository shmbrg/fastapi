"""create new col

Revision ID: b5817ae9a1f0
Revises: e5737a266381
Create Date: 2023-05-11 13:14:32.379443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5817ae9a1f0'
down_revision = 'e5737a266381'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("address", sa.Column("test_col", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("address", "test_col")
