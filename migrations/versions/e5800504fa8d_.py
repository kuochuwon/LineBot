"""empty message

Revision ID: e5800504fa8d
Revises: 8703da144418
Create Date: 2021-04-27 14:26:46.637770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5800504fa8d'
down_revision = '8703da144418'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sd21_Bible',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('locate', sa.String(length=50), nullable=True, comment='經文位置'),
    sa.Column('sentence', sa.Text(), nullable=False, comment='經文內容'),
    sa.Column('comment', sa.Text(), nullable=True, comment='Comment'),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('sd11_users', 'name',
               existing_type=sa.VARCHAR(length=20),
               comment='姓名, 包括團體: ex: 青少契',
               existing_comment='姓名',
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sd11_users', 'name',
               existing_type=sa.VARCHAR(length=20),
               comment='姓名',
               existing_comment='姓名, 包括團體: ex: 青少契',
               existing_nullable=False)
    op.drop_table('sd21_Bible')
    # ### end Alembic commands ###
