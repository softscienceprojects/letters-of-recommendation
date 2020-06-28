"""followers

Revision ID: 205de9a3be34
Revises: b085ba6d5f82
Create Date: 2020-06-28 10:16:59.031817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '205de9a3be34'
down_revision = 'b085ba6d5f82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###