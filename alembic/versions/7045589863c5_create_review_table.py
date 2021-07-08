"""create review table

Revision ID: 7045589863c5
Revises: ee1d693f1688
Create Date: 2021-07-05 05:10:51.469527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7045589863c5'
down_revision = 'ee1d693f1688'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('shop_url_id', sa.String(50), nullable=False),
        sa.Column('author_id', sa.Integer),
        sa.Column('author_name', sa.Integer),
        sa.Column('text', sa.String(50)),
        sa.Column('rating', sa.Integer)
    )

def downgrade():
    op.drop_table('reviews')