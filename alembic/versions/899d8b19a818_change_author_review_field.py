"""change author review field

Revision ID: 899d8b19a818
Revises: 1624af05f476
Create Date: 2021-07-05 14:26:58.506169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '899d8b19a818'
down_revision = '1624af05f476'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('reviews', 'author_id')
    op.add_column('reviews', sa.Column('author_id', sa.String(50), nullable=False))

def downgrade():
    pass

