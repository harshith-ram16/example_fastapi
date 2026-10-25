"""add content column to post table

Revision ID: a05c60262573
Revises: 9c49e549358f
Create Date: 2026-10-25 15:17:53.050993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a05c60262573'
down_revision: Union[str, Sequence[str], None] = '9c49e549358f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
