from flask import Blueprint, request, jsonify
from ..services.history_service import add_city_to_history, fetch_history, clear_user_history

history_bp = Blueprint("history_bp", __name__)

@history_bp.route("/api/history/<username>", methods=["GET"])
def history(username):
    data = fetch_history(username)
    return jsonify(data)

# @history_bp.route("/api/history_last3/<username>", methods=["GET"])
# def history_last3(username):
#     data = fetch_last3(username)
#     return jsonify(data)

@history_bp.route("/api/history/<username>", methods=["POST"])
def history_add(username):
    city = request.json.get("city")
    if not city:
        return jsonify({"error": "city not provided"}), 400
    add_city_to_history(username, city)
    return jsonify({"status": "ok"})

@history_bp.route("/api/history/<username>", methods=["DELETE"])
def history_delete(username):
    clear_user_history(username)
    return jsonify({"status": "ok"})
