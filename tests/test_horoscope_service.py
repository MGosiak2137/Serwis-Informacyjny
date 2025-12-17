# tests/test_horoscope_service.py
import pytest
from serwis_info.modules.calendar.services import horoscope_service

# =========================
# TESTY CZYSTEJ LOGIKI (UNIT)
# =========================

def test_get_available_zodiacs():
    result = horoscope_service.get_available_zodiacs()
    assert "available_signs" in result
    assert "polish_names" in result
    assert "baran" in result["available_signs"]
    assert result["polish_names"]["lew"] == "Lew ♌"


def test_get_horoscope_invalid_sign():
    result = horoscope_service.get_horoscope("invalid")
    assert "error" in result

# =========================
# MOCK REQUESTS – API HOROSKOPU
# =========================

def test_get_horoscope_primary_api_success(mocker):
    fake_response = {
        "success": True,
        "data": {
            "horoscope_data": "Today is a great day",
            "date": "2025-01-01",
            "sign": "aries"
        }
    }

    mocker.patch(
        "serwis_info.modules.calendar.services.horoscope_service.requests.get",
        return_value=mocker.Mock(status_code=200, json=lambda: fake_response)
    )

    mocker.patch(
        "serwis_info.modules.calendar.services.horoscope_service.translate_to_polish",
        return_value="To jest świetny dzień"
    )

    result = horoscope_service.get_horoscope("baran")

    assert result["success"] is True
    assert result["zodiac_sign"] == "baran"
    assert result["horoscope"] == "To jest świetny dzień"


def test_get_horoscope_primary_api_failure_fallback(mocker):
    mocker.patch(
        "serwis_info.modules.calendar.services.horoscope_service.requests.get",
        return_value=mocker.Mock(status_code=500)
    )

    mocker.patch(
        "serwis_info.modules.calendar.services.horoscope_service.requests.post",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: {
                "description": "Fallback horoscope",
                "mood": "Happy",
                "compatibility": "Leo",
                "lucky_number": "7",
                "lucky_time": "12:00"
            }
        )
    )

    mocker.patch(
        "serwis_info.modules.calendar.services.horoscope_service.translate_to_polish",
        side_effect=lambda x: f"PL:{x}" if x else x
    )

    result = horoscope_service.get_horoscope("lew")

    assert result["success"] is True
    assert result["horoscope"] == "PL:Fallback horoscope"
    assert result["mood"] == "PL:Happy"


def test_get_horoscope_all_apis_down(mocker):
    mocker.patch(
        "serwis_info.modules.calendar.services.horoscope_service.requests.get",
        side_effect=Exception("API down")
    )

    result = horoscope_service.get_horoscope("rak")

    assert "error" in result

# =========================
# TESTY ROUTES (ACCESS)
# =========================

def test_horoscope_page_requires_login(client):
    response = client.get("/calendar/horoscope", follow_redirects=True)
    assert response.status_code == 200
    assert b"login" in response.data.lower() or b"zaloguj" in response.data.lower()


def test_horoscope_api_ok(client, mocker):
    mocker.patch(
        "serwis_info.modules.calendar.services.horoscope_service.get_horoscope",
        return_value={"success": True}
    )

    response = client.get("/calendar/api/horoscope/baran")
    assert response.status_code == 200


def test_horoscope_api_error(client, mocker):
    mocker.patch(
        "serwis_info.modules.calendar.services.horoscope_service.get_horoscope",
        return_value={"error": "Invalid"}
    )

    response = client.get("/calendar/api/horoscope/invalid")
    assert response.status_code == 400
