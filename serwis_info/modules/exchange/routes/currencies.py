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
    {"name": "Dolar amerykański", "code": "USD",
     "rate": round(1 / rates_data.get("USD", 0), 2) if rates_data.get("USD") else 0},

    {"name": "Euro", "code": "EUR",
     "rate": round(1 / rates_data.get("EUR", 0), 2) if rates_data.get("EUR") else 0},

    {"name": "Funt brytyjski", "code": "GBP",
     "rate": round(1 / rates_data.get("GBP", 0), 2) if rates_data.get("GBP") else 0},

    {"name": "Frank szwajcarski", "code": "CHF",
     "rate": round(1 / rates_data.get("CHF", 0), 2) if rates_data.get("CHF") else 0},

    # 🔽 NOWE WALUTY 🔽

    {"name": "Jen japoński", "code": "JPY",
     "rate": round(1 / rates_data.get("JPY", 0), 4) if rates_data.get("JPY") else 0},

    {"name": "Korona czeska", "code": "CZK",
     "rate": round(1 / rates_data.get("CZK", 0), 4) if rates_data.get("CZK") else 0},

    {"name": "Korona norweska", "code": "NOK",
     "rate": round(1 / rates_data.get("NOK", 0), 4) if rates_data.get("NOK") else 0},

    {"name": "Korona szwedzka", "code": "SEK",
     "rate": round(1 / rates_data.get("SEK", 0), 4) if rates_data.get("SEK") else 0},

    {"name": "Korona duńska", "code": "DKK",
     "rate": round(1 / rates_data.get("DKK", 0), 4) if rates_data.get("DKK") else 0},

    {"name": "Forint węgierski", "code": "HUF",
     "rate": round(1 / rates_data.get("HUF", 0), 4) if rates_data.get("HUF") else 0},

    {"name": "Juan chiński", "code": "CNY",
     "rate": round(1 / rates_data.get("CNY", 0), 4) if rates_data.get("CNY") else 0},

    {"name": "Dolar australijski", "code": "AUD",
     "rate": round(1 / rates_data.get("AUD", 0), 4) if rates_data.get("AUD") else 0},

    {"name": "Dolar kanadyjski", "code": "CAD",
     "rate": round(1 / rates_data.get("CAD", 0), 4) if rates_data.get("CAD") else 0}
]


    return render_template("currencies.html", title="Kursy walut", rates=rates)


@currencies_bp.route("/convert", methods=["POST"])
def convert():
    amount = float(request.form.get("amount"))
    from_currency = request.form.get("from_currency").upper()
    to_currency = request.form.get("to_currency").upper()

    # zawsze pobierz względem PLN
    rates_data = get_exchange_rates("PLN")

    # konwersja jeśli użytkownik chce z waluty obcej do PLN
    if to_currency == "PLN":
        rate = rates_data.get(from_currency)
        converted = round(amount * rate, 2) if rate else None

    # jeśli ktoś chce PLN → USD/EUR itd.
    elif from_currency == "PLN":
        rate = rates_data.get(to_currency)
        converted = round(amount / rate, 2) if rate else None

    else:
        # Konwersja między obcymi walutami: zawsze przez PLN
        rate_from = rates_data.get(from_currency)
        rate_to = rates_data.get(to_currency)

        if rate_from and rate_to:
            converted = round(amount * (rate_to / rate_from), 2)
        else:
            converted = None

    rates = [
    {"name": "Dolar amerykański", "code": "USD",
     "rate": round(1 / rates_data.get("USD", 0), 2) if rates_data.get("USD") else 0},

    {"name": "Euro", "code": "EUR",
     "rate": round(1 / rates_data.get("EUR", 0), 2) if rates_data.get("EUR") else 0},

    {"name": "Funt brytyjski", "code": "GBP",
     "rate": round(1 / rates_data.get("GBP", 0), 2) if rates_data.get("GBP") else 0},

    {"name": "Frank szwajcarski", "code": "CHF",
     "rate": round(1 / rates_data.get("CHF", 0), 2) if rates_data.get("CHF") else 0},

    # 🔽 NOWE WALUTY 🔽

    {"name": "Jen japoński", "code": "JPY",
     "rate": round(1 / rates_data.get("JPY", 0), 4) if rates_data.get("JPY") else 0},

    {"name": "Korona czeska", "code": "CZK",
     "rate": round(1 / rates_data.get("CZK", 0), 4) if rates_data.get("CZK") else 0},

    {"name": "Korona norweska", "code": "NOK",
     "rate": round(1 / rates_data.get("NOK", 0), 4) if rates_data.get("NOK") else 0},

    {"name": "Korona szwedzka", "code": "SEK",
     "rate": round(1 / rates_data.get("SEK", 0), 4) if rates_data.get("SEK") else 0},

    {"name": "Korona duńska", "code": "DKK",
     "rate": round(1 / rates_data.get("DKK", 0), 4) if rates_data.get("DKK") else 0},

    {"name": "Forint węgierski", "code": "HUF",
     "rate": round(1 / rates_data.get("HUF", 0), 4) if rates_data.get("HUF") else 0},

    {"name": "Juan chiński", "code": "CNY",
     "rate": round(1 / rates_data.get("CNY", 0), 4) if rates_data.get("CNY") else 0},

    {"name": "Dolar australijski", "code": "AUD",
     "rate": round(1 / rates_data.get("AUD", 0), 4) if rates_data.get("AUD") else 0},

    {"name": "Dolar kanadyjski", "code": "CAD",
     "rate": round(1 / rates_data.get("CAD", 0), 4) if rates_data.get("CAD") else 0}
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

