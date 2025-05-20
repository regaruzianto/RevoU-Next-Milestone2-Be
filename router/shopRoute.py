from model.shopModel import Shop
from services.shop_service import ShopService
from flask import Blueprint, request, jsonify
from schemas.shop_schema import ShopCreateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

shop_bp = Blueprint('shop_bp', __name__)

@shop_bp.route('/shops', methods=['GET'])
def get_all_shops():
    try:
        result = ShopService.get_all_shops()
        return jsonify(result), 200 if result.get('status') == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500

@shop_bp.route('/shop/<int:shop_id>', methods=['GET'])
def get_shop_by_id(shop_id):
    try:
        result = ShopService.get_shop_by_id(shop_id)
        return jsonify(result), 200 if result.get('status') == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@shop_bp.route('/shop/<string:shop_name>', methods=['GET'])
def get_shop_by_name(shop_name):
    try:
        result = ShopService.get_shop_by_name(shop_name)
        return jsonify(result), 200 if result.get('status') == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500


@shop_bp.route('/shop', methods=['POST'])
@jwt_required()
def create_shop():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        result = ShopService.create_shop(user_id,data)
        return jsonify(result), 201 if result.get('status') == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@shop_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_shop():
    try:
        user_id = get_jwt_identity()

        data = request.get_json()
        result = ShopService.update_shop(user_id, data)
        return jsonify(result), 200 if result.get('status') == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500