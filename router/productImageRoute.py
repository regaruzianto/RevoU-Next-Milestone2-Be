from services.productImage_service import ProductImageService
from flask import Blueprint, jsonify, request

productImage_bp = Blueprint('productImage_bp', __name__)

@productImage_bp.route('/', methods=['GET'])
def get_all_productImages():
    try:
        result = ProductImageService.get_all_productImages()
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@productImage_bp.route('/<int:product_id>', methods=['GET'])
def get_product_images(product_id):
    try:
        result = ProductImageService.get_product_images(product_id)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500