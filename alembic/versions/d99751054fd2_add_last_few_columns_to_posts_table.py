"""add last few columns to posts table

Revision ID: d99751054fd2
Revises: 81fb47b45721
Create Date: 2026-03-25 11:47:45.498764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd99751054fd2'
down_revision: Union[str, Sequence[str], None] = '81fb47b45721'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False,
                                     server_default="TRUE"))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                     nullable=False,
                                     server_default=sa.text('NOW()')))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
