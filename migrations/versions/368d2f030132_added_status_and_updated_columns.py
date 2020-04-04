"""added status and updated columns

Revision ID: 368d2f030132
Revises: c7caf3a32b0e
Create Date: 2020-04-04 19:04:59.295556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '368d2f030132'
down_revision = 'c7caf3a32b0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('status', sa.String(length=3), nullable=True))
    op.add_column('contact', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('product', sa.Column('status', sa.String(length=3), nullable=True))
    op.add_column('user', sa.Column('status', sa.String(length=3), nullable=True))
    op.add_column('user', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('vendor', sa.Column('status', sa.String(length=3), nullable=True))
    op.add_column('vendor', sa.Column('updated_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vendor', 'updated_date')
    op.drop_column('vendor', 'status')
    op.drop_column('user', 'updated_date')
    op.drop_column('user', 'status')
    op.drop_column('product', 'status')
    op.drop_column('contact', 'updated_date')
    op.drop_column('contact', 'status')
    # ### end Alembic commands ###