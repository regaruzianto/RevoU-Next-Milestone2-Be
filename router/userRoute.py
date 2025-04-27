from model.userModel import User
from services.auth_service import AuthService
from flask import Blueprint, request, jsonify
from services.uploadimg_service import UploadImageService

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        result = AuthService.register(data)
        status_code = 201 if result.get("status") == "success" else 400

        return jsonify(result),status_code
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }),500
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        result = AuthService.login(data)
        status_code = 201 if result.get("status") == "success" else 400
        return jsonify(result),status_code
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }),500
    
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        result = AuthService.get_user(user_id)

        return jsonify(result), 200 if result.get("status") == 'success' else 400
    except Exception as e:
        return jsonify({
            'status' : 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }),500
    
@user_bp.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        result = AuthService.update_user(user_id,data)

        return jsonify(result), 200 if result.get('status') == 'success' else 400
    except Exception as e:
        return jsonify({
            'status' : 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }),500
    

@user_bp.route('/all', methods=['GET'])
def get_all_user():
    try:
        users = User.query.all()

        user_list = [user.to_dict() for user in users]

        return jsonify({
            'status': 'success',
            'message': 'sukses mengambil user',
            'data': user_list
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan'
        }), 500
    

@user_bp.route('/deleteimage/<int:user_id>', methods=['DELETE'])
def delete_image_profile(user_id):
    try:
        result = UploadImageService.delete_image_profile(user_id=user_id)

        return jsonify(result), 200 if result.get('status') == 'success' else 400
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan'
        }), 500