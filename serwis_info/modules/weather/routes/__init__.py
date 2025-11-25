# zamiast tego:
# from .history_routes import register_history_routes

# używaj blueprintów bezpośrednio
from .weather_routes import weather_api_bp
from .history_routes import history_bp

def register_routes(bp):
    bp.register_blueprint(weather_api_bp)
    bp.register_blueprint(history_bp)

