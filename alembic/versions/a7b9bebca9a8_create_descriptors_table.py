"""create descriptors table

Revision ID: a7b9bebca9a8
Revises: eec1c319d39d
Create Date: 2021-07-05 05:04:14.202232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7b9bebca9a8'
down_revision = 'eec1c319d39d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'descriptors',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url_id', sa.String(50), nullable=False),
        sa.Column('descriptors', sa.ARRAY(sa.String(50)), nullable=False),
    )


def downgrade():
    op.drop_table('descriptors')