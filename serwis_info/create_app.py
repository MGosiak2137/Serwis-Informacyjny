from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # --- Blueprinty ---
    from serwis_info.modules.main.routes.main import main_bp
    from app.auth import auth_bp
    from serwis_info.modules.exchange.routes.currencies import currencies_bp
    from serwis_info.modules.exchange.routes.stockmarket import stockmarket_bp
    from serwis_info.modules.exchange.routes.journey import journey_bp
    from serwis_info.modules.exchange.routes.main import main_eco_bp 

    from serwis_info.modules.calendar.routes.horoscope_routes import horoscope_bp
    from serwis_info.modules.news.routes.news_page import news_bp

    from serwis_info.modules.weather import create_weather_blueprint
    weather_bp = create_weather_blueprint()
    app.register_blueprint(weather_bp, url_prefix="/weather")

    from serwis_info.modules.weather.routes.weather_routes import weather_api_bp
    app.register_blueprint(weather_api_bp)
    # from serwis_info.modules.weather.routes.history_routes import history_bp
    # app.register_blueprint(history_bp)
    # koniec rejestracji weather blueprint

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(currencies_bp)
    app.register_blueprint(stockmarket_bp)
    app.register_blueprint(journey_bp)
    app.register_blueprint(main_eco_bp)
    app.register_blueprint(horoscope_bp)
    app.register_blueprint(news_bp)

    @app.route("/")
    def index():
        return redirect(url_for("main.index"))

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
