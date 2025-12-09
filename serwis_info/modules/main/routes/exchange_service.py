import requests
import yfinance as yf
from flask import Flask, render_template

app = Flask(__name__)

API_KEY = "fca_live_U9au8QtFvTahZj1e9JAR1Hgg9hL83QoEWDckPdTO"
API_URL = "https://api.freecurrencyapi.com/v1/latest"

def get_currency_rates():
    # Use exchangerate.host public API to get reliable latest rates
    global LAST_RATES_DEBUG
    LAST_RATES_DEBUG = ''
    try:
        url = "https://api.exchangerate.host/latest"
        # request rates with base PLN so we can compute EUR/PLN and USD/PLN as inverses
        params = {"base": "PLN", "symbols": "EUR,USD"}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        rates = data.get("rates", {})
        eur_per_pln = rates.get("EUR")
        usd_per_pln = rates.get("USD")
        if eur_per_pln:
            eur_pln = 1.0 / eur_per_pln
        else:
            eur_pln = None
        if usd_per_pln:
            usd_pln = 1.0 / usd_per_pln
        else:
            usd_pln = None
        LAST_RATES_DEBUG = f"exchangerate.host base=PLN rates={rates} eur_pln={eur_pln} usd_pln={usd_pln}"

        # if we didn't get rates, try alternate approach (base EUR)
        if eur_pln is None or usd_pln is None:
            try:
                params2 = {"base": "EUR", "symbols": "PLN,USD"}
                resp2 = requests.get(url, params=params2, timeout=10)
                resp2.raise_for_status()
                d2 = resp2.json()
                r2 = d2.get("rates", {})
                eur_to_pln = r2.get("PLN")
                eur_to_usd = r2.get("USD")
                if eur_to_pln:
                    eur_pln = float(eur_to_pln)
                if eur_to_pln is not None and eur_to_usd is not None and eur_to_usd != 0:
                    usd_pln = float(eur_to_pln) / float(eur_to_usd)
                LAST_RATES_DEBUG += f"; fallback base=EUR rates={r2} eur_pln={eur_pln} usd_pln={usd_pln}"
            except Exception as e:
                LAST_RATES_DEBUG += f"; fallback base=EUR failed: {e}"

        # final fallback: try freecurrencyapi (original)
        if eur_pln is None or usd_pln is None:
            try:
                params3 = {"apikey": API_KEY, "currencies": "PLN,EUR,USD", "base_currency": "USD"}
                resp3 = requests.get(API_URL, params=params3, timeout=10)
                resp3.raise_for_status()
                j3 = resp3.json()
                # Try common response shapes
                rates3 = j3.get('data') or j3.get('results') or j3
                # If we have rates like {'PLN':x,'EUR':y,'USD':z}
                if isinstance(rates3, dict) and 'PLN' in rates3 and 'EUR' in rates3 and 'USD' in rates3:
                    eur_pln = rates3['PLN'] / rates3['EUR']
                    usd_pln = rates3['PLN'] / rates3['USD']
                    LAST_RATES_DEBUG += f"; freecurrencyapi rates3={rates3} eur_pln={eur_pln} usd_pln={usd_pln}"
            except Exception as e:
                LAST_RATES_DEBUG += f"; freecurrencyapi fallback failed: {e}"

        return eur_pln, usd_pln
    except Exception as e:
        LAST_RATES_DEBUG = f"primary exchangerate.host failed: {e}"
        return None, None

def get_gold_price():
    gold = yf.Ticker("GC=F")
    hist = gold.history(period="1d")
    if not hist.empty:
        return hist['Close'].iloc[-1]
    return None


def get_gold_history(days=90):
    """Return list of historical gold close prices for the last `days` days.

    Each item: {'date': 'YYYY-MM-DD', 'close': float}
    """
    try:
        gold = yf.Ticker("GC=F")
        period = f"{days}d"
        hist = gold.history(period=period)
        if hist is None or hist.empty:
            return []
        # hist.index are timestamps; iterate in ascending order
        result = []
        for idx, row in hist.iterrows():
            try:
                date_str = idx.strftime('%Y-%m-%d')
            except Exception:
                date_str = str(idx)
            close = row.get('Close') if 'Close' in row else None
            if close is None or (isinstance(close, float) and (close != close)):
                continue
            result.append({'date': date_str, 'close': float(close)})
        return result
    except Exception:
        return []


def get_currency_history(base: str, symbol: str, days: int = 30):
    """Fetch historical exchange rates for `base`->`symbol` for the last `days` days.

    Uses exchangerate.host timeseries endpoint (no API key required).
    Returns list of {'date': 'YYYY-MM-DD', 'rate': float} ordered oldest->newest.
    """
    try:
        from datetime import datetime, timedelta
        end = datetime.utcnow().date()
        start = end - timedelta(days=days - 1)
        url = 'https://api.exchangerate.host/timeseries'
        params = {
            'start_date': start.isoformat(),
            'end_date': end.isoformat(),
            'base': base,
            'symbols': symbol,
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        j = resp.json()
        rates = j.get('rates') or {}
        items = []
        for d in sorted(rates.keys()):
            r = rates[d].get(symbol)
            if r is None:
                continue
            try:
                items.append({'date': d, 'rate': float(r)})
            except Exception:
                continue
        return items
    except Exception:
        return []

if __name__ == "__main__":
    app.run(debug=True)
