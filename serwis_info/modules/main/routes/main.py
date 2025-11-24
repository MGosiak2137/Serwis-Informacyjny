from flask import Blueprint, render_template, jsonify


main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/main",
    template_folder="../../templates",
    static_folder="../static",
)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/api/calendar")
def get_calendar():
    from serwis_info.modules.main.routes import calendar_service
    data = calendar_service.get_calendar_data()
    return jsonify(data)
    