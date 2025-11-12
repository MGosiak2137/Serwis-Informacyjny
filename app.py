# Główny plik uruchamiający flaska
# Importuje create_app() z pakietu serwis_info i uruchamia serwer flask

try:
    from serwis_info import create_app
    app = create_app()
except Exception:
    from flask import Flask, render_template, request
    app = Flask(__name__, template_folder='serwis_info/templates', static_folder='serwis_info/static')

    @app.route("/")
    def index():
        # przykładowe wartości footer_url/footer_text do łatwego testu
        return render_template("nav_foot_eco.html")

    @app.route("/currencies")
    def currencies():
        sample_rates = [
            {"name": "Dolar", "code": "USD", "rate": "4.21"},
            {"name": "Euro", "code": "EUR", "rate": "4.60"},
            {"name": "Funt", "code": "GBP", "rate": "5.31"},
        ]
        return render_template("currencies.html")
    
    @app.route("/stockmarket")
    def stockmarket():
        sample_rates = [
            {"name": "WIG20", "code": "W20", "rate": "+0.54%"},
            {"name": "S&P 500", "code": "SPX", "rate": "+0.73%"},
            {"name": "DAX", "code": "DAX", "rate": "-0.12%"},
        ]
        return render_template("stockmarket.html")

    @app.route("/journey")
    def journey():
        destination = request.args.get("destination")
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")
        people = request.args.get("people") or 1
        return render_template("journey.html",
                               destination=destination,
                               date_from=date_from,
                               date_to=date_to,
                               people=people)

if __name__ == "__main__":
    app.run(debug=True)