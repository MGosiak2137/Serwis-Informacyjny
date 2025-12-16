import datetime
from unittest.mock import patch

import pytest

from serwis_info.modules.exchange.routes import stockmarket


class DummySeries:
	def __init__(self, lst):
		self._lst = lst

	@property
	def iloc(self):
		return self

	def __getitem__(self, idx):
		return self._lst[idx]


class DummyDF:
	def __init__(self, rows):
		self._rows = list(rows)
		self.empty = len(self._rows) == 0
		self._closes = [r[1]["Close"] for r in self._rows] if self._rows else []

	def iterrows(self):
		return iter(self._rows)

	def __len__(self):
		return len(self._rows)

	def __getitem__(self, key):
		if key == "Close":
			return DummySeries(self._closes)
		raise KeyError


def _idx(dt_str):
	return datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

def test_is_market_open_btc_true():
	assert stockmarket.is_market_open_for_symbol("BTC-USD") is True

def test_interpolate_expands_and_keeps_ends():
	data = [
		{"date": "2025-01-01", "close": 100.0, "high": 101.0, "low": 99.0},
		{"date": "2025-01-02", "close": 110.0, "high": 111.0, "low": 109.0},
	]
	out = stockmarket.interpolate_data(data, target_points=5)
	assert len(out) > 2
	assert out[0]["close"] == 100.0
	assert out[-1]["close"] == 110.0

def test_interpolate_downsamples_simple():
	data = [{"date": str(i), "close": float(i), "high": float(i), "low": float(i)} for i in range(10)]
	out = stockmarket.interpolate_data(data, target_points=5)
	assert len(out) == 5

@patch("serwis_info.modules.exchange.routes.stockmarket.yf")
def test_get_intraday_parsing(mock_yf):
	rows = [
		(_idx("2025-12-15 10:00:00"), {"Open": 100.0, "High": 101.0, "Low": 99.0, "Close": 100.5, "Volume": 1000}),
	]
	mock_yf.Ticker.return_value.history.return_value = DummyDF(rows)
	res = stockmarket.get_intraday_data("FAKE", interval="5m")
	assert isinstance(res, list)
	assert res[0]["close"] == round(100.5, 2)

@patch("serwis_info.modules.exchange.routes.stockmarket.yf")
def test_get_historical_min_max(mock_yf):
	rows = [
		(_idx("2025-12-01 00:00:00"), {"Close": 90.0, "High": 95.0, "Low": 85.0}),
		(_idx("2025-12-02 00:00:00"), {"Close": 110.0, "High": 115.0, "Low": 108.0}),
	]
	mock_yf.Ticker.return_value.history.return_value = DummyDF(rows)
	hist, mn, mx = stockmarket.get_historical_data("FAKE", period="1mo")
	assert mn == 90.0
	assert mx == 110.0

@patch("serwis_info.modules.exchange.routes.stockmarket.yf")
def test_get_rate_info_exact_percentage(mock_yf):
	rows = [
		(_idx("2025-12-01 00:00:00"), {"Close": 100.0}),
		(_idx("2025-12-02 00:00:00"), {"Close": 110.0}),
	]
	mock_yf.Ticker.return_value.history.return_value = DummyDF(rows)
	info = stockmarket.get_rate_info("FAKE", "Name", "CODE")
	assert info["price"] == 110.0
	assert info["rate"] == "+10.00%"

@patch("serwis_info.modules.exchange.routes.stockmarket.yf")
def test_get_historical_empty_returns_defaults(mock_yf):
	mock_yf.Ticker.return_value.history.return_value = DummyDF([])
	hist, mn, mx = stockmarket.get_historical_data("EMPTY", period="1mo")
	assert hist == []
	assert mn == 0
	assert mx == 0

@patch("serwis_info.modules.exchange.routes.stockmarket.is_market_open_for_symbol")
@patch("serwis_info.modules.exchange.routes.stockmarket.get_rate_info")
def test_ticker_prices_json_structure(mock_get_rate, mock_is_open):
	mock_get_rate.return_value = {"name": "N", "code": "C", "rate": "+1.23%", "price": 123.45}
	mock_is_open.return_value = True
	from flask import Flask
	app = Flask(__name__)
	with app.test_request_context():
		resp = stockmarket.ticker_prices()
		data = resp.get_json()
		assert isinstance(data, list)
		assert all(isinstance(item, dict) for item in data)
		assert all("symbol" in item and "price" in item and "rate" in item for item in data)


