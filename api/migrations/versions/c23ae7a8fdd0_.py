"""empty message

Revision ID: c23ae7a8fdd0
Revises: 91c6904dbfc2
Create Date: 2022-03-07 19:08:25.463682

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c23ae7a8fdd0'
down_revision = '91c6904dbfc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_product', 'quantity',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('order_product', 'subtotal',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('order_product', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_product', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('order_product', 'subtotal',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('order_product', 'quantity',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
