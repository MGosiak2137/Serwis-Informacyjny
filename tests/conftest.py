# tests/conftest.py
import pytest
from app import create_app, db as _db
from app.models import User
from werkzeug.security import generate_password_hash

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

@pytest.fixture
def logged_in_user(client, app):
    user = User(
        email="test@test.pl",
        nickname="testuser",
        password_hash=generate_password_hash("password")
    )

    with app.app_context():
        _db.session.add(user)
        _db.session.commit()

    client.post(
        "/auth/login",
        data={
            "email": "test@test.pl",
            "password": "password"
        },
        follow_redirects=True
    )

    return user