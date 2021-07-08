"""create tags table

Revision ID: eec1c319d39d
Revises: e6b3a6e3cf01
Create Date: 2021-07-05 05:00:07.516440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eec1c319d39d'
down_revision = 'e6b3a6e3cf01'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url_id', sa.String(50), nullable=False),
        sa.Column('tags', sa.ARRAY(sa.String(50)), nullable=False),
    )


def downgrade():
    op.drop_table('tags')
