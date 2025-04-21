from services.order_service import OrderService
from flask import Blueprint, request, jsonify
from model.orderModel import Order,OrderItem

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/orders/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        result = OrderService.get_orders(user_id, page, per_page)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 400
    
@order_bp.route('/orders/<int:user_id>/<int:order_id>', methods=['GET'])
def get_order_by_id(user_id,order_id):
    try:
        result = OrderService.get_order_by_id(user_id,order_id)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 400
    
@order_bp.route('/create/<int:user_id>', methods=['POST'])
def create_order(user_id):
    try:
        data = request.get_json()
        result = OrderService.create_order(user_id,data)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 400
    
@order_bp.route('/cancel/<int:user_id>/<int:order_id>', methods=['DELETE']) 
def cancel_order(user_id,order_id):
    try:
        result = OrderService.cancel_order(user_id,order_id)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 400
    
@order_bp.route('/', methods=['GET']) 
def all_order():
    try:
        result = Order.query.all()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': 'eror',
            'message': str(e)
        })