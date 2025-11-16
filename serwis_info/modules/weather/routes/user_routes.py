from flask import request, jsonify
from ..db.user_repository import get_user_id, set_default_city

def register_user_routes(bp):

    @bp.route('/api/default_city/<username>', methods=['POST'])
    def set_default(username):
        user_id = get_user_id(username)
        city = request.json.get("city")

        if not city:
            return jsonify({"error": "Brak miasta"}), 400

        set_default_city(user_id, city)
        return jsonify({"message": f"Ustawiono domyślne miasto na {city}"})
