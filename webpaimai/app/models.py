from sqlalchemy import CheckConstraint

from app import db

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='普通用户', server_default='普通用户')
    __table_args__ = (
        CheckConstraint('role IN (\'普通用户\', \'超级用户\')', name='check_role'),
    )

class UserPermission(db.Model):
    __tablename__ = 'user_permission'
    permission_id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(80), nullable=False)

class Goods(db.Model):
    __tablename__ = 'goods'
    goods_id = db.Column(db.Integer, primary_key=True)
    goods_name = db.Column(db.String(100), nullable=False)
    goods_description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    release_time = db.Column(db.DateTime)
    image = db.Column(db.String(200))

class Auction(db.Model):
    __tablename__ = 'auction'
    auction_id = db.Column(db.Integer, primary_key=True)
    starting_price = db.Column(db.Float, nullable=False)
    minimum_increment = db.Column(db.Float, nullable=False)
    reserve_price = db.Column(db.Float)
    start_time = db.Column(db.DateTime, nullable=False)
    time_long = db.Column(db.Integer, nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.goods_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
class Bid(db.Model):
    __tablename__ = 'bid'
    bid_id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, nullable=False)
    bid_time = db.Column(db.DateTime)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.auction_id'))
