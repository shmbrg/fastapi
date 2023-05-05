"""create adress table

Revision ID: b4ca0daa5057
Revises: 3c8c1cbecad2
Create Date: 2023-05-05 16:38:36.515630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4ca0daa5057'
down_revision = '3c8c1cbecad2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("address",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("address1", sa.String(), nullable=False),
                    sa.Column("address2", sa.String(), nullable=False),
                    sa.Column("city", sa.String(), nullable=False),
                    sa.Column("state", sa.String(), nullable=False),
                    sa.Column("country", sa.String(), nullable=False),
                    sa.Column("postalcode", sa.String(), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table("address")
