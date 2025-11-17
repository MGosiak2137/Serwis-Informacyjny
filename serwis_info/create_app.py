from flask import Flask, render_template

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    
    from serwis_info.modules.weather.routes.dashboard_routes import dashboards_bp
    from serwis_info.modules.weather.routes.history_routes import history_bp
    from serwis_info.modules.weather.routes.user_routes import user_bp
    
    app.secret_key = "moja"
    app.register_blueprint(dashboards_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(user_bp)
  

    from serwis_info.modules.weather import create_weather_blueprint
    weather_bp = create_weather_blueprint()
    app.register_blueprint(weather_bp, url_prefix='/weather')
    
    @app.route("/")
    def index():
        return render_template("index.html")

    return app
