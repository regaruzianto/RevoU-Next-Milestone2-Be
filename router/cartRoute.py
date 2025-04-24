from services.cart_service import CartService
from flask import Blueprint, jsonify, request


cart_bp = Blueprint('cart_bp',__name__)


@cart_bp.route('/<int:user_id>',methods=['GET'])
def get_cart(user_id):
    try:
        result = CartService.get_cart(user_id)
        return jsonify(result), 200 if result.get("status") == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@cart_bp.route('/<int:user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    try:
        data = request.get_json()
        result = CartService.add_to_cart(user_id,data)
        return jsonify(result), 200 if result.get("status") == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@cart_bp.route('/update/<int:user_id>/<int:cart_id>', methods=['PUT'])
def update_cart_item(user_id, cart_id):
    try:
        data = request.get_json()
        result = CartService.update_cart_item(user_id,cart_id,data)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message' : "Terjadi kesalahan server",
            'error': str(e)
        }),500
    
@cart_bp.route('/remove/<int:user_id>/<int:cart_id>', methods=['DELETE'])
def remove_from_cart(user_id, cart_id):
    try: 
        result = CartService.remove_from_cart(user_id,cart_id)
        return jsonify(result),200 if result.get("status") == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }),500
    
@cart_bp.route('/clear/<int:user_id>', methods=['DELETE'])
def clear_cart(user_id):
    try:
        result = CartService.clear_cart(user_id)
        return jsonify(result),200 if result.get("status") == 'success' else 400
    except Exception as e:
                return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }),500
    

