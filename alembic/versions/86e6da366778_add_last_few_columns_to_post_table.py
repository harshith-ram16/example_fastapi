"""add last few columns to post table

Revision ID: 86e6da366778
Revises: 3ea1b76d7ee5
Create Date: 2026-10-25 16:37:52.384179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86e6da366778'
down_revision: Union[str, Sequence[str], None] = '3ea1b76d7ee5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("published",sa.Boolean(),nullable=False,server_default="True"))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
