"""create suggestion table

Revision ID: 35df26f7c8bc
Revises: f9564baf07ea
Create Date: 2021-07-05 05:08:05.988405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35df26f7c8bc'
down_revision = 'f9564baf07ea'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'followed_suggestion',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url_id', sa.String(50), nullable=False),
        sa.Column('followed', sa.Boolean, nullable=False),

    )


def downgrade():
    op.drop_table('followed_suggestion')
