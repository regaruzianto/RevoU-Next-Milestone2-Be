from flask import Blueprint, jsonify, request
from services.bank_service import BankService
from flask_jwt_extended import jwt_required, get_jwt_identity


bank_bp= Blueprint('bank_bp', __name__)


@bank_bp.route('/<int:user_id>', methods=['GET'])
def get_bank_account(user_id):
    try:
        result = BankService.get_bank_account(user_id)
        return jsonify(result), 200 if result.get('status') == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalaha server',
            'error': str(e)
        })
    
@bank_bp.route('/create', methods=['POST'])
@jwt_required()
def create_bank_account():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        result = BankService.create_bank_account(user_id, data)
        return jsonify(result), 200 if result.get('status') == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500

@bank_bp.route('/delete/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_bank_account(account_id):
    try:
        user_id = get_jwt_identity()

        result = BankService.delete_bank_account(user_id,account_id)
        return jsonify(result), 200 if result.get('status') == 'success' else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500