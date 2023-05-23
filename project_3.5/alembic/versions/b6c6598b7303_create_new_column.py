"""create new column

Revision ID: b6c6598b7303
Revises: b5817ae9a1f0
Create Date: 2023-05-12 10:28:34.674832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6c6598b7303'
down_revision = 'b5817ae9a1f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("address", sa.Column("test_col_1", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("address", "test_col_1")
