import requests
import yfinance as yf
from flask import Flask, render_template

app = Flask(__name__)

API_KEY = "fca_live_ETTrbfogzJW4ig6qMwd4i3Co98bLc61r7HnsqMex"
API_URL = "https://api.freecurrencyapi.com/v1/latest"

def get_currency_rates():
    params = {
        "apikey": API_KEY,
        "currencies": "PLN,EUR,USD",
        "base_currency": "USD"  # lub "PLN", zależnie jak chcesz bazę kursu
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    # Załóżmy, że API zwraca kursy względem base_currency, zmapuj na PLN
    try:
        eur_pln = data["data"]["PLN"] / data["data"]["EUR"]  # EUR to PLN
        usd_pln = data["data"]["PLN"] / data["data"]["USD"]  # USD to PLN
    except Exception:
        eur_pln = None
        usd_pln = None
    return eur_pln, usd_pln

def get_gold_price():
    gold = yf.Ticker("GC=F")
    hist = gold.history(period="1d")
    if not hist.empty:
        return hist['Close'].iloc[-1]
    return None

if __name__ == "__main__":
    app.run(debug=True)
