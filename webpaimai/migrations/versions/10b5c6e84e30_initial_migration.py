"""Initial migration.

Revision ID: 10b5c6e84e30
Revises: 
Create Date: 2025-01-13 13:53:39.528896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10b5c6e84e30'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_permission',
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.Column('permission_name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('permission_id')
    )
    op.create_table('goods',
    sa.Column('goods_id', sa.Integer(), nullable=False),
    sa.Column('goods_name', sa.String(length=100), nullable=False),
    sa.Column('goods_description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=True),
    sa.Column('release_time', sa.DateTime(), nullable=True),
    sa.Column('image', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['seller_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('goods_id')
    )
    op.create_table('auction',
    sa.Column('auction_id', sa.Integer(), nullable=False),
    sa.Column('starting_price', sa.Float(), nullable=False),
    sa.Column('minimum_increment', sa.Float(), nullable=False),
    sa.Column('reserve_price', sa.Float(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('time_long', sa.Integer(), nullable=True),
    sa.Column('goods_id', sa.Integer(), nullable=True),
    sa.Column('seller_now', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['goods_id'], ['goods.goods_id'], ),
    sa.ForeignKeyConstraint(['seller_now'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('auction_id')
    )
    op.create_table('bid',
    sa.Column('bid_id', sa.Integer(), nullable=False),
    sa.Column('bid_amount', sa.Float(), nullable=False),
    sa.Column('bid_time', sa.DateTime(), nullable=True),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.Column('auction_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['auction_id'], ['auction.auction_id'], ),
    sa.ForeignKeyConstraint(['buyer_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('bid_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bid')
    op.drop_table('auction')
    op.drop_table('goods')
    op.drop_table('user_permission')
    op.drop_table('user')
    # ### end Alembic commands ###