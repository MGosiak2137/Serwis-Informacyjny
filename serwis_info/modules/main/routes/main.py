from flask import Blueprint, render_template, jsonify


main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/main",
    template_folder="../templates",
    static_folder="../static",          
)


@main_bp.route("/")
def index():
    return render_template("index.html", body_class="home-page")

@main_bp.route("/api/calendar")
def get_calendar():
    from serwis_info.modules.main.routes import calendar_service
    data = calendar_service.get_calendar_data()
    return jsonify(data)
    
@main_bp.route("/api/exchange")
def home():
    from serwis_info.modules.main.routes import exchange_service
    eur_pln, usd_pln = exchange_service.get_currency_rates()
    gold_price = exchange_service.get_gold_price()
    return jsonify(eur_pln=eur_pln, usd_pln=usd_pln, gold_price=gold_price)