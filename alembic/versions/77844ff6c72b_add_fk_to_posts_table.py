"""add fk to posts table

Revision ID: 77844ff6c72b
Revises: b87bfcbcced5
Create Date: 2022-06-28 17:41:27.770405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77844ff6c72b'
down_revision = 'b87bfcbcced5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
