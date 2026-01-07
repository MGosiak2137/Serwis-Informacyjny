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
@patch("serwis_info.modules.exchange.routes.currencies.render_template")
def test_convert_pln_to_usd(mock_render, mock_rates):
    mock_rates.return_value = {
        "USD": 0.23, "EUR": 0.24, "GBP": 0.25, "CHF": 0.26,
        "JPY": 0.002, "CZK": 0.18, "NOK": 0.19, "SEK": 0.20,
        "DKK": 0.21, "HUF": 0.0012, "CNY": 0.15, "AUD": 0.17, "CAD": 0.18
    }

    # render_template zwraca zwykły string zamiast próbować załadować plik
    mock_render.return_value = "HTML content"

    app = make_app()
    client = app.test_client()

    resp = client.post('/currencies/convert', data={"amount": "100", "from_currency": "PLN", "to_currency": "USD"})
    assert resp.status_code == 200
    assert resp.data == b"HTML content"



@patch("serwis_info.modules.exchange.services.currency_service.requests.get")
def test_currency_service_get_exchange_rates_returns_list(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"USD": 0.23, "EUR": 0.24}}
    mock_get.return_value = mock_resp

    lst = currency_service.get_exchange_rates(base_currency="PLN")
    assert isinstance(lst, list)
    assert any(item.get('code') == 'USD' for item in lst)


@patch("serwis_info.modules.exchange.routes.currencies.requests.get")
@patch("serwis_info.modules.exchange.routes.currencies.render_template")
def test_currencies_page_renders_rates(mock_render, mock_get):
    # mock API response
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"USD": 0.23, "EUR": 0.24}}
    mock_get.return_value = mock_resp

    # zamiast renderować rzeczywisty template
    mock_render.return_value = "HTML content"

    app = make_app()
    client = app.test_client()
    resp = client.get('/currencies/')

    assert resp.status_code == 200
    assert resp.data == b"HTML content"


@patch("serwis_info.modules.exchange.routes.currencies.requests.get")
@patch("serwis_info.modules.exchange.routes.currencies.render_template")
def test_convert_other_to_pln(mock_render, mock_get):
    # mock API response
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"USD": 0.23}}
    mock_get.return_value = mock_resp

    # mock template render
    mock_render.return_value = "HTML content"

    app = make_app()
    client = app.test_client()
    resp = client.post('/currencies/convert', data={"amount": "100", "from_currency": "USD", "to_currency": "PLN"})

    assert resp.status_code == 200
    assert resp.data == b"HTML content"

