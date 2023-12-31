"""empty message

Revision ID: f0cfa762d758
Revises: 11dfa7923aa5
Create Date: 2023-12-21 13:29:12.675735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0cfa762d758'
down_revision = '11dfa7923aa5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('link_geoposition', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('link_geoposition')

    # ### end Alembic commands ###
