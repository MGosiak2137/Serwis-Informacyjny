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
