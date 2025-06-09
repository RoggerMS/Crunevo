"""add post comment model

Revision ID: 7c5da695d26a
Revises: 810dc2c6c5d4
Create Date: 2025-06-10 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "7c5da695d26a"
down_revision = "810dc2c6c5d4"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "post_comments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("post_comments")
