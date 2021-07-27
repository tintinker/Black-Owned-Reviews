"""change sum to float

Revision ID: 25b3de68e4a1
Revises: 599be06c8c86
Create Date: 2021-07-08 11:50:51.474821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25b3de68e4a1'
down_revision = '599be06c8c86'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('review_summary', 'text')
    op.add_column('review_summary', sa.Column('text', sa.String(1250), nullable=True))



def downgrade():
    pass
