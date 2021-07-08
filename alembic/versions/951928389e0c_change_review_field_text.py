"""change review field text

Revision ID: 951928389e0c
Revises: 899d8b19a818
Create Date: 2021-07-05 14:31:34.309311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '951928389e0c'
down_revision = '899d8b19a818'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('reviews', 'text')
    op.add_column('reviews', sa.Column('text', sa.String(1000), nullable=True))

def downgrade():
    pass
