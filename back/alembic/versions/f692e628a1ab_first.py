"""first

Revision ID: f692e628a1ab
Revises: 1a77097885b9
Create Date: 2025-09-27 09:31:23.118378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f692e628a1ab'
down_revision: Union[str, Sequence[str], None] = '1a77097885b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
