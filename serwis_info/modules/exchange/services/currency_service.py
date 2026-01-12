import requests
import os

API_KEY = os.getenv("CURRENCY_API_KEY")
API_URL = "https://api.freecurrencyapi.com/v1/latest"


def get_exchange_rates(base_currency="PLN"):
    """Pobiera listę kursów względem wybranej waluty"""
    params = {"apikey": API_KEY, "base_currency": base_currency}
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        rates = data.get("data", {})
        return [
            {"name": code, "code": code, "rate": round(rate, 4)}
            for code, rate in rates.items()
        ]
    except Exception as e:
        print(f"Błąd API: {e}")
        return []


def get_exchange_rate(base_currency, target_currency):
    """Zwraca kurs wymiany między dwiema walutami"""
    rates = get_exchange_rates(base_currency)
    for r in rates:
        if r["code"] == target_currency:
            return r["rate"]
    return None
