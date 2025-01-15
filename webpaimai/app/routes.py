from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Goods, Auction, Bid
from datetime import datetime
from datetime import timedelta

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return jsonify({"message": "Welcome to the Flask app!"})


@main.route('/favicon.ico')
def favicon():
    return '', 204


@main.route('/auction', methods=['POST'])
def create_auction():
    data = request.get_json()

    starting_price = data.get('starting_price')
    minimum_increment = data.get('minimum_increment')
    reserve_price = data.get('reserve_price')
    start_time = data.get('start_time')
    time_long = data.get('time_long')
    goods_id = data.get('goods_id')
    user_id = data.get('user_id')

    try:
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid date format, expected %Y-%m-%d %H:%M'}), 400

    new_auction = Auction(
        starting_price=starting_price,
        minimum_increment=minimum_increment,
        reserve_price=reserve_price,
        start_time=start_time,
        time_long=time_long,
        goods_id=goods_id,
        user_id=user_id
    )

    try:
        db.session.add(new_auction)
        db.session.commit()
        return jsonify({'auction_id': new_auction.auction_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 409

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(f"注册时发生错误: {e}")
        return jsonify({"error": "注册失败，请稍后重试"}), 500
@main.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({"error": "Invalid username or password"}), 401

    user_data = {
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role,

    }

    return jsonify({"message": "Login successful", "user": user_data}), 200

@main.route('/goods', methods=['POST'])
def create_goods():
    data = request.get_json()

    goods_name = data.get('goods_name')
    price = data.get('price')
    seller_id = data.get('seller_id')

    if not goods_name or not price or not seller_id:
        return jsonify({'error': 'goods_name, price, and seller_id are required'}), 400

    try:

        new_goods = Goods(
            goods_name=goods_name,
            price=price,
            seller_id=seller_id,
            release_time=datetime.utcnow()
        )

        db.session.add(new_goods)
        db.session.commit()

        return jsonify({'goods_id': new_goods.goods_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/all_goods', methods=['GET'])
def get_all_goods():
    goods_list = Goods.query.all()
    result = []
    for goods in goods_list:
        result.append({
            "id": goods.goods_id,
            "name": goods.goods_name,
            "price": goods.price,
            "seller_id": goods.seller_id
        })
    return jsonify(result), 200


@main.route('/bid', methods=['POST'])
def place_bid():

    data = request.json
    auction_id = data.get('auction_id')
    buyer_id = data.get('buyer_id')
    bid_amount = data.get('bid_amount')

    auction = Auction.query.get(auction_id)
    if not auction:
        return jsonify({"error": "Auction not found"}), 404

    if bid_amount <= auction.current_price:
        return jsonify({"error": "Bid amount must be greater than current price"}), 400

    auction.current_price = bid_amount
    db.session.add(auction)

    bid = Bid(
        auction_id=auction_id,
        buyer_id=buyer_id,
        bid_amount=bid_amount,
        bid_time=datetime.utcnow()
    )
    db.session.add(bid)
    db.session.commit()

    return jsonify({"message": "Bid placed successfully", "current_price": auction.current_price})


@main.route('/auction/<int:auction_id>', methods=['GET'])
def get_auction_detail(auction_id):
    auction = Auction.query.get(auction_id)
    if not auction:
        return jsonify({"error": "Auction not found"}), 404

    goods = Goods.query.get(auction.goods_id)
    if not goods:
        return jsonify({"error": "Goods not found"}), 404

    current_price = auction.starting_price
    bids = Bid.query.filter_by(auction_id=auction_id).all()
    if bids:
        current_price = max(bid.bid_amount for bid in bids)

    auction_detail = {
        "auction_id": auction.auction_id,
        "goods_name": goods.goods_name,
        "goods_description": goods.goods_description,
        "starting_price": auction.starting_price,
        "current_price": current_price,
        "minimum_increment": auction.minimum_increment,
        "reserve_price": auction.reserve_price,
        "time_long": auction.time_long,
        "start_time": auction.start_time,
        "end_time": auction.start_time + timedelta(minutes=auction.time_long)
    }

    return jsonify(auction_detail)
@main.route('/auction/<int:auction_id>/close', methods=['POST'])
def close_auction(auction_id):
    auction = Auction.query.get(auction_id)
    if not auction:
        return jsonify({"error": "Auction not found"}), 404

    highest_bid = Bid.query.filter_by(auction_id=auction_id).order_by(Bid.bid_amount.desc()).first()
    if not highest_bid:
        return jsonify({"message": "No bids placed. Auction closed without a winner."}), 200

    return jsonify({
        "message": "Auction closed successfully",
        "winner": highest_bid.buyer_id,
        "winning_bid": highest_bid.bid_amount
    }), 200


@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role
        })
    return jsonify(result), 200
@main.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')  # 默认角色为 'user'

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User added successfully", "user_id": new_user.user_id}), 201

    except Exception as e:
        print(f"Error adding user: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@main.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role
    }), 200


@main.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    user.username = data.get('username', user.username)
    user.password = data.get('password', user.password)
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200


@main.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        print(f"Error while deleting user: {e}")
        return jsonify({"error": "Internal server error"}), 500


@main.route('/goods/<int:goods_id>', methods=['GET'])
def get_good(goods_id):
    good = Goods.query.get(goods_id)
    if not good:
        return jsonify({"error": "Good not found"}), 404
    return jsonify({
        "goods_id": good.goods_id,
        "goods_name": good.goods_name,
        "price": good.price,
        "seller_id": good.seller_id
    }), 200


@main.route('/goods/<int:goods_id>', methods=['PUT'])
def update_goods(goods_id):
    good = Goods.query.get(goods_id)
    if not good:
        return jsonify({"error": "Good not found"}), 404
    data = request.json
    good.goods_name = data.get('goods_name', good.goods_name)
    good.price = data.get('price', good.price)
    good.seller_id = data.get('seller_id', good.seller_id)
    db.session.commit()
    return jsonify({"message": "Good updated successfully"}), 200

@main.route('/goods/<int:goods_id>', methods=['DELETE'])
def delete_goods(goods_id):
    good = Goods.query.get(goods_id)
    if not good:
        return jsonify({"error": "Good not found"}), 404
    db.session.delete(good)
    db.session.commit()
    return jsonify({"message": "Good deleted successfully"}), 200