"""empty message

Revision ID: c9b9c951bf75
Revises: 70132a6abed2
Create Date: 2024-02-29 10:35:49.970084

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c9b9c951bf75'
down_revision = '70132a6abed2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fname', sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column('lname', sa.String(length=80), nullable=True))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=80), nullable=True))
        batch_op.drop_column('lname')
        batch_op.drop_column('fname')

    # ### end Alembic commands ###
