"""empty message

Revision ID: 427c3593df70
Revises: c087030d3139
Create Date: 2025-12-31 19:15:42.699730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '427c3593df70'
down_revision: Union[str, Sequence[str], None] = 'c087030d3139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
