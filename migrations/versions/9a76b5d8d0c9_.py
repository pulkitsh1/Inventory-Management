"""empty message

Revision ID: 9a76b5d8d0c9
Revises: 2b2968e8e395
Create Date: 2024-02-29 11:45:23.758989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a76b5d8d0c9'
down_revision = '2b2968e8e395'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assigned', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assigned', schema=None) as batch_op:
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###
