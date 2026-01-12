import os
import json
import threading
import time
import requests
import yfinance as yf
from datetime import datetime, timezone
from flask import Flask

app = Flask(__name__)

API_KEY = os.getenv("CURRENCY_API_KEY")
API_URL = "https://api.freecurrencyapi.com/v1/latest"

# Gold history cache settings
_CACHE_FILENAME = os.path.join(os.path.dirname(__file__), 'gold_history_cache.json')
_DEFAULT_HISTORY_DAYS = 90
_CACHE_UPDATE_INTERVAL = 120  # seconds (2 minutes)
_MAX_CACHE_POINTS = 2000  # keep recent points to avoid unbounded growth

# In-memory cache and synchronization
_GOLD_HISTORY_CACHE = []  # oldest->newest list of {'date': 'YYYY-MM-DD' or ISO, 'close': float}
_cache_lock = threading.Lock()
_updater_started = False

# Rates caching (to avoid blocking /main/api/exchange on slow network calls)
_LAST_RATES = (None, None)
_rates_lock = threading.Lock()

# Currency history cache settings (USD/PLN and EUR/PLN)
_CURRENCY_CACHE_FILENAME = os.path.join(os.path.dirname(__file__), 'currency_history_cache.json')
_CURRENCY_HISTORY_CACHE = {'USD_PLN': [], 'EUR_PLN': []}  # lists of {'date': 'YYYY-MM-DD' or ISO, 'rate': float}
_currency_lock = threading.Lock()


def _parse_date_to_dt(s: str):
    """Parse date string (YYYY-MM-DD or ISO datetime) into a timezone-aware UTC datetime."""
    try:
        # try ISO first
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt
    except Exception:
        try:
            # fallback to date-only
            dt = datetime.strptime(s, '%Y-%m-%d')
            return dt.replace(tzinfo=timezone.utc)
        except Exception:
            return None


def _normalize_and_sort_history(history_list):
    """Return sanitized list sorted oldest->newest by parsed datetime."""
    sanitized = []
    for it in history_list:
        if not isinstance(it, dict):
            continue
        d = it.get('date') or it.get('dt') or it.get('Date')
        c = it.get('close')
        try:
            c = float(c)
        except Exception:
            continue
        if not d:
            continue
        sanitized.append({'date': str(d), 'close': float(c)})

    # sort by parsed datetime if possible, else keep original order
    try:
        parsed = []
        for it in sanitized:
            dt = _parse_date_to_dt(it['date'])
            if dt is None:
                # put at end with epoch baseline so we don't crash
                dt = datetime.fromtimestamp(0, tz=timezone.utc)
            parsed.append((dt, it))
        parsed.sort(key=lambda x: x[0])
        return [it for dt, it in parsed]
    except Exception:
        return sanitized


def _log(msg: str):
    try:
        # prefer Flask logger if available
        from flask import current_app
        current_app.logger.debug(msg)
    except Exception:
        try:
            print(msg)
        except Exception:
            pass


def _load_cache_from_disk():
    global _GOLD_HISTORY_CACHE
    try:
        if os.path.exists(_CACHE_FILENAME):
            with open(_CACHE_FILENAME, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            if isinstance(data, list):
                sanitized = _normalize_and_sort_history(data)
                with _cache_lock:
                    _GOLD_HISTORY_CACHE = sanitized
                _log(f"Loaded gold history cache from disk ({len(sanitized)} items)")
                return
    except Exception as e:
        _log(f"Failed to load gold history cache: {e}")
    with _cache_lock:
        _GOLD_HISTORY_CACHE = []


def _save_cache_to_disk(history):
    try:
        tmp = _CACHE_FILENAME + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as fh:
            json.dump(history, fh, ensure_ascii=False)
        os.replace(tmp, _CACHE_FILENAME)
        _log(f"Saved gold history cache to disk ({len(history)} items)")
    except Exception as e:
        _log(f"Failed to save gold history cache: {e}")


def _fetch_gold_history_yf(days: int = _DEFAULT_HISTORY_DAYS):
    """Fetch history directly from yfinance (same behavior as previous get_gold_history)."""
    try:
        gold = yf.Ticker("GC=F")
        period = f"{days}d"
        hist = gold.history(period=period)
        if hist is None or hist.empty:
            return []
        result = []
        for idx, row in hist.iterrows():
            try:
                date_str = idx.strftime('%Y-%m-%d')
            except Exception:
                date_str = str(idx)
            close = row.get('Close') if 'Close' in row else None
            if close is None:
                continue
            try:
                result.append({'date': date_str, 'close': float(close)})
            except Exception:
                continue
        return result
    except Exception as e:
        _log(f"Error fetching gold history from yfinance: {e}")
        return []


def _fetch_current_price():
    """Try to fetch a near-real-time gold price (minute-level) and return float or None."""
    try:
        gold = yf.Ticker("GC=F")
        # try intraday minute price first
        hist = gold.history(period='1d', interval='1m')
        if hist is not None and not hist.empty:
            try:
                last = hist['Close'].iloc[-1]
                return float(last)
            except Exception:
                pass
        # fallback to daily close
        return get_gold_price()
    except Exception as e:
        _log(f"Error fetching current gold price: {e}")
        return None


def _append_current_price_to_cache():
    try:
        price = _fetch_current_price()
        if price is None:
            _log("No current price available; skipping append")
            return False
        now = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        entry = {'date': now, 'close': float(price)}
        with _cache_lock:
            # avoid adding duplicate consecutive entries (allow different timestamps)
            if _GOLD_HISTORY_CACHE and _GOLD_HISTORY_CACHE[-1]['close'] == entry['close'] and _GOLD_HISTORY_CACHE[-1]['date'] == entry['date']:
                return False
            _GOLD_HISTORY_CACHE.append(entry)
            # trim to max points
            if len(_GOLD_HISTORY_CACHE) > _MAX_CACHE_POINTS:
                _GOLD_HISTORY_CACHE[:] = _GOLD_HISTORY_CACHE[-_MAX_CACHE_POINTS:]
            to_save = list(_GOLD_HISTORY_CACHE)
        _save_cache_to_disk(to_save)
        _log(f"Appended current price to cache: {entry['date']} -> {entry['close']}")
        return True
    except Exception as e:
        _log(f"Error appending current price to cache: {e}")
        return False


def get_cached_latest_price():
    """Return the latest price from the in-memory cache (fast)."""
    try:
        with _cache_lock:
            if not _GOLD_HISTORY_CACHE:
                # try load from disk once
                _load_cache_from_disk()
                if not _GOLD_HISTORY_CACHE:
                    return None
            last = _GOLD_HISTORY_CACHE[-1]
            return float(last['close'])
    except Exception as e:
        _log(f"Error getting cached latest price: {e}")
        return None


def _updater_loop():
    # updater now appends current price every interval; once per day it also refreshes full history
    cycles = 0
    while True:
        try:
            # append latest gold price
            _append_current_price_to_cache()
            # append latest FX rates
            try:
                _append_current_rates_to_cache()
            except Exception as e:
                _log(f"Error appending FX rates to cache: {e}")
            cycles += 1
            # every 12 cycles (~24 minutes at 2-minute interval) attempt to refresh full historical series
            if cycles % 12 == 0:
                _update_cache_once(_DEFAULT_HISTORY_DAYS)
                try:
                    _update_currency_cache_once(_DEFAULT_HISTORY_DAYS)
                except Exception as e:
                    _log(f"Currency history updater error: {e}")
        except Exception as e:
            _log(f"Gold history updater error: {e}")
        time.sleep(_CACHE_UPDATE_INTERVAL) 


def _update_cache_once(days: int = _DEFAULT_HISTORY_DAYS):
    try:
        new = _fetch_gold_history_yf(days=days)
        if not new:
            _log("YF fetch returned no data; skipping cache update")
            return False
        with _cache_lock:
            # ensure we keep oldest->newest ordering
            _GOLD_HISTORY_CACHE = new
        _save_cache_to_disk(new)
        _log(f"Gold history cache updated ({len(new)} items)")
        return True
    except Exception as e:
        _log(f"Exception in _update_cache_once: {e}")
        return False




def _start_updater():
    global _updater_started
    if _updater_started:
        return
    _updater_started = True
    t = threading.Thread(target=_updater_loop, daemon=True, name='gold-history-updater')
    t.start()
    _log("Started gold history background updater thread")


def get_last_rates():
    """Return last cached (eur_pln, usd_pln) tuple."""
    try:
        with _rates_lock:
            return tuple(_LAST_RATES)
    except Exception:
        return (None, None)

# Initialize cache at import time
_load_cache_from_disk()
# currency cache will be loaded after helpers are defined to avoid calling before function exists
# Start background updater (will refresh disk cache every 5 minutes)
# Guard against Werkzeug reloader starting multiple processes when in debug mode.
try:
    if (not app.debug) or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        _start_updater()
    else:
        _log("Skipping updater startup in Werkzeug reloader parent process")
except Exception as e:
    _log(f"Failed to start updater: {e}")


# Public API: get_gold_history now prefers the in-memory cache (loaded from disk on startup),
# but will attempt to fetch fresh data when the cache is missing or too short.
def get_gold_history(days: int = _DEFAULT_HISTORY_DAYS):
    """Return list of historical gold close prices for the last `days` days.

    Behavior:
    - If the in-memory cache contains at least `days` entries, return the most recent `days` items from cache (oldest->newest).
    - Otherwise, attempt to fetch fresh data from yfinance, update cache/disk, and return it.
    - If fetch fails but disk cache exists, return whatever cache we have.
    """
    try:
        with _cache_lock:
            cached = list(_GOLD_HISTORY_CACHE)
        if cached and len(cached) >= days:
            # return only last `days` items (maintain oldest->newest)
            return cached[-days:]

        # try to fetch fresh
        fresh = _fetch_gold_history_yf(days=days)
        if fresh:
            with _cache_lock:
                _GOLD_HISTORY_CACHE[:] = fresh
            _save_cache_to_disk(fresh)
            return fresh

        # fallback to whatever cache we have (possibly shorter)
        if cached:
            return cached

        return []
    except Exception as e:
        _log(f"get_gold_history error: {e}")
        return []


# --- existing currency helpers (unchanged) ---

def get_currency_rates():
    # Use exchangerate.host public API to get reliable latest rates
    global LAST_RATES_DEBUG, _LAST_RATES
    LAST_RATES_DEBUG = ''
    try:
        url = "https://api.exchangerate.host/latest"
        # request rates with base PLN so we can compute EUR/PLN and USD/PLN as inverses
        params = {"base": "PLN", "symbols": "EUR,USD"}
        resp = requests.get(url, params=params, timeout=6)
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
                resp2 = requests.get(url, params=params2, timeout=6)
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
                resp3 = requests.get(API_URL, params=params3, timeout=6)
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

        # update cached rates for fast access
        try:
            with _rates_lock:
                _LAST_RATES = (eur_pln, usd_pln)
        except Exception:
            pass

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


# --- Currency cache helpers ---

def _load_currency_cache_from_disk():
    global _CURRENCY_HISTORY_CACHE
    try:
        if os.path.exists(_CURRENCY_CACHE_FILENAME):
            with open(_CURRENCY_CACHE_FILENAME, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                # sanitize each series
                usd = data.get('USD_PLN', [])
                eur = data.get('EUR_PLN', [])
                with _currency_lock:
                    _CURRENCY_HISTORY_CACHE['USD_PLN'] = [x for x in usd if isinstance(x, dict) and 'date' in x and 'rate' in x]
                    _CURRENCY_HISTORY_CACHE['EUR_PLN'] = [x for x in eur if isinstance(x, dict) and 'date' in x and 'rate' in x]
                _log(f"Loaded currency history cache from disk (USD:{len(_CURRENCY_HISTORY_CACHE['USD_PLN'])} EUR:{len(_CURRENCY_HISTORY_CACHE['EUR_PLN'])})")
                return
    except Exception as e:
        _log(f"Failed to load currency history cache: {e}")
    with _currency_lock:
        _CURRENCY_HISTORY_CACHE = {'USD_PLN': [], 'EUR_PLN': []}


def _save_currency_cache_to_disk(cache):
    try:
        tmp = _CURRENCY_CACHE_FILENAME + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as fh:
            json.dump(cache, fh, ensure_ascii=False)
        os.replace(tmp, _CURRENCY_CACHE_FILENAME)
        _log(f"Saved currency history cache to disk (USD:{len(cache.get('USD_PLN',[]))} EUR:{len(cache.get('EUR_PLN',[]))})")
    except Exception as e:
        _log(f"Failed to save currency history cache: {e}")


def _append_current_rates_to_cache():
    try:
        eur_pln, usd_pln = get_currency_rates()
        if eur_pln is None and usd_pln is None:
            _log("No current FX rates available; skipping append")
            return False
        now = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        with _currency_lock:
            if usd_pln is not None:
                uentry = {'date': now, 'rate': float(usd_pln)}
                if not _CURRENCY_HISTORY_CACHE['USD_PLN'] or _CURRENCY_HISTORY_CACHE['USD_PLN'][-1].get('rate') != uentry['rate'] or _CURRENCY_HISTORY_CACHE['USD_PLN'][-1].get('date') != uentry['date']:
                    _CURRENCY_HISTORY_CACHE['USD_PLN'].append(uentry)
                    if len(_CURRENCY_HISTORY_CACHE['USD_PLN']) > _MAX_CACHE_POINTS:
                        _CURRENCY_HISTORY_CACHE['USD_PLN'] = _CURRENCY_HISTORY_CACHE['USD_PLN'][-_MAX_CACHE_POINTS:]
            if eur_pln is not None:
                eentry = {'date': now, 'rate': float(eur_pln)}
                if not _CURRENCY_HISTORY_CACHE['EUR_PLN'] or _CURRENCY_HISTORY_CACHE['EUR_PLN'][-1].get('rate') != eentry['rate'] or _CURRENCY_HISTORY_CACHE['EUR_PLN'][-1].get('date') != eentry['date']:
                    _CURRENCY_HISTORY_CACHE['EUR_PLN'].append(eentry)
                    if len(_CURRENCY_HISTORY_CACHE['EUR_PLN']) > _MAX_CACHE_POINTS:
                        _CURRENCY_HISTORY_CACHE['EUR_PLN'] = _CURRENCY_HISTORY_CACHE['EUR_PLN'][-_MAX_CACHE_POINTS:]
            # make a copy for disk
            to_save = {'USD_PLN': list(_CURRENCY_HISTORY_CACHE['USD_PLN']), 'EUR_PLN': list(_CURRENCY_HISTORY_CACHE['EUR_PLN'])}
        _save_currency_cache_to_disk(to_save)
        _log(f"Appended current FX rates to cache: eur_pln={eur_pln} usd_pln={usd_pln}")
        return True
    except Exception as e:
        _log(f"Error appending FX rates to cache: {e}")
        return False


def _update_currency_cache_once(days: int = 90):
    try:
        # attempt to fetch full timeseries for both USD_PLN and EUR_PLN using existing network helper
        usd = get_currency_history('USD', 'PLN', days)
        eur = get_currency_history('EUR', 'PLN', days)
        # normalize shape to {'date', 'rate'} and sort oldest->newest
        def norm(lst):
            out = []
            for it in lst:
                if not isinstance(it, dict):
                    continue
                d = it.get('date')
                r = it.get('rate') or it.get('close') or it.get('value')
                try:
                    r = float(r)
                except Exception:
                    continue
                if not d:
                    continue
                out.append({'date': str(d), 'rate': float(r)})
            # sort by date if possible
            try:
                out.sort(key=lambda x: _parse_date_to_dt(x['date']) or datetime.fromtimestamp(0, tz=timezone.utc))
            except Exception:
                pass
            return out
        usd_norm = norm(usd)
        eur_norm = norm(eur)
        with _currency_lock:
            if usd_norm:
                _CURRENCY_HISTORY_CACHE['USD_PLN'] = usd_norm
            if eur_norm:
                _CURRENCY_HISTORY_CACHE['EUR_PLN'] = eur_norm
            to_save = {'USD_PLN': list(_CURRENCY_HISTORY_CACHE['USD_PLN']), 'EUR_PLN': list(_CURRENCY_HISTORY_CACHE['EUR_PLN'])}
        _save_currency_cache_to_disk(to_save)
        _log(f"Currency history cache updated (USD:{len(usd_norm)} EUR:{len(eur_norm)})")
        return True
    except Exception as e:
        _log(f"Exception in _update_currency_cache_once: {e}")
        return False


def get_cached_currency_history(base: str, symbol: str, days: int = 30):
    """Return cached currency history for base->symbol (oldest->newest). If cache is too short, try to fetch fresh timeseries and update cache."""
    key = None
    if base.upper() == 'USD' and symbol.upper() == 'PLN':
        key = 'USD_PLN'
    elif base.upper() == 'EUR' and symbol.upper() == 'PLN':
        key = 'EUR_PLN'
    else:
        # not a cached pair — fall back to network fetch
        return get_currency_history(base, symbol, days)
    try:
        with _currency_lock:
            cached = list(_CURRENCY_HISTORY_CACHE.get(key, []))
        if cached and len(cached) >= days:
            return cached[-days:]
        # else try to fetch fresh timeseries and update cache
        fresh = get_currency_history(base, symbol, days)
        if fresh:
            # normalized by _update_currency_cache_once logic
            normed = []
            for it in fresh:
                if not isinstance(it, dict):
                    continue
                d = it.get('date')
                r = it.get('rate') or it.get('value') or it.get('close')
                try:
                    r = float(r)
                except Exception:
                    continue
                if not d:
                    continue
                normed.append({'date': str(d), 'rate': float(r)})
            try:
                with _currency_lock:
                    _CURRENCY_HISTORY_CACHE[key] = normed
                    to_save = {'USD_PLN': list(_CURRENCY_HISTORY_CACHE['USD_PLN']), 'EUR_PLN': list(_CURRENCY_HISTORY_CACHE['EUR_PLN'])}
                _save_currency_cache_to_disk(to_save)
            except Exception:
                pass
            return normed
        # fallback to cached (possibly shorter)
        if cached:
            return cached
        return []
    except Exception as e:
        _log(f"get_cached_currency_history error: {e}")
        return []


# Ensure currency cache is loaded after helpers are defined
try:
    _load_currency_cache_from_disk()
except Exception:
    pass

# Spawn a non-blocking initial append of FX rates so we persist a starting point immediately
try:
    threading.Thread(target=_append_current_rates_to_cache, daemon=True).start()
except Exception:
    pass

if __name__ == "__main__":
    app.run(debug=True)
