from flask import Blueprint, render_template, request
import requests

currencies_bp = Blueprint(
    "currencies",
    __name__,
    url_prefix="/currencies",
    template_folder="../templates",
    static_folder="../static"
)

API_KEY = "fca_live_ETTrbfogzJW4ig6qMwd4i3Co98bLc61r7HnsqMex"
API_URL = "https://api.freecurrencyapi.com/v1/latest"


def get_exchange_rates(base_currency="PLN"):
    """Pobiera aktualne kursy walut."""
    params = {"apikey": API_KEY, "base_currency": base_currency}
    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        return data.get("data", {})
    except Exception as e:
        print("Błąd API:", e)
        return {}


@currencies_bp.route("/", methods=["GET"])
def currencies():
    rates_data = get_exchange_rates("PLN")
    rates = [
        {"name": "Dolar amerykański", "code": "USD", "rate": round(rates_data.get("USD", 0), 2)},
        {"name": "Euro", "code": "EUR", "rate": round(rates_data.get("EUR", 0), 2)},
        {"name": "Funt brytyjski", "code": "GBP", "rate": round(rates_data.get("GBP", 0), 2)},
        {"name": "Frank szwajcarski", "code": "CHF", "rate": round(rates_data.get("CHF", 0), 2)},
    ]
    return render_template("currencies.html", title="Kursy walut", rates=rates)


@currencies_bp.route("/convert", methods=["POST"])
def convert():
    amount = float(request.form.get("amount"))
    from_currency = request.form.get("from_currency").upper()
    to_currency = request.form.get("to_currency").upper()

    rates_data = get_exchange_rates(from_currency)
    rate = rates_data.get(to_currency)
    converted = round(amount * rate, 2) if rate else None

    rates = [
        {"name": "Dolar amerykański", "code": "USD", "rate": round(rates_data.get("USD", 0), 2)},
        {"name": "Euro", "code": "EUR", "rate": round(rates_data.get("EUR", 0), 2)},
        {"name": "Funt brytyjski", "code": "GBP", "rate": round(rates_data.get("GBP", 0), 2)},
        {"name": "Frank szwajcarski", "code": "CHF", "rate": round(rates_data.get("CHF", 0), 2)},
    ]

    return render_template(
        "currencies.html",
        title="Kursy walut",
        rates=rates,
        amount=amount,
        from_currency=from_currency,
        to_currency=to_currency,
        converted=converted
    )
