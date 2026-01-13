import json
from unittest.mock import patch


def test_get_config_endpoint(client):
    response = client.get("/weather/api/config")

    assert response.status_code == 200
    data = response.get_json()

    assert "API_KEY" in data
    assert "API_URL" in data
    assert data["API_URL"].startswith("https://api.openweathermap.org")


@patch("serwis_info.modules.weather.routes.weather_routes.requests.get")
def test_simple_weather_endpoint(mock_get, client):
    """
    Test /api/simple_weather z mockiem OpenWeather
    """
    mock_get.return_value.json.return_value = {
        "main": {"temp": 12.3},
        "weather": [
            {"description": "zachmurzenie umiarkowane", "icon": "03d"}
        ]
    }

    response = client.get("/weather/api/simple_weather")

    assert response.status_code == 200
    data = response.get_json()

    assert set(data.keys()) == {"temp", "desc", "icon"}
    assert isinstance(data["temp"], int)
    assert isinstance(data["desc"], str)
    assert isinstance(data["icon"], str)


@patch("serwis_info.modules.weather.routes.weather_routes.requests.get")
def test_weather_forecast_endpoint(mock_get, client):
    """
    Test /api/forecast – 3-dniowa prognoza
    """
    mock_get.return_value.json.return_value = {
        "list": [
            {
                "dt_txt": "2025-01-10 12:00:00",
                "main": {"temp": 10, "humidity": 80},
                "wind": {"speed": 5},
                "weather": [{"description": "słonecznie", "icon": "01d"}]
            },
            {
                "dt_txt": "2025-01-10 15:00:00",
                "main": {"temp": 12, "humidity": 70},
                "wind": {"speed": 6},
                "weather": [{"description": "słonecznie", "icon": "01d"}]
            },
            {
                "dt_txt": "2025-01-11 12:00:00",
                "main": {"temp": 8, "humidity": 75},
                "wind": {"speed": 4},
                "weather": [{"description": "pochmurnie", "icon": "03d"}]
            }
        ]
    }

    response = client.get("/weather/api/forecast")

    assert response.status_code == 200
    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) >= 1

    day = data[0]
    assert set(day.keys()) == {
        "date", "temp", "wind", "humidity", "icon", "desc"
    }
