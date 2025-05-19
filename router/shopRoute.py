from model.shopModel import Shop
from services.shop_service import ShopService
from flask import Blueprint, request, jsonify
from schemas.shop_schema import ShopCreateSchema

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
def create_shop():
    try:
        data = request.get_json()
        result = ShopService.create_shop(data)
        return jsonify(result), 201 if result.get('status') == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@shop_bp.route('/update/<int:shop_id>', methods=['PUT'])
def update_shop(shop_id):
    try:
        data = request.get_json()
        result = ShopService.update_shop(shop_id, data)
        return jsonify(result), 200 if result.get('status') == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500