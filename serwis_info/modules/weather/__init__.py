from flask import Blueprint

def create_weather_blueprint():
    from .routes import register_routes
    bp = Blueprint('weather', __name__, template_folder='templates', static_folder='static')
    register_routes(bp)
    return bp