"""change review id to  str

Revision ID: 7b9df09f3be4
Revises: c31c8b64c3e9
Create Date: 2021-07-05 14:05:56.584531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b9df09f3be4'
down_revision = 'c31c8b64c3e9'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('reviews', 'author_id')
    op.add_column('reviews', sa.Column('author_id', sa.String(20), nullable=False))


def downgrade():
    pass
