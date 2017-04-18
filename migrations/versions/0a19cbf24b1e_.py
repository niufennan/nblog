"""empty message

Revision ID: 0a19cbf24b1e
Revises: 69f19354fb36
Create Date: 2017-03-24 23:45:39.052518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a19cbf24b1e'
down_revision = '69f19354fb36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('lastseen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'lastseen')
    # ### end Alembic commands ###
