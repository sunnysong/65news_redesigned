"""empty message

Revision ID: b0a6842f02
Revises: 476b7f9f4853
Create Date: 2015-07-21 21:20:51.197795

"""

# revision identifiers, used by Alembic.
revision = 'b0a6842f02'
down_revision = '476b7f9f4853'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('recommended', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_posts_category'), 'posts', ['category'], unique=False)
    op.create_index(op.f('ix_posts_likes'), 'posts', ['likes'], unique=False)
    op.create_index(op.f('ix_posts_recommended'), 'posts', ['recommended'], unique=False)
    op.create_index(op.f('ix_posts_title'), 'posts', ['title'], unique=True)
    op.drop_constraint(u'posts_title_key', 'posts', type_='unique')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(u'posts_title_key', 'posts', ['title'])
    op.drop_index(op.f('ix_posts_title'), table_name='posts')
    op.drop_index(op.f('ix_posts_recommended'), table_name='posts')
    op.drop_index(op.f('ix_posts_likes'), table_name='posts')
    op.drop_index(op.f('ix_posts_category'), table_name='posts')
    op.drop_column('posts', 'recommended')
    ### end Alembic commands ###