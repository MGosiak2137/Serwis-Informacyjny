from flask import Blueprint, render_template, jsonify
import os

# Oblicz ścieżkę do templates kalendarza
current_dir = os.path.dirname(os.path.abspath(__file__))
calendar_templates_dir = os.path.join(current_dir, '../templates')
calendar_static_dir = os.path.join(current_dir, '../static')

horoscope_bp = Blueprint(
    "horoscope",
    __name__,
    url_prefix="/calendar",
    template_folder=calendar_templates_dir,  
    static_folder=calendar_static_dir        
)

@horoscope_bp.route("/horoscope")
def horoscope_page():
    return render_template("horoscope.html")

@horoscope_bp.route("/api/horoscope/<zodiac_sign>")
def get_horoscope(zodiac_sign):
    from serwis_info.modules.calendar.services import horoscope_service
    data = horoscope_service.get_horoscope(zodiac_sign)
    if "error" in data:
        return jsonify(data), 400
    return jsonify(data)

@horoscope_bp.route("/api/horoscope")
def get_all_zodiacs():
    from serwis_info.modules.calendar.services import horoscope_service
    data = horoscope_service.get_available_zodiacs()
    return jsonify(data)