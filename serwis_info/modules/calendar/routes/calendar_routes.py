from flask import Blueprint, render_template, jsonify
import os

# Oblicz ścieżkę do templates kalendarza
current_dir = os.path.dirname(os.path.abspath(__file__))
calendar_templates_dir = os.path.join(current_dir, '../templates')
calendar_static_dir = os.path.join(current_dir, '../static')

calendar_bp = Blueprint(
    "calendar",
    __name__,
    url_prefix="/calendar",
    template_folder=calendar_templates_dir,  
    static_folder=calendar_static_dir        
)

@calendar_bp.route("/")
def calendar():
    return render_template("calendar.html")

@calendar_bp.route("/api/calendar")
def get_calendar():
    from serwis_info.modules.calendar.services import calendar_service
    data = calendar_service.get_calendar_data()
    return jsonify(data)

@calendar_bp.route("/horoscope")
def horoscope_page():
    return render_template("horoscope.html")

@calendar_bp.route("/api/horoscope/<zodiac_sign>")
def get_horoscope(zodiac_sign):
    from serwis_info.modules.calendar.services import horoscope_service
    data = horoscope_service.get_horoscope(zodiac_sign)
    if "error" in data:
        return jsonify(data), 400
    return jsonify(data)

@calendar_bp.route("/api/horoscope")
def get_all_zodiacs():
    from serwis_info.modules.calendar.services import horoscope_service
    data = horoscope_service.get_available_zodiacs()
    return jsonify(data)