"""expand review length

Revision ID: c31c8b64c3e9
Revises: 0e904cdf1342
Create Date: 2021-07-05 06:51:06.711826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c31c8b64c3e9'
down_revision = '0e904cdf1342'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('reviews', 'text')
    op.add_column('reviews', sa.Column('text', sa.String(250), nullable=False))


def downgrade():
    pass