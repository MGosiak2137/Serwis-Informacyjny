import pytest
from app import db
from app.models import User
from flask_login import current_user


# -----------------------
# FIXTURES
# -----------------------

@pytest.fixture
def user(app):
    """Testowy użytkownik zapisany w bazie"""
    user = User(
        email="test@example.com",
        nickname="tester",
    )
    user.set_password("Test1234!")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def login(client, user):
    """Pomocnicza funkcja logowania"""
    def do_login(password="Test1234!"):
        return client.post(
            "/auth/login",
            data={
                "email": user.email,
                "password": password,
            },
            follow_redirects=True,
        )
    return do_login


# -----------------------
# TESTY MODELU USER
# -----------------------

def test_set_and_check_password(user):
    assert user.check_password("Test1234!") is True
    assert user.check_password("WrongPass") is False


# -----------------------
# LOGOWANIE / WYLOGOWANIE
# -----------------------

def test_login_success(client, login):
    response = login()
    assert response.status_code == 200
    # po zalogowaniu użytkownik jest uwierzytelniony
    with client.session_transaction():
        assert current_user.is_authenticated


def test_login_wrong_password(client, login):
    response = login(password="BadPass")
    assert response.status_code == 200
    with client.session_transaction():
        assert current_user.is_authenticated is False


def test_logout_logs_user_out(client, login):
    login()
    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction():
        assert current_user.is_authenticated is False


# -----------------------
# DOSTĘP DO KONTA
# -----------------------

def test_account_access_not_logged_in(client):
    response = client.get("/main/account", follow_redirects=False)
    # Flask-Login redirectuje do login
    assert response.status_code in (301, 302)


def test_account_access_logged_in(client, login):
    login()
    response = client.get("/main/account")
    assert response.status_code == 200


# -----------------------
# ZMIANA HASŁA
# -----------------------

def test_change_password_wrong_current(client, login):
    login()
    response = client.post(
        "/main/account/change-password",
        data={
            "current_password": "WrongPass",
            "new_password": "NewPass123!",
            "confirm_password": "NewPass123!",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

# -----------------------
# USUWANIE KONTA
# -----------------------

def test_delete_account_logged_in(client, login, user):
    login()
    response = client.post("/main/account/delete", follow_redirects=True)
    assert response.status_code == 200

    deleted_user = User.query.filter_by(email=user.email).first()
    assert deleted_user is None
