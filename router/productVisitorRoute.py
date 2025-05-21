from services.productVisitor_service import ProductVisitorService
from flask import Blueprint, jsonify, request



productVisitor_bp = Blueprint('productVisitor_bp', __name__)

@productVisitor_bp.route('/', methods=['GET'])
def get_product_visitors():
    try:
        query_params = request.args.to_dict()
        result = ProductVisitorService.get_product_visitors_daily(query_params)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@productVisitor_bp.route('/track/<int:user_id>/<int:product_id>', methods=['POST'])
def track_product_visitor(user_id, product_id):
    try:

        result = ProductVisitorService.track_product_visitors(user_id, product_id)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    

@productVisitor_bp.route('/shop/track/<int:user_id>/<int:shop_id>', methods=['POST'])
def track_shop_visitor(user_id, shop_id):
    try:

        result = ProductVisitorService.track_shop_visitors(user_id, shop_id)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    

@productVisitor_bp.route('/shop', methods=['GET'])
def get_shop_visitors():
    try:
        query_params = request.args.to_dict()
        result = ProductVisitorService.get_shop_visitors(query_params)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500