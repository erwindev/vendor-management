"""vendor tables

Revision ID: f40a95457ff1
Revises: eea109e76846
Create Date: 2020-04-03 20:55:31.074395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f40a95457ff1'
down_revision = 'eea109e76846'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('address_type_id', sa.Integer(), nullable=False),
    sa.Column('street1', sa.String(length=100), nullable=True),
    sa.Column('street2', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=100), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('zipcode', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('address_id', 'address_type_id')
    )
    op.create_table('contact',
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('contact_type_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('phone1', sa.String(length=100), nullable=True),
    sa.Column('phone2', sa.String(length=100), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('contact_id', 'contact_type_id')
    )
    op.create_table('vendor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('website', sa.String(length=100), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vendor')
    op.drop_table('contact')
    op.drop_table('address')
    # ### end Alembic commands ###