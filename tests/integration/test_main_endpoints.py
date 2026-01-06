# tests/integration/test_main_endpoints.py

import serwis_info.modules.main.routes.main as main_routes


def test_main_index_returns_html(client, monkeypatch):
    """
    Integracyjny test endpointu HTML /
    """

    monkeypatch.setattr(
        main_routes,
        "_load_news_preview",
        lambda limit=3: [{"title": "Test news"}]
    )

    response = client.get("/main/")

    assert response.status_code == 200
    assert b"<html" in response.data


def test_calendar_api_returns_json(client, monkeypatch):
    fake_data = {
        "date": "1 stycznia 2025",
        "day_of_year": 1,
        "namedays": ["Test"],
        "is_holiday": False,
        "holiday_name": None,
    }

    monkeypatch.setattr(
        "serwis_info.modules.main.routes.calendar_service.get_calendar_data",
        lambda: fake_data
    )

    response = client.get("/main/api/calendar")

    assert response.status_code == 200
    assert "date" in response.get_json()


def test_exchange_api_returns_json(client, monkeypatch):
    monkeypatch.setattr(
        "serwis_info.modules.main.routes.exchange_service.get_currency_rates",
        lambda: (4.0, 3.8)
    )
    monkeypatch.setattr(
        "serwis_info.modules.main.routes.exchange_service.get_gold_price",
        lambda: 280.0
    )
    monkeypatch.setattr(
        "serwis_info.modules.main.routes.exchange_service.get_gold_history",
        lambda days: []
    )
    monkeypatch.setattr(
        "serwis_info.modules.main.routes.exchange_service.get_currency_history",
        lambda a, b, days: []
    )

    response = client.get("/main/api/exchange")

    assert response.status_code == 200

    data = response.get_json()

    assert "eur_pln" in data
    assert "usd_pln" in data
    assert "gold_price" in data
