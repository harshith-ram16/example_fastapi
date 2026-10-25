"""create posts table

Revision ID: 9c49e549358f
Revises: 
Create Date: 2026-10-25 14:58:23.443474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c49e549358f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",sa.Column("id",sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
