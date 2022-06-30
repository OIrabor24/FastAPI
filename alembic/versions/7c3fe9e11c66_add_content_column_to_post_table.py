"""add content column to post table

Revision ID: 7c3fe9e11c66
Revises: 550d98299c4b
Create Date: 2022-06-28 17:23:12.110942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c3fe9e11c66'
down_revision = '550d98299c4b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False)) 
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content') 
    pass
