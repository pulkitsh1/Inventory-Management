"""empty message

Revision ID: 5b159b8246aa
Revises: eda5ed4963d6
Create Date: 2024-02-22 12:11:02.642416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b159b8246aa'
down_revision = 'eda5ed4963d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # with op.batch_alter_table('inventory', schema=None) as batch_op:
    #     batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))

    # ### end Alembic commands ###
    pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.drop_column('id')

    # ### end Alembic commands ###
