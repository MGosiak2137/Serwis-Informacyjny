
from .weather_routes import weather_api_bp
from .history_routes import history_bp

def register_routes(bp):
    bp.register_blueprint(weather_api_bp)
    bp.register_blueprint(history_bp)

#Łączy wszystkie blueprinty Flaska w jeden punkt rejestracji. 

#bp → główny blueprint aplikacji lub app. 