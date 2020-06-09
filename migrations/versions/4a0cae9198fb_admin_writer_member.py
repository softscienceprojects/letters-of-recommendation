"""admin/writer/member

Revision ID: 4a0cae9198fb
Revises: 9d6c44e3e262
Create Date: 2020-06-09 21:09:08.306699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a0cae9198fb'
down_revision = '9d6c44e3e262'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('isAdmin', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('isMember', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('isWriter', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'isWriter')
    op.drop_column('users', 'isMember')
    op.drop_column('users', 'isAdmin')
    # ### end Alembic commands ###
