from services.product_service import ProductService
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

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
@jwt_required()
def create_product():
    try:
        user_id = get_jwt_identity()

        data = request.get_json()
        result = ProductService.create_product(user_id,data)
        return jsonify(result), 201 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500


@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        user_id = get_jwt_identity()

        data = request.get_json()
        result = ProductService.update_product(user_id,product_id, data)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    try:
        user_id = get_jwt_identity()    

        result = ProductService.delete_product(user_id,product_id)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500


@product_bp.route('/byuserid', methods=['GET'])
def get_products_by_userID():
    try:
        # Get query parameters
        query_params = request.args.to_dict()
        result = ProductService.get_products_by_userID(query_params)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
