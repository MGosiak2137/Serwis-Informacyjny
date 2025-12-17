import os
import sys
import pytest

# Ensure project root is on sys.path for imports like `serwis_info.*`
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Use the main app factory
from serwis_info.create_app import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(TESTING=True, LOGIN_DISABLED=True)
    return app


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client


class _DummyUser:
    def __init__(self, user_id: int = 1):
        self.id = user_id


@pytest.fixture()
def fake_login(monkeypatch):
    """Bypass Flask-Login for news blueprint routes and provide a dummy current_user.

    Patches:
      - serwis_info.modules.news.routes.news_page.login_required -> identity decorator
      - serwis_info.modules.news.routes.news_page.current_user -> dummy object with id
    """
    import serwis_info.modules.news.routes.news_page as news_page

    def identity_decorator(fn):
        return fn

    monkeypatch.setattr(news_page, "login_required", identity_decorator, raising=False)
    monkeypatch.setattr(news_page, "current_user", _DummyUser(1), raising=False)
    return _DummyUser(1)
