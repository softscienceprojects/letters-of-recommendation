"""tags

Revision ID: a1b239ae8a24
Revises: b1eaf15c3463
Create Date: 2020-06-20 00:57:24.978900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b239ae8a24'
down_revision = 'b1eaf15c3463'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('postTags')
    op.add_column('tags', sa.Column('name', sa.String(), nullable=False))
    op.drop_column('tags', 'tag')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('tag', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('tags', 'name')
    op.create_table('postTags',
    sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='postTags_post_id_fkey'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='postTags_tag_id_fkey')
    )
    # ### end Alembic commands ###
