"""Image table

Revision ID: ff627bdd6649
Revises: fffbfed68b59
Create Date: 2020-07-04 11:57:05.320543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff627bdd6649'
down_revision = 'fffbfed68b59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asset_id', sa.String(), nullable=True),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('public_id', sa.String(), nullable=False),
    sa.Column('format', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###
