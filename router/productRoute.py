from services.product_service import ProductService
from flask import Blueprint, request, jsonify


product_bp = Blueprint('product_bp', __name__) 


@product_bp.route('/', methods=['GET'])
def get_products():
    try:
        # Get query parameters
        query_params = request.args.to_dict()
        result = ProductService.get_products(query_params)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        result = ProductService.get_product_by_id(product_id)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@product_bp.route('/', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        result = ProductService.create_product(data)
        return jsonify(result), 201 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500


@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.get_json()
        result = ProductService.update_product(product_id, data)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        result = ProductService.delete_product(product_id)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500