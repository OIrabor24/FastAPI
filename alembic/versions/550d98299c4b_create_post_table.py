"""create post table

Revision ID: 550d98299c4b
Revises: 
Create Date: 2022-06-27 18:34:43.489633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '550d98299c4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
    , sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
