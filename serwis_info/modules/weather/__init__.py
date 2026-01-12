from flask import Blueprint
from .routes.weather_routes import weather_api_bp
from .routes.history_routes import history_bp
from .routes.dashboard_routes import register_dashboard_routes

def create_weather_blueprint():
    bp = Blueprint(
        'weather', __name__,
        template_folder='templates',
        static_folder='static'
    )
    bp.register_blueprint(weather_api_bp)
    bp.register_blueprint(history_bp)
    register_dashboard_routes(bp)
    return bp
