import pytest
from app.models import User


def test_set_password_hash_is_created():
    """Ustawienie hasła tworzy hash"""
    user = User(email="unit@test.pl", nickname="unit")
    user.set_password("Secret123!")

    assert user.password_hash is not None
    assert user.password_hash != "Secret123!"


def test_check_password_correct():
    """Poprawne hasło zwraca True"""
    user = User(email="unit@test.pl", nickname="unit")
    user.set_password("Secret123!")

    assert user.check_password("Secret123!") is True


def test_check_password_incorrect():
    """Niepoprawne hasło zwraca False"""
    user = User(email="unit@test.pl", nickname="unit")
    user.set_password("Secret123!")

    assert user.check_password("WrongPass") is False


def test_check_password_with_empty_password():
    """Puste hasło nigdy nie przechodzi"""
    user = User(email="unit@test.pl", nickname="unit")
    user.set_password("Secret123!")

    assert user.check_password("") is False
