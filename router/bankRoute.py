from flask import Blueprint, jsonify, request
from services.bank_service import BankService


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