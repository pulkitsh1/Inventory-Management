"""empty message

Revision ID: 84bedb9d2732
Revises: a2d65dc59d2a
Create Date: 2024-02-22 12:27:26.589947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84bedb9d2732'
down_revision = 'a2d65dc59d2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.drop_column('id')

    # ### end Alembic commands ###