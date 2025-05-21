from flask import Blueprint, request, jsonify, make_response
from datetime import timedelta
from services.uploadimg_service import UploadImageService
import os
import requests
import base64
from flask_jwt_extended import jwt_required, get_jwt_identity


upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('image')

        if not file:
            return jsonify({
                "status": "error",
                "message": "File image tidak ditemukan di request."
            }), 404

        result = UploadImageService.upload(file, folder_name='/users/profile')

        return jsonify(result), 200 if result.get("status") == "success" else 400

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }),500

@upload_bp.route('/userimage/<int:user_id>', methods=['POST'])
def upload_user_image(user_id):
    try:

        file = request.files.get('image')

        if not file:
            return jsonify({
                "status": "error",
                "message": "File image tidak ditemukan di request."
            }), 404

        result = UploadImageService.upload_image_profile(file, user_id)

        return jsonify(result), 200 if result.get("status") == "success" else 400

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }),500

@upload_bp.route('/userimage/delete/<int:user_id>', methods=['DELETE'])
def delete_user_image(user_id):
    try:
        result = UploadImageService.delete_image_profile(user_id)

        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@upload_bp.route('/productimage/<int:product_id>', methods=['POST'])
def upload_product_image(product_id):
    try:

        file = request.files.get('image')

        if not file:
            return jsonify({
                "status": "error",
                "message": "File image tidak ditemukan di request."
            }), 404

        result = UploadImageService.upload_product_image(product_id,file, folder_name='/products')

        return jsonify(result), 200 if result.get('status') == 'success' else 400
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': "Terjadi kesalahan server"
        }), 500
    
@upload_bp.route('/productimage/delete/<int:product_id>/<string:image_id>', methods=['DELETE'])
def delete_product_image(product_id, file_id):
    try:
        result = UploadImageService.delete_product_image(product_id, file_id)

        return jsonify(result), 200 if result.get('status') == 'success' else 400

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': "Terjadi kesalahan server",
            'error': str(e)
        })
    
@upload_bp.route('/shopimage', methods=['POST'])
@jwt_required()
def upload_shop_image():
    try:

        file = request.files.get('image')
        user_id = get_jwt_identity()

        if not file:
            return jsonify({
                "status": "error",
                "message": "File image tidak ditemukan di request."
            }), 404

        result = UploadImageService.upload_shop_image(file, user_id)

        return jsonify(result), 200 if result.get('status') == 'success' else 400
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': "Terjadi kesalahan server"
        }), 500