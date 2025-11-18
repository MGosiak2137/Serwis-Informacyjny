from flask import Blueprint, render_template, request
import yfinance as yf
from datetime import datetime, timedelta, time
import pytz

stockmarket_bp = Blueprint("stockmarket", __name__, url_prefix="/stockmarket")

POLISH_DAYS = {
    0: "Poniedziałek", 1: "Wtorek", 2: "Środa", 3: "Czwartek",
    4: "Piątek", 5: "Sobota", 6: "Niedziela"
}

# Mapowanie symboli na rynki — strefa czasowa + godziny otwarcia
MARKET_INFO = {
    # Indeksy USA
    "^GSPC": ("US/Eastern", time(9, 30), time(16, 0)),
    "^N100": ("US/Eastern", time(9, 30), time(16, 0)),

    # Niemcy — DAX
    "^GDAXI": ("Europe/Berlin", time(9, 0), time(17, 30)),

    # FTSE UK
    "^FTSE": ("Europe/London", time(8, 0), time(16, 30)),

    # Surowce — Futures (prawie 24/5)
    "GC=F": ("US/Eastern", time(18, 0), time(17, 0)),
    "CL=F": ("US/Eastern", time(18, 0), time(17, 0)),
    "NG=F": ("US/Eastern", time(18, 0), time(17, 0)),
    "SI=F": ("US/Eastern", time(18, 0), time(17, 0)),

    # Kryptowaluty — 24/7
    "BTC-USD": ("UTC", None, None),
    "ETH-USD": ("UTC", None, None),
}

def is_market_open_for_symbol(symbol):
    """
    Realistyczne sprawdzanie czy rynek jest otwarty:
    - uwzględnia strefę czasową
    - sprawdza godziny otwarcia
    - blokuje weekendy
    - kryptowaluty: 24/7
    """
    tz_name, open_time, close_time = MARKET_INFO.get(
        symbol, ("US/Eastern", time(9, 30), time(16, 0))
    )

    tz = pytz.timezone(tz_name)
    now_local = datetime.now(tz)

    # Kryptowaluty
    if open_time is None:
        return True

    # Weekendy → zamknięte
    if now_local.weekday() >= 5:
        return False

    # Futures (np. OIL) — mają sesję ciągłą 18:00 - 17:00 kolejnego dnia
    if open_time > close_time:
        if now_local.time() >= open_time or now_local.time() <= close_time:
            return True
        return False

    # Normalne godziny otwarcia
    return open_time <= now_local.time() <= close_time


def get_intraday_data(symbol, interval="5m"):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="7d", interval=interval)
        
        result = []
        for idx, row in data.iterrows():
            day_name = POLISH_DAYS[idx.weekday()]
            result.append({
                "time": idx.strftime("%H:%M"),
                "day": day_name,
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
                "volume": int(row["Volume"]),
            })
        return result
    except Exception as e:
        print(f"Błąd pobierania danych intraday dla {symbol}: {e}")
        return []


def interpolate_data(data, target_points):
    if len(data) <= 1:
        return data
    
    if len(data) >= target_points:
        step = len(data) // target_points
        return data[::step]
    
    interpolated = [data[0]]
    for i in range(len(data) - 1):
        current = data[i]
        next_point = data[i + 1]
        
        steps_between = (target_points - len(data)) // (len(data) - 1)
        
        for j in range(1, steps_between + 1):
            ratio = j / (steps_between + 1)
            interpolated.append({
                "date": current["date"],
                "close": round(current["close"] + (next_point["close"] - current["close"]) * ratio, 2),
                "high": round(current["high"] + (next_point["high"] - current["high"]) * ratio, 2),
                "low": round(current["low"] + (next_point["low"] - current["low"]) * ratio, 2),
            })
        
        interpolated.append(next_point)
    
    return interpolated


def get_historical_data(symbol, period="1mo", target_points=None):
    try:
        ticker = yf.Ticker(symbol)
        
        actual_period = "5d" if period == "1d" else period
        data = ticker.history(period=actual_period)
        
        if data.empty:
            return [], 0, 0
        
        result = []
        for idx, row in data.iterrows():
            result.append({
                "date": idx.strftime("%Y-%m-%d"),
                "close": round(row["Close"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
            })
        
        if period == "1d" and len(result) > 0:
            last_date = result[-1]["date"]
            result = [r for r in result if r["date"] == last_date]
        
        if target_points:
            result = interpolate_data(result, target_points)
        
        if not result:
            return [], 0, 0
            
        closes = [r["close"] for r in result]
        return result, min(closes), max(closes)
    except Exception as e:
        print(f"Błąd pobierania danych historycznych dla {symbol}: {e}")
        return [], 0, 0


def get_rate_info(symbol, name, code):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d")
        
        if not data.empty:
            prev_close = data["Close"].iloc[-2] if len(data) > 1 else data["Close"].iloc[0]
            curr_close = data["Close"].iloc[-1]
            change_pct = ((curr_close - prev_close) / prev_close) * 100
            rate = f"{change_pct:+.2f}%"
        else:
            rate = "n/d"
        
        return {"name": name, "code": code, "rate": rate}
    except Exception as e:
        print(f"Błąd pobierania info dla {symbol}: {e}")
        return {"name": name, "code": code, "rate": "n/d"}


@stockmarket_bp.route("/")
def stockmarket():
    indices = [
        ("^GSPC", "S&P 500", "SPX", "Indeksy", "USD"),
        ("^GDAXI", "DAX", "DAX", "Indeksy", "EUR"),
        ("^N100", "NASDAQ 100", "NDX", "Indeksy", "USD"),
        ("^FTSE", "FTSE 100", "FTSE", "Indeksy", "GBP"),

        ("GC=F", "Złoto", "GOLD", "Surowce", "USD"),
        ("CL=F", "Ropa WTI", "OIL", "Surowce", "USD"),
        ("NG=F", "Gaz naturalny", "GAS", "Surowce", "USD"),
        ("SI=F", "Srebro", "SILVER", "Surowce", "USD"),

        ("BTC-USD", "Bitcoin", "BTC", "Kryptowaluty", "USD"),
        ("ETH-USD", "Ethereum", "ETH", "Kryptowaluty", "USD"),
    ]
    
    intraday_data = {}
    sample_rates = []
    historical_data = {}
    
    time_range = request.args.get("range", "1mo")
    if time_range not in ["1d", "5d", "1mo", "1y"]:
        time_range = "1mo"
    
    target_points_map = {
        "1d": 20,
        "5d": 30,
        "1mo": 60,
        "1y": 254,
    }
    target_points = target_points_map.get(time_range, 60)
    
    for symbol, name, code, category, currency in indices:
        data_list = get_intraday_data(symbol)
        intraday_data[symbol] = data_list[-5:] if data_list else []

        hist_data, min_val, max_val = get_historical_data(symbol, time_range, target_points)
        historical_data[symbol] = {
            "data": hist_data,
            "min": min_val,
            "max": max_val
        }
        
        rate_info = get_rate_info(symbol, name, code)
        rate_info["is_open"] = is_market_open_for_symbol(symbol)
        rate_info["symbol"] = symbol
        rate_info["category"] = category
        rate_info["currency"] = currency
        sample_rates.append(rate_info)
    
    now = datetime.now()
    day_name = POLISH_DAYS[now.weekday()]
    formatted_time = f"{day_name}, {now.strftime('%d.%m.%Y %H:%M:%S')}"
    
    global_status = "OTWARTA ✓" if any(r["is_open"] for r in sample_rates) else "ZAMKNIĘTA ✗"
    
    return render_template(
        "stockmarket.html",
        rates=sample_rates,
        intraday_data=intraday_data,
        historical_data=historical_data,
        update_time=formatted_time,
        market_status=global_status,
        is_market_open=any(r["is_open"] for r in sample_rates),
        current_range=time_range,
    )
