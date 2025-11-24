from datetime import time

CATEGORIES = {
    "Indeksy - Global": [
        ("^GSPC", "S&P 500", "S&P 500", "Indeksy - Global", "USD"),
        ("^DJI", "Dow Jones Industrial Average", "DJI", "Indeksy - Global", "USD"),
        ("^IXIC", "NASDAQ Composite", "NASDAQ", "Indeksy - Global", "USD"),
        ("^NDX", "NASDAQ-100 (NDX)", "NDX", "Indeksy - Global", "USD"),
        ("^N225", "Nikkei 225", "Nikkei", "Indeksy - Global", "JPY"),
        ("^HSI", "Hang Seng Index", "HSI", "Indeksy - Global", "HKD"),
        ("^SSEC", "Shanghai Composite", "SSEC", "Indeksy - Global", "CNY"),
        ("^FTSE", "FTSE 100", "FTSE", "Indeksy - Global", "GBP"),
        ("^GDAXI", "DAX", "DAX", "Indeksy - Global", "EUR"),
        ("^FCHI", "CAC 40", "CAC40", "Indeksy - Global", "EUR"),
        ("^STOXX50E", "Euro STOXX 50", "STOXX50", "Indeksy - Global", "EUR"),
        ("^WIG20", "WIG20", "WIG20", "Indeksy - Global", "PLN"),
        ("^IBEX", "IBEX 35", "IBEX35", "Indeksy - Global", "EUR"),
        ("^AXJO", "S&P/ASX 200", "ASX200", "Indeksy - Global", "AUD"),
        ("^KS11", "KOSPI", "KOSPI", "Indeksy - Global", "KRW"),
        ("^GSPTSE", "S&P/TSX Composite", "TSX", "Indeksy - Global", "CAD"),
        ("^BVSP", "Bovespa (IBOV)", "BOVESPA", "Indeksy - Global", "BRL"),
        ("^MXX", "IPC Mexico", "IPC", "Indeksy - Global", "MXN"),
        ("BTC-USD", "Bitcoin (index/spot)", "BTC", "Indeksy - Global", "USD"),
        ("GC=F", "Gold (Futures)", "GOLD", "Indeksy - Global", "USD"),
    ],

    "Akcje - Polskie": [
        ("PKO.WA", "PKO BP", "PKO", "Akcje - Polskie", "PLN"),
        ("PKN.WA", "PKN Orlen", "PKN", "Akcje - Polskie", "PLN"),
        ("PZU.WA", "PZU", "PZU", "Akcje - Polskie", "PLN"),
        ("LPP.WA", "LPP", "LPP", "Akcje - Polskie", "PLN"),
        ("CDR.WA", "CD Projekt", "CDR", "Akcje - Polskie", "PLN"),
        ("KGH.WA", "KGHM", "KGH", "Akcje - Polskie", "PLN"),
        ("PGE.WA", "PGE", "PGE", "Akcje - Polskie", "PLN"),
        ("JSW.WA", "JSW", "JSW", "Akcje - Polskie", "PLN"),
        ("CCC.WA", "CCC", "CCC", "Akcje - Polskie", "PLN"),
    ],

    "Akcje - Amerykańskie": [
        ("AAPL", "Apple", "AAPL", "Akcje - Amerykańskie", "USD"),
        ("MSFT", "Microsoft", "MSFT", "Akcje - Amerykańskie", "USD"),
        ("AMZN", "Amazon", "AMZN", "Akcje - Amerykańskie", "USD"),
        ("GOOGL", "Alphabet (Class A)", "GOOGL", "Akcje - Amerykańskie", "USD"),
        ("META", "Meta Platforms", "META", "Akcje - Amerykańskie", "USD"),
        ("TSLA", "Tesla", "TSLA", "Akcje - Amerykańskie", "USD"),
        ("NVDA", "NVIDIA", "NVDA", "Akcje - Amerykańskie", "USD"),
        ("JPM", "JPMorgan Chase", "JPM", "Akcje - Amerykańskie", "USD"),
        ("WMT", "Walmart", "WMT", "Akcje - Amerykańskie", "USD"),
    ],

    "Akcje - Europejskie": [
        ("SAP.DE", "SAP (DE)", "SAP", "Akcje - Europejskie", "EUR"),
        ("ADS.DE", "Adidas (DE)", "ADS", "Akcje - Europejskie", "EUR"),
        ("SAN.PA", "Santander (FR/PA)", "SAN", "Akcje - Europejskie", "EUR"),
        ("RDSA.AS", "Shell (AS)", "RDSA", "Akcje - Europejskie", "EUR"),
        ("VOW3.DE", "Volkswagen (DE)", "VOW", "Akcje - Europejskie", "EUR"),
        ("ULVR.L", "Unilever (LON)", "ULVR", "Akcje - Europejskie", "GBP"),
    ],

    "Akcje - Azjatyckie": [
        ("9988.HK", "Alibaba (HK)", "9988", "Akcje - Azjatyckie", "HKD"),
        ("0700.HK", "Tencent (HK)", "0700", "Akcje - Azjatyckie", "HKD"),
        ("TSM", "TSMC (ADR)", "TSM", "Akcje - Azjatyckie", "USD"),
        ("6758.T", "Sony (TYO)", "6758", "Akcje - Azjatyckie", "JPY"),
        ("9984.T", "SoftBank (TYO)", "9984", "Akcje - Azjatyckie", "JPY"),
    ],

    "Surowce": [
        ("GC=F", "Gold Futures", "GOLD", "Surowce", "USD"),
        ("SI=F", "Silver Futures", "SILVER", "Surowce", "USD"),
        ("CL=F", "Crude Oil WTI", "OIL", "Surowce", "USD"),
        ("NG=F", "Natural Gas", "GAS", "Surowce", "USD"),
        ("HG=F", "Copper Futures", "COPPER", "Surowce", "USD"),
        ("PL=F", "Platinum Futures", "PLATINUM", "Surowce", "USD"),
        ("PA=F", "Palladium Futures", "PALLADIUM", "Surowce", "USD"),
        ("RB=F", "RBOB Gasoline Futures", "RBOB", "Surowce", "USD"),
        ("HO=F", "Heating Oil Futures", "HEATING_OIL", "Surowce", "USD"),
        ("ZC=F", "Corn Futures", "CORN", "Surowce", "USD"),
        ("ZS=F", "Soybeans Futures", "SOYBEANS", "Surowce", "USD"),
        ("KC=F", "Coffee Futures", "COFFEE", "Surowce", "USD"),
        ("SB=F", "Sugar Futures", "SUGAR", "Surowce", "USD"),
        ("CC=F", "Cocoa Futures", "COCOA", "Surowce", "USD"),
        ("LBS=F", "Cotton Futures", "COTTON", "Surowce", "USD"),
        ("XAUUSD=X", "Gold (spot)", "GOLD_SPOT", "Surowce", "USD"),
        ("XAGUSD=X", "Silver (spot)", "SILVER_SPOT", "Surowce", "USD"),
    ],

    "Krypto": [
        ("BTC-USD", "Bitcoin", "BTC", "Kryptowaluty", "USD"),
        ("ETH-USD", "Ethereum", "ETH", "Kryptowaluty", "USD"),
        ("BNB-USD", "Binance Coin", "BNB", "Kryptowaluty", "USD"),
        ("ADA-USD", "Cardano", "ADA", "Kryptowaluty", "USD"),
        ("SOL-USD", "Solana", "SOL", "Kryptowaluty", "USD"),
        ("DOGE-USD", "Dogecoin", "DOGE", "Kryptowaluty", "USD"),
        ("XRP-USD", "XRP", "XRP", "Kryptowaluty", "USD"),
        ("LTC-USD", "Litecoin", "LTC", "Kryptowaluty", "USD"),
        ("LINK-USD", "Chainlink", "LINK", "Kryptowaluty", "USD"),
    ],
}

# MARKET_META: timezone + open_time + close_time for categories (used to compute is_open)
MARKET_META = {
    "Indeksy - Global": ("UTC", None, None),  # leave as 24/7 (no blocking) to avoid false closed states
    "Akcje - Polskie": ("Europe/Warsaw", time(9, 0), time(16, 50)),
    "Akcje - Amerykańskie": ("US/Eastern", time(9, 30), time(16, 0)),
    "Akcje - Europejskie": ("Europe/Berlin", time(9, 0), time(17, 30)),
    "Akcje - Azjatyckie": ("Asia/Tokyo", time(9, 0), time(15, 0)),
    "Surowce": ("US/Eastern", time(18, 0), time(17, 0)),   # futures: 18:00 - 17:00 next day
    "Krypto": ("UTC", None, None),
}
