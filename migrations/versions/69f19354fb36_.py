"""empty message

Revision ID: 69f19354fb36
Revises: e8394ee5ec05
Create Date: 2017-03-24 23:26:59.376476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69f19354fb36'
down_revision = 'e8394ee5ec05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('createtime', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'createtime')
    # ### end Alembic commands ###