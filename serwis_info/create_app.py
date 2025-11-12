from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # importujemy blueprinty (zdefiniowane osobno)
    from serwis_info.modules.exchange.routes.currencies import currencies_bp
    from serwis_info.modules.exchange.routes.stockmarket import stockmarket_bp

    # rejestrujemy blueprinty
    app.register_blueprint(currencies_bp)
    app.register_blueprint(stockmarket_bp)

    @app.route("/")
    def index():
        return "<h3>Serwis informacyjny — strona główna</h3>"

    return app
