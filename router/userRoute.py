from model.userModel import User
from services.auth_service import AuthService
from flask import Blueprint, request, jsonify

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
