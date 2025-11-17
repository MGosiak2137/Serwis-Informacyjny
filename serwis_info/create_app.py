from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Tutaj możesz dodawać konfigurację globalną
    app.config['SECRET_KEY'] = 'tajny_klucz'

    # Inne moduły, np. weather, można inicjalizować później
    from serwis_info.modules.weather import create_weather_blueprint
    weather_bp = create_weather_blueprint()
    app.register_blueprint(weather_bp, url_prefix='/weather')
    return app


