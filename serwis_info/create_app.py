from flask import Flask, render_template
import os

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    
    from serwis_info.modules.exchange.routes.currencies import currencies_bp
    from serwis_info.modules.exchange.routes.stockmarket import stockmarket_bp
    from serwis_info.modules.exchange.routes.journey import journey_bp    
    from serwis_info.modules.main.routes.main import main_bp
    from serwis_info.modules.main.routes.auth import auth_bp
    
    app.secret_key = "moja"
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(currencies_bp)
    app.register_blueprint(stockmarket_bp)
    app.register_blueprint(journey_bp)   
    
    @app.route("/")
    def index():
        return render_template("index.html")

    return app

