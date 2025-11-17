from flask import Flask, render_template
import os

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    
    try:
        # Spróbuj bezpośredniego importu z pliku
        from serwis_info.modules.calendar.routes.calendar_routes import calendar_bp
        print("✅ Blueprint zaimportowany bezpośrednio z pliku!")
        app.register_blueprint(calendar_bp)
    except ImportError as e:
        print(f"❌ Błąd importu blueprinta: {e}")
        # Tymczasowy blueprint
        from flask import Blueprint
        temp_bp = Blueprint('calendar', __name__, url_prefix='/calendar')
        
        @temp_bp.route('/')
        def temp_calendar():
            return "Kalendarz - w budowie"
            
        @temp_bp.route('/horoscope')
        def temp_horoscope():
            return "Horoskop - w budowie"
            
        app.register_blueprint(temp_bp)

    @app.route("/")
    def index():
        # Przekieruj bezpośrednio do kalendarza jako strony głównej
        from flask import redirect
        return redirect("/calendar/")

    return app