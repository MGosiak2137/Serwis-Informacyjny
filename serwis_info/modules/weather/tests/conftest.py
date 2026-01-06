import pytest
from flask import Flask

from serwis_info.modules.weather.routes.weather_routes import weather_api_bp
from serwis_info.modules.weather.routes.history_routes import history_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(weather_api_bp, url_prefix="/weather")
    app.register_blueprint(history_bp, url_prefix="/weather")
    return app


@pytest.fixture
def client(app):
    return app.test_client()
