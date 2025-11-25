from flask import Blueprint, render_template, request, jsonify
import yfinance as yf
from datetime import datetime, time
import pytz

stockmarket_bp = Blueprint("stockmarket", __name__, url_prefix="/stockmarket")

POLISH_DAYS = {
    0: "Poniedziałek", 1: "Wtorek", 2: "Środa", 3: "Czwartek",
    4: "Piątek", 5: "Sobota", 6: "Niedziela"
}

MARKET_INFO = {
    "^GSPC": ("US/Eastern", time(9, 30), time(16, 0)),
    "^N100": ("US/Eastern", time(9, 30), time(16, 0)),
    "^GDAXI": ("Europe/Berlin", time(9, 0), time(17, 30)),
    "^FTSE": ("Europe/London", time(8, 0), time(16, 30)),
    "GC=F": ("US/Eastern", time(18, 0), time(17, 0)),
    "CL=F": ("US/Eastern", time(18, 0), time(17, 0)),
    "NG=F": ("US/Eastern", time(18, 0), time(17, 0)),
    "SI=F": ("US/Eastern", time(18, 0), time(17, 0)),
    "BTC-USD": ("UTC", None, None),
    "ETH-USD": ("UTC", None, None),
}

try:
    from ..data.categories import CATEGORIES, MARKET_META
except Exception:
    try:
        from serwis_info.modules.exchange.data.categories import CATEGORIES, MARKET_META
    except Exception:
        CATEGORIES = {}
        MARKET_META = {}

try:
    _BASE_MARKET_INFO = MARKET_INFO.copy()
except NameError:
    _BASE_MARKET_INFO = {}

FINAL_MARKET_INFO = _BASE_MARKET_INFO.copy()
for cat_name, items in CATEGORIES.items():
    meta = MARKET_META.get(cat_name)
    if not meta:
        continue
    for entry in items:
        symbol = entry[0]
        FINAL_MARKET_INFO[symbol] = meta

def is_market_open_for_symbol(symbol):
    tz_name, open_time, close_time = FINAL_MARKET_INFO.get(symbol, ("US/Eastern", time(9, 30), time(16, 0)))
    tz = pytz.timezone(tz_name)
    now_local = datetime.now(tz)
    if open_time is None:
        return True
    if now_local.weekday() >= 5:
        return False
    if open_time > close_time:
        return now_local.time() >= open_time or now_local.time() <= close_time
    return open_time <= now_local.time() <= close_time

def get_intraday_data(symbol, interval="5m"):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="7d", interval=interval)
        result = []
        for idx, row in data.iterrows():
            result.append({
                "time": idx.strftime("%H:%M"),
                "day": POLISH_DAYS[idx.weekday()],
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
                "volume": int(row["Volume"]),
            })
        return result
    except Exception:
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
    except Exception:
        return [], 0, 0

def get_rate_info(symbol, name, code):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d")
        if not data.empty:
            prev_close = data["Close"].iloc[-2] if len(data) > 1 else data["Close"].iloc[0]
            curr_close = data["Close"].iloc[-1]
            change_pct = ((curr_close - prev_close) / prev_close) * 100
            return {"name": name, "code": code, "rate": f"{change_pct:+.2f}%", "price": round(curr_close, 2)}
        return {"name": name, "code": code, "rate": "n/d", "price": None}
    except Exception:
        return {"name": name, "code": code, "rate": "n/d", "price": None}

SYMBOL_META = {}
for cat_list_name, cat_list in CATEGORIES.items():
    for s, name, code, category, currency in cat_list:
        SYMBOL_META[s] = {"name": name, "code": code, "category": category, "currency": currency}

@stockmarket_bp.route("/")
def stockmarket():
    selected_category = request.args.get("category")
    symbols_param = request.args.get("symbols")
    selected_symbols = [s.strip() for s in symbols_param.split(",") if s.strip()] if symbols_param else []
    categories = list(CATEGORIES.keys())
    options_for_category = []
    if selected_category and selected_category in CATEGORIES:
        options_for_category = [{"symbol": s, "name": name, "code": code, "currency": currency}
                                for (s, name, code, category, currency) in CATEGORIES[selected_category]]

    intraday_data = {}
    sample_rates = []
    historical_data = {}

    time_range = request.args.get("range", "1mo")
    if time_range not in ["1d", "5d", "1mo", "1y"]:
        time_range = "1mo"
    target_points_map = {"1d": 20, "5d": 30, "1mo": 60, "1y": 254}
    target_points = target_points_map.get(time_range, 60)

    symbols_to_load = []
    if selected_symbols:
        for sym in selected_symbols:
            meta = SYMBOL_META.get(sym)
            if meta:
                symbols_to_load.append((sym, meta["name"], meta["code"], meta["category"], meta["currency"]))
            else:
                guess_currency = "PLN" if sym.endswith(".WA") else "USD"
                symbols_to_load.append((sym, sym, sym, "", guess_currency))

    for item in symbols_to_load:
        if len(item) == 5:
            symbol, name, code, category, currency = item
        else:
            symbol = item[0]
            name = item[1] if len(item) > 1 else symbol
            code = item[2] if len(item) > 2 else symbol
            category = item[3] if len(item) > 3 else ""
            currency = item[4] if len(item) > 4 else ""
        data_list = get_intraday_data(symbol)
        intraday_data[symbol] = data_list[-5:] if data_list else []
        hist_data, min_val, max_val = get_historical_data(symbol, time_range, target_points)
        historical_data[symbol] = {"data": hist_data, "min": min_val, "max": max_val}
        rate_info = get_rate_info(symbol, name, code)
        rate_info["is_open"] = is_market_open_for_symbol(symbol)
        rate_info["symbol"] = symbol
        rate_info["category"] = category
        rate_info["currency"] = currency
        sample_rates.append(rate_info)

    now = datetime.now()
    formatted_time = f"{POLISH_DAYS[now.weekday()]}, {now.strftime('%d.%m.%Y %H:%M:%S')}"
    global_status = "OTWARTA ✓" if sample_rates and any(r["is_open"] for r in sample_rates) else "BRAK DANYCH"

    return render_template("stockmarket.html",
                           rates=sample_rates,
                           intraday_data=intraday_data,
                           historical_data=historical_data,
                           update_time=formatted_time,
                           market_status=global_status,
                           is_market_open=any(r["is_open"] for r in sample_rates) if sample_rates else False,
                           current_range=time_range,
                           categories=categories,
                           options_for_category=options_for_category,
                           selected_category=selected_category,
                           selected_symbols=selected_symbols)

@stockmarket_bp.route("/data")
def data_for_symbols():
    symbols_param = request.args.get("symbols", "")
    time_range = request.args.get("range", "1mo")
    symbols = [s.strip() for s in symbols_param.split(",") if s.strip()]
    if time_range not in ["1d", "5d", "1mo", "1y"]:
        time_range = "1mo"
    target_points_map = {"1d": 20, "5d": 30, "1mo": 60, "1y": 254}
    target_points = target_points_map.get(time_range, 60)
    out = {}
    for sym in symbols:
        try:
            hist_data, min_v, max_v = get_historical_data(sym, period=time_range, target_points=target_points)
            out[sym] = {"data": hist_data, "min": min_v, "max": max_v}
        except Exception:
            out[sym] = {"data": [], "min": 0, "max": 0}
    return jsonify({"range": time_range, "historical": out})

@stockmarket_bp.route("/ticker")
def ticker_prices():
    TOP_TICKER = [("^GSPC", "S&P 500"), ("^GDAXI", "DAX"), ("^FTSE", "FTSE 100"), ("BTC-USD", "Bitcoin"), ("GC=F", "Gold")]
    out = []
    for sym, display in TOP_TICKER:
        try:
            info = get_rate_info(sym, display, sym)
            out.append({"symbol": sym, "name": display, "price": info.get("price"), "rate": info.get("rate"), "is_open": is_market_open_for_symbol(sym)})
        except Exception:
            out.append({"symbol": sym, "name": display, "price": None, "rate": "n/d", "is_open": False})
    return jsonify(out)