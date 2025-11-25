
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

@weather_api_bp.route("/api/forecast")
def weather_forecast():
    API_KEY = "25ae8c36b22398f35b25584807571f27"
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Warsaw&units=metric&lang=pl&appid={API_KEY}"

    data = requests.get(url).json()

    # OpenWeather zwraca prognozy co 3h → wybieramy te z godziny 12:00 dla kolejnych 3 dni
    forecast = []
    added_days = set()

    for item in data["list"]:
        dt_txt = item["dt_txt"]  # np. 2025-01-12 12:00:00

        if "12:00:00" in dt_txt:
            day = dt_txt.split(" ")[0]
            if day not in added_days:
                added_days.add(day)
                forecast.append({
                    "date": day,
                    "temp": round(item["main"]["temp"]),
                    "desc": item["weather"][0]["description"].capitalize(),
                    "icon": item["weather"][0]["icon"]
                })
            if len(forecast) == 3:
                break

    return jsonify(forecast)
