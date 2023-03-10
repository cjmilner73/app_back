"""empty message

Revision ID: e70938936286
Revises: 2ffe83ee752a
Create Date: 2021-09-01 21:48:03.860932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e70938936286'
down_revision = '2ffe83ee752a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('holding', sa.Column('day_change', sa.DECIMAL(asdecimal=False), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('holding', 'day_change')
    # ### end Alembic commands ###
