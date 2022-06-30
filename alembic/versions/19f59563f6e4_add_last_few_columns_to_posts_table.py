"""add last few columns to posts table

Revision ID: 19f59563f6e4
Revises: 77844ff6c72b
Create Date: 2022-06-28 18:16:46.063317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19f59563f6e4'
down_revision = '77844ff6c72b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass