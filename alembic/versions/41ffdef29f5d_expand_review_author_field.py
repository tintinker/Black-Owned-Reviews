"""expand review author field

Revision ID: 41ffdef29f5d
Revises: 25b3de68e4a1
Create Date: 2021-07-27 01:35:03.965102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41ffdef29f5d'
down_revision = '25b3de68e4a1'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('reviews', 'author_name')
    op.add_column('reviews', sa.Column('author_name', sa.String(100), nullable=True))

def downgrade():
    pass
