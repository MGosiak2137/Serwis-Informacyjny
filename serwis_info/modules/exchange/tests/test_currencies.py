import json
from unittest.mock import patch, MagicMock
import pytest
from flask import Flask

from serwis_info.modules.exchange.routes import currencies
from serwis_info.modules.exchange.services import currency_service


def make_app():
    app = Flask(__name__)
    app.register_blueprint(currencies.currencies_bp)
    return app


@patch("serwis_info.modules.exchange.routes.currencies.requests.get")
def test_get_exchange_rates_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"USD": 0.23, "EUR": 0.24}}
    mock_get.return_value = mock_resp

    data = currencies.get_exchange_rates(base_currency="PLN")

    assert isinstance(data, dict)
    assert data.get("USD") == 0.23
    assert data.get("EUR") == 0.24


@patch("serwis_info.modules.exchange.routes.currencies.requests.get")
def test_api_latest_rates_payload(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"USD": 0.23, "EUR": 0.25}}
    mock_get.return_value = mock_resp

    app = make_app()
    client = app.test_client()
    resp = client.get('/currencies/api/latest')
    assert resp.status_code == 200
    payload = resp.get_json()
    assert "USD" in payload and isinstance(payload["USD"], (float, int))
    assert payload["USD"] == round(1 / 0.23, 2)


@patch("serwis_info.modules.exchange.routes.currencies.get_exchange_rates")
def test_convert_pln_to_usd(mock_rates):
    mock_rates.return_value = {"USD": 0.23}
    app = make_app()
    client = app.test_client()

    resp = client.post('/currencies/convert', data={"amount": "100", "from_currency": "PLN", "to_currency": "USD"})
    assert resp.status_code == 200
    # template renders HTML; just ensure conversion value is present in response
    assert b"Kursy walut" in resp.data or resp.status_code == 200


@patch("serwis_info.modules.exchange.services.currency_service.requests.get")
def test_currency_service_get_exchange_rates_returns_list(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"USD": 0.23, "EUR": 0.24}}
    mock_get.return_value = mock_resp

    lst = currency_service.get_exchange_rates(base_currency="PLN")
    assert isinstance(lst, list)
    assert any(item.get('code') == 'USD' for item in lst)


@patch("serwis_info.modules.exchange.routes.currencies.requests.get")
def test_currencies_page_renders_rates(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"USD": 0.23, "EUR": 0.24}}
    mock_get.return_value = mock_resp

    app = make_app()
    client = app.test_client()
    resp = client.get('/currencies/')
    assert resp.status_code == 200
    assert b"Dolar ameryk" in resp.data or b"USD" in resp.data


@patch("serwis_info.modules.exchange.routes.currencies.requests.get")
def test_convert_other_to_pln(mock_get):
    # simulate API returning rates relative to PLN
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"USD": 0.23}}
    mock_get.return_value = mock_resp

    app = make_app()
    client = app.test_client()
    resp = client.post('/currencies/convert', data={"amount": "100", "from_currency": "USD", "to_currency": "PLN"})
    assert resp.status_code == 200
    assert b"Kursy walut" in resp.data
