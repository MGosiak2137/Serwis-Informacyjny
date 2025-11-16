from flask import Flask

from serwis_info.modules.main.routes import main_bp
from serwis_info.modules.main.auth.routes import auth_bp


def create_my_app():
    app = Flask(__name__)
    app.secret_key = "moja"
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app


if __name__ == "__main__":
    app = create_my_app()
    app.run(debug=True)
