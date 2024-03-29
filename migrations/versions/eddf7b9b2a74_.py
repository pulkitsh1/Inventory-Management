"""empty message

Revision ID: eddf7b9b2a74
Revises: 94723e529a47
Create Date: 2024-03-19 12:38:21.184304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eddf7b9b2a74'
down_revision = '94723e529a47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('attachments_count', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions_model', schema=None) as batch_op:
        batch_op.drop_column('attachments_count')

    # ### end Alembic commands ###
