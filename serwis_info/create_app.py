from flask import Flask, render_template

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
       

    from serwis_info.modules.weather import create_weather_blueprint
    weather_bp = create_weather_blueprint()
    app.register_blueprint(weather_bp, url_prefix='/weather')
    
    @app.route("/")
    def index():
        return render_template("dashboard.html")

    return app
