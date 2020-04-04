"""removed address and merged with contact

Revision ID: c7caf3a32b0e
Revises: 62a98497d8ad
Create Date: 2020-04-04 17:11:44.740053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7caf3a32b0e'
down_revision = '62a98497d8ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('address')
    op.add_column('contact', sa.Column('city', sa.String(length=100), nullable=True))
    op.add_column('contact', sa.Column('country', sa.String(length=100), nullable=True))
    op.add_column('contact', sa.Column('state', sa.String(length=100), nullable=True))
    op.add_column('contact', sa.Column('street1', sa.String(length=100), nullable=True))
    op.add_column('contact', sa.Column('street2', sa.String(length=100), nullable=True))
    op.add_column('contact', sa.Column('zipcode', sa.String(length=15), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contact', 'zipcode')
    op.drop_column('contact', 'street2')
    op.drop_column('contact', 'street1')
    op.drop_column('contact', 'state')
    op.drop_column('contact', 'country')
    op.drop_column('contact', 'city')
    op.create_table('address',
    sa.Column('address_id', sa.INTEGER(), nullable=False),
    sa.Column('address_type_id', sa.INTEGER(), nullable=False),
    sa.Column('street1', sa.VARCHAR(length=100), nullable=True),
    sa.Column('street2', sa.VARCHAR(length=100), nullable=True),
    sa.Column('city', sa.VARCHAR(length=100), nullable=True),
    sa.Column('state', sa.VARCHAR(length=100), nullable=True),
    sa.Column('country', sa.VARCHAR(length=100), nullable=True),
    sa.Column('zipcode', sa.VARCHAR(length=15), nullable=True),
    sa.PrimaryKeyConstraint('address_id', 'address_type_id')
    )
    # ### end Alembic commands ###