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
    # attempt to fetch historical gold prices (last 90 days)
    gold_history = []
    try:
        gold_history = exchange_service.get_gold_history(90)
    except Exception:
        gold_history = []

    # fetch small FX histories for USD/PLN and EUR/PLN (last 30 days)
    usd_history = []
    eur_history = []
    try:
        usd_history = exchange_service.get_currency_history('USD', 'PLN', 30)
    except Exception:
        usd_history = []
    try:
        eur_history = exchange_service.get_currency_history('EUR', 'PLN', 30)
    except Exception:
        eur_history = []

    return jsonify(
        eur_pln=eur_pln,
        usd_pln=usd_pln,
        gold_price=gold_price,
        gold_history=gold_history,
        usd_history=usd_history,
        eur_history=eur_history,
        rates_debug=getattr(exchange_service, 'LAST_RATES_DEBUG', None),
    )