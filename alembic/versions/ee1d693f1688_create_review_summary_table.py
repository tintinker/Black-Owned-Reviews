"""create review_summary table

Revision ID: ee1d693f1688
Revises: 35df26f7c8bc
Create Date: 2021-07-05 05:09:13.153333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee1d693f1688'
down_revision = '35df26f7c8bc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'review_summary',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url_id', sa.String(50), nullable=False),
        sa.Column('avg_rating', sa.Integer, nullable=False),
        sa.Column('num_reviews', sa.Integer, nullable=False),
        sa.Column('num_downloaded_reviews', sa.Integer, nullable=False),

    )
def downgrade():
    op.drop_table('review_summary')
