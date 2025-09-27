"""first

Revision ID: 1a77097885b9
Revises: 0dbf499fa347
Create Date: 2025-09-27 09:29:25.986243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a77097885b9'
down_revision: Union[str, Sequence[str], None] = '0dbf499fa347'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
