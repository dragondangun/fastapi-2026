"""create posts table

Revision ID: b253def6fbf4
Revises:
Create Date: 2026-03-23 11:54:08.255334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b253def6fbf4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False,
                              primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
