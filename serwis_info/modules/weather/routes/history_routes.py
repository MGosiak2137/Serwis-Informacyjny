from flask import Blueprint, jsonify, request
from ..services.history_service import add_city_to_history
from ..db.history_repository import get_history, clear_history, get_top_cities
from ..db.user_repository import get_user_id

history_bp = Blueprint("history", __name__, url_prefix="/weather")

def register_history_routes(app):
    @history_bp.route('/api/history/<username>', methods=['GET'])
    def history(username):
        user_id = get_user_id(username)
        data = get_history(user_id)
        return jsonify([{"city": row[0]} for row in data])

    @history_bp.route('/api/history/<username>', methods=['POST'])
    def history_add(username):
        user_id = get_user_id(username)
        city = request.json.get("city")
        if not city:
            return jsonify({"error": "Brak miasta"}), 400
        add_city_to_history(user_id, city)
        return jsonify({"message": "Dodano do historii"})

    @history_bp.route('/api/history/<username>', methods=['DELETE'])
    def history_delete(username):
        user_id = get_user_id(username)
        clear_history(user_id)
        return jsonify({"message": "Historia została usunięta"})

    @history_bp.route('/api/top_cities/<username>')
    def top_cities(username):
        user_id = get_user_id(username)
        rows = get_top_cities(user_id, 5)
        return jsonify([row[0] for row in rows])
    @history_bp.route('/api/history_last3/<username>')
    def history_last3(username):
        user_id = get_user_id(username)
        data = get_history(user_id)
        last3 = [row[0] for row in data[:3]]  # ostatnie 3
        return jsonify(last3)
