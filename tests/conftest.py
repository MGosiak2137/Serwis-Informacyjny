import os
import threading
import tempfile
from contextlib import closing
import socket

import pytest
from werkzeug.serving import make_server

# Ensure project root is on sys.path so imports like `serwis_info` work when
# pytest is invoked from other directories or virtualenvs.
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import glob

# Workaround: ensure pytest loads each test file as a module with a unique
# module name to avoid "import file mismatch" when different test files share
# the same basename. We do this by wrapping importlib.util.spec_from_file_location
# so that test files get a stable unique module name based on their absolute
# path.
# (no importlib monkeypatching — keep imports and sys.modules cleanup above)

# If there are test modules with the same basename in different subfolders
# pytest may import one earlier which causes "import file mismatch" errors.
# Remove any pre-imported modules whose basenames appear multiple times so
# pytest will import the correct file for each path.
test_root = os.path.abspath(os.path.dirname(__file__))
duplicates = {}
for p in glob.glob(os.path.join(test_root, '**', 'test_*.py'), recursive=True):
    name = os.path.splitext(os.path.basename(p))[0]
    duplicates.setdefault(name, []).append(os.path.abspath(p))

for name, paths in duplicates.items():
    if len(paths) > 1 and name in sys.modules:
        del sys.modules[name]

from serwis_info.create_app import create_app, db
from config import TestingConfig


def _find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def pytest_collect_file(path=None, file_path=None, parent=None):
    # Support both legacy (path) and new (file_path) hook signatures.
  #  p = file_path if file_path is not None else path
   # if p is None:
    #    return None
    #try:
     #   name = p.basename
    #except AttributeError:
     #   name = os.path.basename(str(p))
    #if name.startswith("test_") and name.endswith(".py"):
     #   modname = os.path.splitext(name)[0]
      #  if modname in sys.modules:
       #     del sys.modules[modname]
    return None


def pytest_load_initial_conftests(early_config, parser):
    # Run very early during pytest startup: remove any modules from
    # sys.modules whose names collide with test basenames so pytest will
    # import the correct file for each test path later.
    try:
        test_root = os.path.abspath(os.path.dirname(__file__))
        for p in glob.glob(os.path.join(test_root, '**', 'test_*.py'), recursive=True):
            modname = os.path.splitext(os.path.basename(p))[0]
            if modname in sys.modules:
                del sys.modules[modname]
    except Exception:
        # best-effort only; don't raise during initial conftest loading
        pass


@pytest.fixture(scope="session")
def app():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    db_path = tmp.name

    app = create_app(TestingConfig)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SESSION_COOKIE_SECURE"] = False
    app.config["SESSION_COOKIE_HTTPONLY"] = False
    app.config["SESSION_COOKIE_SAMESITE"] = None
    app.config["REMEMBER_COOKIE_SECURE"] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = 3600

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

    try:
        os.unlink(db_path)
    except OSError:
        pass


@pytest.fixture
def client(app):
    """Test client WITHOUT login (for unauthenticated tests)."""
    test_client = app.test_client()
    return test_client


@pytest.fixture
def authenticated_client(app):
    """Test client with logged-in user (user id=1)."""
    from app.models import User
    from flask_login import login_user
    
    test_client = app.test_client()
    
    # Create a test user that will be used for logins
    with app.app_context():
        user = db.session.query(User).filter_by(id=1).first()
        if not user:
            user = User(email='fake@login.com', nickname='fakeuser')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
    
    # Use Flask-Login's login_user via the test client to properly set session
    with test_client:
        with app.test_request_context():
            # Reload user within this context to avoid detached instance error
            user = db.session.query(User).filter_by(id=1).first()
            login_user(user, remember=False)
    
    return test_client


@pytest.fixture
def fake_login(authenticated_client):
    """Provides access to the authenticated client's session for changing user."""
    def _login(user_id=1):
        """Change logged-in user_id for a test."""
        with authenticated_client.session_transaction() as sess:
            sess['user_id'] = user_id
            sess.permanent = True
        return user_id
    
    return _login


@pytest.fixture
def logged_in_user(app, client):
    """Create and login a real user in the test database."""
    from app.models import User
    from flask_login import login_user
    
    with app.app_context():
        user = User(email='testuser@example.com', nickname='testuser')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        
        # Log the user in using Flask-Login properly
        with client.session_transaction() as sess:
            sess['user_id'] = user_id
            sess['_fresh'] = True
            sess.permanent = True
        
        yield user
        
        # Cleanup
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()


@pytest.fixture
def credentials(app):
    """Provide test user credentials for e2e tests. Creates user in test DB."""
    from app.models import User
    
    email = 'test@test.pl'
    password = 'testpassword123'
    
    with app.app_context():
        # Check if user exists, if not create it
        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        
        user = User(email=email, nickname='testuser')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    
    return {
        'email': email,
        'nickname': 'testuser',
        'password': password
    }


@pytest.fixture
def ensure_logged_in(app, credentials):
    """Fixture that pre-creates a logged-in user for tests."""
    from app.models import User
    
    with app.app_context():
        user = db.session.query(User).filter_by(email=credentials['email']).first()
        if not user:
            user = User(email=credentials['email'], nickname=credentials['nickname'])
            user.set_password(credentials['password'])
            db.session.add(user)
            db.session.commit()
        return user


@pytest.fixture(scope="function")
def e2e_server(app):
    """
    Uruchamia prawdziwy serwer HTTP dla testów E2E (Playwright).
    Zwraca URL serwera, np. http://127.0.0.1:52341
    """
    server = make_server("127.0.0.1", 0, app)
    
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    
    host, port = server.server_address
    base_url = f"http://{host}:{port}"
    
    # ---- tu test dostaje URL ----
    yield base_url
    
    # ---- teardown (ZAWSZE się wykona) ----
    server.shutdown()
    thread.join()


@pytest.fixture
def open_first_article_detail():
    """Helper fixture for opening first article detail in e2e tests."""
    return None




