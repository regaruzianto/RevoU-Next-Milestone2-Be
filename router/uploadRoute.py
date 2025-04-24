from flask import Blueprint, request, jsonify, make_response
from datetime import timedelta
from services.uploadimg_service import UploadImageService
import os
import requests
import base64


upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('image')

        if not file:
            return jsonify({
                "status": "error",
                "message": "File image tidak ditemukan di request."
            }), 400

        result = UploadImageService.upload(file, folder_name='/users/profile')

        return jsonify(result), 200 if result.get("status") == "success" else 400

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        })

@upload_bp.route('/userimage/<int:user_id>', methods=['POST'])
def upload_user_image(user_id):
    try:

        file = request.files.get('image')

        if not file:
            return jsonify({
                "status": "error",
                "message": "File image tidak ditemukan di request."
            }), 400

        result = UploadImageService.upload_image_profile(file, user_id)

        return jsonify(result), 200 if result.get("status") == "success" else 400

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        })

