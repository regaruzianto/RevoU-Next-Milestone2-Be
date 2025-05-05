from services.visitor_service import VisitorService
from flask import Blueprint, jsonify, request

visitor_bp = Blueprint('visitor_bp', __name__)

@visitor_bp.route('/visitors', methods=['GET'])
def get_visitors_daily():
    try:
        query_params = request.args.to_dict()
        result = VisitorService.get_visitors_daily(query_params)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@visitor_bp.route('/track/<int:user_id>', methods=['POST'])
def track_visitor(user_id):
    try:

        result = VisitorService.track_visitor(user_id)
        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500
    
@visitor_bp.route('/count', methods=['GET'])
def count_visitor():
    try:
        query_params = request.args.to_dict()
        result = VisitorService.count_visitor(query_params)

        return jsonify(result), 200 if result.get("status") == "success" else 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server',
            'error': str(e)
        }), 500