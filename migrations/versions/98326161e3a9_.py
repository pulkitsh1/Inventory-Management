"""empty message

Revision ID: 98326161e3a9
Revises: 4b2c6a38fd8d
Create Date: 2024-02-13 11:31:14.458544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98326161e3a9'
down_revision = '4b2c6a38fd8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_type', sa.String(length=120), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('product_type')

    # ### end Alembic commands ###
