from flask import Flask, render_template

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    from serwis_info.modules.exchange.routes.currencies import currencies_bp
    from serwis_info.modules.exchange.routes.stockmarket import stockmarket_bp
    from serwis_info.modules.exchange.routes.journey import journey_bp

    app.register_blueprint(currencies_bp)
    app.register_blueprint(stockmarket_bp)
    app.register_blueprint(journey_bp)

    @app.route("/")
    def index():
        return render_template("nav_foot_eco.html")

    return app
