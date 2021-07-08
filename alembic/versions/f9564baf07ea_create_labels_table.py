"""create labels table

Revision ID: f9564baf07ea
Revises: a7b9bebca9a8
Create Date: 2021-07-05 05:06:25.184669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9564baf07ea'
down_revision = 'a7b9bebca9a8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'labels',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url_id', sa.String(50), nullable=False),
        sa.Column('black', sa.Boolean, nullable=False),
        sa.Column('women', sa.Boolean, nullable=False),
        sa.Column('lgbtq', sa.Boolean, nullable=False),
        sa.Column('veteran', sa.Boolean, nullable=False),

    )


def downgrade():
    op.drop_table('labels')