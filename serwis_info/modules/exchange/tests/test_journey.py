from unittest.mock import patch, MagicMock
import pytest
from flask import Flask
from serwis_info.modules.exchange.routes import journey
from datetime import datetime


def make_app():
    app = Flask(__name__)
    app.register_blueprint(journey.journey_bp)
    return app


def test_safe_parse_iso_valid_and_invalid():
    assert journey.safe_parse_iso("2025-12-01T10:00:00Z") is not None
    assert journey.safe_parse_iso("not-a-date") is None


@patch("serwis_info.modules.exchange.routes.journey.translator.translate")
def test_translate_to_english_fallback_on_error(mock_translate):
    mock_translate.side_effect = Exception("fail")
    assert journey.translate_to_english("Warszawa") == "Warszawa"


@patch("serwis_info.modules.exchange.routes.journey.requests.get")
def test_get_iata_code_returns_airport_code(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"data": {"searchItems": [{"type": "AIRPORT", "id": "waw"}]}}
    mock_get.return_value = mock_resp

    code = journey.get_iata_code("Warszawa")
    assert isinstance(code, str)
    assert len(code) == 3


def test_parse_segment_times_duration_and_stops():
    # build minimal slices
    dep = {"departInfo": {"airport": {"code": "WAW"}, "time": {"dateTime": "2025-12-01T10:00:00Z"}}}
    arr = {"arrivalInfo": {"airport": {"code": "LHR"}, "time": {"dateTime": "2025-12-01T12:30:00Z"}}}
    slice_data = {"segments": [dep, arr]}

    dep_airport, arr_airport, dep_time_fmt, arr_time_fmt, duration, stops = journey.parse_segment_times(slice_data)
    assert dep_airport == "WAW"
    assert arr_airport == "LHR"
    assert "h" in duration
    assert stops == 1


@patch("serwis_info.modules.exchange.routes.journey.requests.get")
def test_fetch_hotels_handles_api_error(mock_get):
    mock_get.side_effect = Exception("network")
    assert journey.fetch_hotels("id", "2025-12-01", "2025-12-05", 2) == []


@patch("serwis_info.modules.exchange.routes.journey.requests.get")
def test_fetch_flights_oneway_returns_empty_on_error(mock_get):
    mock_get.side_effect = Exception("network")
    assert journey.fetch_flights_oneway("WAW", "LHR", "2025-12-01", "ECO", 1) == []


@patch("serwis_info.modules.exchange.routes.journey.requests.get")
def test_fetch_flights_oneway_parses_listings(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "data": {
            "listings": [
                {"totalPriceWithDecimal": {"price": 100}, "airlines": [{"name": "A"}]},
                {"totalPriceWithDecimal": {"price": 200}, "airlines": [{"name": "B"}]}
            ]
        }
    }
    mock_get.return_value = mock_resp

    res = journey.fetch_flights_oneway("WAW", "LHR", "2025-12-01", "ECO", 1)
    assert isinstance(res, list)
    assert len(res) >= 1


@patch("serwis_info.modules.exchange.routes.journey.render_template")
@patch("serwis_info.modules.exchange.routes.journey.translate_to_english")
@patch("serwis_info.modules.exchange.routes.journey.requests.get")
def test_journey_route_basic_flow(mock_get, mock_translate, mock_render):
    mock_translate.side_effect = lambda x: x
    mock_render.return_value = "HTML content"

    # Mock API call
    def side_effect(url, *args, **kwargs):
        if "api.nbp.pl" in url:
            mock = MagicMock()
            mock.status_code = 200
            mock.json.return_value = {"rates":[{"mid":4.2}]}
            return mock
        elif "booking-com.p.rapidapi.com" in url:
            mock = MagicMock()
            mock.status_code = 200
            mock.json.return_value = {"result":[{"hotel_name":"Test","address_trans":"Addr","min_total_price":100,"review_score":9.0,"max_photo_url":""}]}
            return mock
        else:
            mock = MagicMock()
            mock.status_code = 200
            mock.json.return_value = {"data":{"listings":[{"totalPriceWithDecimal":{"price":100},"airlines":[{"name":"A"}],"slices":[{"segments":[{"departInfo":{"airport":{"code":"WAW"},"time":{"dateTime":"2025-12-01T10:00:00Z"}}},{"arrivalInfo":{"airport":{"code":"LHR"},"time":{"dateTime":"2025-12-01T12:30:00Z"}}}]}]}]}}
            return mock

    mock_get.side_effect = side_effect

    app = make_app()
    client = app.test_client()
    resp = client.get('/journey/?origin=WAW&destination=LHR&date_from=2025-12-01&date_to=2025-12-02')

    assert resp.status_code == 200
    assert resp.data == b"HTML content"
