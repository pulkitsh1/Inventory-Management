"""empty message

Revision ID: a2d65dc59d2a
Revises: 5b159b8246aa
Create Date: 2024-02-22 12:13:47.716726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2d65dc59d2a'
down_revision = '5b159b8246aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # with op.batch_alter_table('inventory', schema=None) as batch_op:
        # batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))

    # ### end Alembic commands ###
    pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.drop_column('id')

    # ### end Alembic commands ###
