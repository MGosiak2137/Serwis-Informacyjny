from flask import request, jsonify, Blueprint
from ..db.user_repository import get_user_id, set_default_city, get_default_city, clear_default_city

user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/user",
    template_folder="../templates",
    static_folder="../static"
)



@user_bp.route('/api/default_city/<username>', methods=['POST'])
def set_default(username):
    user_id = get_user_id(username)
    city = request.json.get("city")

    if not city:
        return jsonify({"error": "Brak miasta"}), 400

    set_default_city(user_id, city)
    return jsonify({"message": f"Ustawiono domyślne miasto na {city}"})

@user_bp.route('/api/default_city/<username>', methods=['GET'])
def get_default(username):
    user_id = get_user_id(username)
    city = get_default_city(user_id)
    return jsonify({"default_city": city})
    

@user_bp.route('/api/default_city/<username>', methods=['DELETE'])
def delete_default(username):
    user_id = get_user_id(username)
    clear_default_city(user_id)
    return jsonify({"message": "Domyślne miasto usunięte"})