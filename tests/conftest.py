# tests/conftest.py
import pytest
from app import create_app, db as _db

@pytest.fixture
def app():
    app = create_app()

    # >>> KONFIGURACJA TESTOWA <<<
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        LOGIN_DISABLED=False,
    )

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
