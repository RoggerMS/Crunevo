"""extend login log fields

Revision ID: b1327c7d9c78
Revises: 2c17a7ce8387
Create Date: 2025-06-09 06:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "b1327c7d9c78"
down_revision = "2c17a7ce8387"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "login_logs", sa.Column("country", sa.String(length=100), nullable=True)
    )
    op.add_column("login_logs", sa.Column("city", sa.String(length=100), nullable=True))
    op.add_column(
        "login_logs", sa.Column("device_type", sa.String(length=50), nullable=True)
    )
    op.add_column(
        "login_logs", sa.Column("method", sa.String(length=50), nullable=True)
    )


def downgrade():
    op.drop_column("login_logs", "method")
    op.drop_column("login_logs", "device_type")
    op.drop_column("login_logs", "city")
    op.drop_column("login_logs", "country")
