from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import requests
from ..db.repository import get_user_preferences, update_user_preferences
from ..db.connection import SessionLocal
from sqlalchemy.exc import OperationalError

main_eco_bp = Blueprint(
    "main_eco",
    __name__,
    url_prefix="/main_eco",
    template_folder="../templates",
    static_folder="../static"
)

@main_eco_bp.route("/main_eco", methods=["GET"])
@login_required
def main():
    prefs = None
    try:
        db = SessionLocal()
        prefs = get_user_preferences(db, current_user.id)
        db.close()
    except OperationalError:
        prefs = None
    
    return render_template("nav_foot_eco.html", title="Moduł ekonomiczne", preferences=prefs)

@main_eco_bp.route("/get-preferences", methods=["GET"])
@login_required
def get_preferences():
    try:
        db = SessionLocal()
        prefs = get_user_preferences(db, current_user.id)
        db.close()
        if not prefs:
            return jsonify({"error": "Preferencje nie znalezione"}), 404
        return jsonify({
            "favorite_actions": prefs.favorite_actions,
            "currencies": prefs.currencies,
            "search_history": prefs.search_history
        })
    except OperationalError:
        return jsonify({"error": "Baza danych niedostępna"}), 503

@main_eco_bp.route("/update-preferences", methods=["PUT"])
@login_required
def update_preferences_route():
    try:
        db = SessionLocal()
        data = request.json
        prefs = update_user_preferences(
            db,
            current_user.id,
            favorite_actions=data.get("favorite_actions"),
            currencies=data.get("currencies"),
            search_history=data.get("search_history")
        )
        db.close()
        return jsonify({
            "favorite_actions": prefs.favorite_actions,
            "currencies": prefs.currencies,
            "search_history": prefs.search_history
        })
    except OperationalError:
        return jsonify({"error": "Baza danych niedostępna"}), 503