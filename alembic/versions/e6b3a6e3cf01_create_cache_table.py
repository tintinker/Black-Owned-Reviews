"""create cache table

Revision ID: e6b3a6e3cf01
Revises: 
Create Date: 2021-07-05 04:54:47.903356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6b3a6e3cf01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cache',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url_id', sa.String(50), nullable=False),
    )


def downgrade():
    op.drop_table('cache')
