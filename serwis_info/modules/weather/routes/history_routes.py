from flask import jsonify, request
from ..services.history_service import add_city_to_history
from ..db.history_repository import get_history, clear_history, get_top_cities
from ..db.user_repository import get_user_id

def register_history_routes(bp):

    @bp.route('/api/history/<username>', methods=['GET'])
    def history(username):
        user_id = get_user_id(username)
        data = get_history(user_id)
        return jsonify([{"city": row[0]} for row in data])

    @bp.route('/api/history/<username>', methods=['POST'])
    def history_add(username):
        user_id = get_user_id(username)
        city = request.json.get("city")

        if not city:
            return jsonify({"error": "Brak miasta"}), 400

        add_city_to_history(user_id, city)
        return jsonify({"message": "Dodano do historii"})

    @bp.route('/api/history/<username>', methods=['DELETE'])
    def history_delete(username):
        user_id = get_user_id(username)
        clear_history(user_id)
        return jsonify({"message": "Historia została usunięta"})

    @bp.route('/api/top_cities/<username>')
    def top_cities(username):
        limit = int(request.args.get("limit", 5))
        user_id = get_user_id(username)
        rows = get_top_cities(user_id, limit)
        return jsonify([row[0] for row in rows])
