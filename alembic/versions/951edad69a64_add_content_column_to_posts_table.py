"""add content column to posts table

Revision ID: 951edad69a64
Revises: b253def6fbf4
Create Date: 2026-03-23 12:04:35.204509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '951edad69a64'
down_revision: Union[str, Sequence[str], None] = 'b253def6fbf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
