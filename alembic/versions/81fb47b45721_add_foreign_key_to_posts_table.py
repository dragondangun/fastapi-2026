"""add foreign-key to posts table

Revision ID: 81fb47b45721
Revises: a0052df657c0
Create Date: 2026-03-24 14:23:53.827865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81fb47b45721'
down_revision: Union[str, Sequence[str], None] = 'a0052df657c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts",
                          referent_table="users", local_cols=['owner_id'],
                          remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
