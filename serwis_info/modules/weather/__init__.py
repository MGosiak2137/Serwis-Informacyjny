from flask import Blueprint
from .routes import register_routes

def create_weather_blueprint():
    bp = Blueprint(
        'weather', __name__,
        template_folder='templates',
        static_folder='static'
    )

    register_routes(bp)
    return bp
