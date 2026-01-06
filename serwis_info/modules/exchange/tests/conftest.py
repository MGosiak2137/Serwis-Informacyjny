import pytest
from serwis_info.create_app import create_app
from config import TestingConfig
from werkzeug.serving import make_server
import threading


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.from_object(TestingConfig)

    # WAŻNE: tryb testowy
    app.config["TESTING"] = True
    app.config["LOGIN_DISABLED"] = False

    yield app


@pytest.fixture(scope="session")
def e2e_server(app):
    server = make_server("127.0.0.1", 0, app)
    port = server.server_port

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    yield f"http://127.0.0.1:{port}"

    server.shutdown()
    thread.join()
