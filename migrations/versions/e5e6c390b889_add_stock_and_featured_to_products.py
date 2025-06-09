"""add stock and featured to products

Revision ID: e5e6c390b889
Revises: b1327c7d9c78
Create Date: 2025-06-10 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "e5e6c390b889"
down_revision = "b1327c7d9c78"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("products", sa.Column("stock", sa.Integer(), nullable=True))
    op.add_column("products", sa.Column("featured", sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column("products", "featured")
    op.drop_column("products", "stock")
