"""empty message

Revision ID: dc0be4c8969c
Revises: b7f18279ed4f
Create Date: 2021-04-14 15:06:04.577302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc0be4c8969c'
down_revision = 'b7f18279ed4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sd11_users', sa.Column('user_unique_id', sa.String(length=64), nullable=True, comment='使用者在Line上的unique ID'))
    op.alter_column('sd11_users', 'id',
               existing_type=sa.INTEGER(),
               comment='流水號',
               existing_comment='使用者在Line上的unique ID',
               autoincrement=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sd11_users', 'id',
               existing_type=sa.INTEGER(),
               comment='使用者在Line上的unique ID',
               existing_comment='流水號',
               autoincrement=True)
    op.drop_column('sd11_users', 'user_unique_id')
    # ### end Alembic commands ###