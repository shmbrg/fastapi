"""remove role col in users

Revision ID: e5737a266381
Revises: 0fa84cc6f4f4
Create Date: 2023-05-05 17:11:09.031585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5737a266381'
down_revision = '0fa84cc6f4f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("users", "role")


def downgrade() -> None:
    op.add_column("users", sa.Column("role", sa.String(), nullable=True))
