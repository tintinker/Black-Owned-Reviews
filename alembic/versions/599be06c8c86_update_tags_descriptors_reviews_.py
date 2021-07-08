"""update tags,descriptors,reviews,suggestion

Revision ID: 599be06c8c86
Revises: 951928389e0c
Create Date: 2021-07-08 10:42:23.491657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '599be06c8c86'
down_revision = '951928389e0c'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('tags', 'tags')
    op.add_column('tags', sa.Column('tags', sa.ARRAY(sa.String(100)), nullable=True))

    op.drop_column('descriptors', 'descriptors')
    op.add_column('descriptors', sa.Column('descriptors', sa.ARRAY(sa.String(100)), nullable=True))
    
    op.add_column('followed_suggestion', sa.Column('was_ad', sa.Boolean))
    
    op.drop_column('reviews', 'text')
    op.add_column('reviews', sa.Column('text', sa.String(1250), nullable=True))



def downgrade():
    pass
