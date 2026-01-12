from flask import Blueprint, jsonify, render_template
from flask_login import login_required
import requests
from collections import Counter

weather_api_bp = Blueprint("weather_api", __name__)

API_KEY = "25ae8c36b22398f35b25584807571f27"

@weather_api_bp.route("/")
def weather_main():
    return render_template("dashboard.html")

@weather_api_bp.route("/dashboard")
@login_required
def dashboard_page():
    return render_template("dashboard.html")

@weather_api_bp.route("/api/simple_weather")
def simple_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Warsaw&units=metric&lang=pl&appid={API_KEY}"
    data = requests.get(url).json()
    return jsonify({
        "temp": round(data["main"]["temp"]),
        "desc": data["weather"][0]["description"].capitalize(),
        "icon": data["weather"][0]["icon"]
    })

@weather_api_bp.route("/api/forecast")
def weather_forecast():
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Warsaw&units=metric&lang=pl&appid={API_KEY}"
    data = requests.get(url).json()

    daily = {}
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        desc = item["weather"][0]["description"].capitalize()
        if date not in daily:
            daily[date] = {"temps":[], "winds":[], "humidity":[], "icons":[], "desc":[]}
        daily[date]["temps"].append(item["main"]["temp"])
        daily[date]["winds"].append(item["wind"]["speed"])
        daily[date]["humidity"].append(item["main"]["humidity"])
        daily[date]["icons"].append(item["weather"][0]["icon"])
        daily[date]["desc"].append(desc)

    forecast = []
    for date, values in list(daily.items())[:3]:
        avg_temp = round(sum(values["temps"]) / len(values["temps"]))
        avg_wind = round(sum(values["winds"]) / len(values["winds"]), 1)
        avg_hum = round(sum(values["humidity"]) / len(values["humidity"]))
        icon = Counter(values["icons"]).most_common(1)[0][0]
        desc = Counter(values["desc"]).most_common(1)[0][0]
        forecast.append({
            "date": date,
            "temp": avg_temp,
            "wind": avg_wind,
            "humidity": avg_hum,
            "icon": icon,
            "desc": desc
        })

    return jsonify(forecast)
