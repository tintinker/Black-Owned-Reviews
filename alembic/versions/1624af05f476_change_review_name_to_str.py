"""change review name to  str

Revision ID: 1624af05f476
Revises: 7b9df09f3be4
Create Date: 2021-07-05 14:13:47.938651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1624af05f476'
down_revision = '7b9df09f3be4'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('reviews', 'author_name')
    op.add_column('reviews', sa.Column('author_name', sa.String(30), nullable=False))


def downgrade():
    pass
