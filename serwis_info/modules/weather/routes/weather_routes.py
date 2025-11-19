
from flask import Blueprint, jsonify
import requests

weather_api_bp = Blueprint("weather_api", __name__, url_prefix="/weather")

@weather_api_bp.route("/api/simple_weather")
def simple_weather():
    API_KEY = "25ae8c36b22398f35b25584807571f27"

    url = f"https://api.openweathermap.org/data/2.5/weather?q=Warsaw&units=metric&lang=pl&appid={API_KEY}"
    data = requests.get(url).json()

    return jsonify({
        "temp": round(data["main"]["temp"]),
        "desc": data["weather"][0]["description"].capitalize(),
        "icon": data["weather"][0]["icon"]
    })
