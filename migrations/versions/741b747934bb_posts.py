"""posts

Revision ID: 741b747934bb
Revises: 205de9a3be34
Create Date: 2020-06-28 10:18:17.979075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '741b747934bb'
down_revision = '205de9a3be34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datePosted', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###