from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from ..db.eco_preferences_repository import get_preferences, update_preferences
import yfinance as yf
import re

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
    return render_template("nav_foot_eco.html", title="Moduł ekonomiczne")

@main_eco_bp.route("/get-preferences", methods=["GET"])
@login_required
def get_prefs():
    try:
        prefs = get_preferences(current_user.id)
        return jsonify(prefs)
    except Exception as e:
        print(f"Error in get-preferences: {e}")
        return jsonify({"error": str(e)}), 500

@main_eco_bp.route("/update-preferences", methods=["PUT"])
@login_required
def update_prefs():
    try:
        data = request.json
        update_preferences(
            current_user.id,
            favorite_actions=data.get("favorite_actions"),
            currencies=data.get("currencies"),
            search_history=data.get("search_history")
        )
        prefs = get_preferences(current_user.id)
        return jsonify(prefs)
    except Exception as e:
        print(f"Error in update-preferences: {e}")
        return jsonify({"error": str(e)}), 500

@main_eco_bp.route("/api/price/<symbol>", methods=["GET"])
def get_price(symbol):
    """Pobierz aktualną cenę i zmianę dla symbolu"""
    try:
        price_data = get_symbol_price(symbol)
        if price_data:
            return jsonify(price_data)
        return jsonify({"error": "Nie znaleziono symbolu"}), 404
    except Exception as e:
        print(f"Error getting price for {symbol}: {e}")
        return jsonify({"error": str(e)}), 500

def get_symbol_price(symbol):
    """Pobierz cenę z API (np. yfinance)"""
    try:
        match = re.search(r'\(([^)]+)\)', symbol)
        if match:
            symbol = match.group(1)
        
        data = yf.Ticker(symbol)
        hist = data.history(period="2d")
        
        # Pobierz walutę z info
        currency = "USD"
        try:
            info = data.info
            if 'currency' in info:
                currency = info['currency']
        except:
            pass
        
        if len(hist) < 2:
            return {
                "price": 0.00,
                "change": 0.00,
                "currency": currency,
                "status": "no_data"
            }
        
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        change_percent = ((current_price - prev_price) / prev_price) * 100
        
        return {
            "price": round(float(current_price), 2),
            "change": round(change_percent, 2),
            "currency": currency
        }
    except Exception as e:
        print(f"Error fetching price data for {symbol}: {e}")
        # Zwróć dummy dane zamiast None
        return {
            "price": 0.00,
            "change": 0.00,
            "currency": "USD",
            "status": "error",
            "message": str(e)
        }