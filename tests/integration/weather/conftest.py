import os
import sys
import pytest

# Ensure project root is on sys.path for imports like `serwis_info.*`
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

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
