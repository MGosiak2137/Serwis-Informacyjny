# tests/integration/test_horoscope_endpoints.py

def test_horoscope_page_returns_html(client, logged_in_user):
    """
    Integracyjny test endpointu HTML (login required)
    """
    response = client.get("/calendar/horoscope")

    assert response.status_code == 200
    assert b"<html" in response.data


def test_horoscope_api_returns_json(client, monkeypatch):
    """
    Integracyjny test endpointu API horoskopu
    """

    fake_response = {
        "zodiac_sign": "baran",
        "zodiac_name": "Baran ♈",
        "horoscope": "Testowy horoskop",
        "date": "2025-03-10",
        "sign": "aries",
        "success": True
    }

    monkeypatch.setattr(
        "serwis_info.modules.calendar.services.horoscope_service.get_horoscope",
        lambda sign: fake_response
    )

    response = client.get("/calendar/api/horoscope/baran")

    assert response.status_code == 200

    data = response.get_json()

    assert data["zodiac_sign"] == "baran"
    assert data["success"] is True
    assert "horoscope" in data


def test_all_zodiacs_api(client, monkeypatch):
    """
    Integracyjny test endpointu API - lista znaków
    """

    fake_data = {
        "available_signs": ["baran", "byk"],
        "polish_names": {
            "baran": "Baran ♈",
            "byk": "Byk ♉"
        }
    }

    monkeypatch.setattr(
        "serwis_info.modules.calendar.services.horoscope_service.get_available_zodiacs",
        lambda: fake_data
    )

    response = client.get("/calendar/api/horoscope")

    assert response.status_code == 200

    data = response.get_json()

    assert "available_signs" in data
    assert "baran" in data["available_signs"]
