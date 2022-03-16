"""empty message

Revision ID: 26ae3ceb883a
Revises: c23ae7a8fdd0
Create Date: 2022-03-15 00:41:13.658932

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '26ae3ceb883a'
down_revision = 'c23ae7a8fdd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('total_value', sa.Float(), nullable=False))
    op.add_column('order', sa.Column('total_portage', sa.Float(), nullable=False))
    op.add_column('order', sa.Column('deadline', sa.Integer(), nullable=False))
    op.alter_column('order', 'total',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.add_column('order_product', sa.Column('portage', sa.Float(), nullable=False))
    op.add_column('order_product', sa.Column('deadline', sa.Integer(), nullable=False))
    op.add_column('product', sa.Column('weight', sa.Float(), nullable=False))
    op.add_column('product', sa.Column('length', sa.Float(), nullable=False))
    op.add_column('product', sa.Column('width', sa.Float(), nullable=False))
    op.add_column('product', sa.Column('height', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'height')
    op.drop_column('product', 'width')
    op.drop_column('product', 'length')
    op.drop_column('product', 'weight')
    op.drop_column('order_product', 'deadline')
    op.drop_column('order_product', 'portage')
    op.alter_column('order', 'total',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.drop_column('order', 'deadline')
    op.drop_column('order', 'total_portage')
    op.drop_column('order', 'total_value')
    # ### end Alembic commands ###
