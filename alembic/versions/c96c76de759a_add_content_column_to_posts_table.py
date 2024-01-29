"""add content column to posts table

Revision ID: c96c76de759a
Revises: a5c9afb5dbcf
Create Date: 2024-01-29 23:20:46.999873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c96c76de759a'
down_revision: Union[str, None] = 'a5c9afb5dbcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
