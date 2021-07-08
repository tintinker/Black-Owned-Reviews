"""add timeframe to  review table

Revision ID: 0e904cdf1342
Revises: 7045589863c5
Create Date: 2021-07-05 05:47:29.074993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e904cdf1342'
down_revision = '7045589863c5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('reviews', sa.Column('timeframe', sa.String(50), nullable=False))


def downgrade():
    op.drop_column('reviews', 'timeframe')
