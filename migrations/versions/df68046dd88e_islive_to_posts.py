"""isLive to Posts

Revision ID: df68046dd88e
Revises: ff627bdd6649
Create Date: 2020-07-04 13:12:08.983343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df68046dd88e'
down_revision = 'ff627bdd6649'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('isLive', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'isLive')
    # ### end Alembic commands ###
