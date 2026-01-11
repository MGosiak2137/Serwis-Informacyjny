import json

def test_simple_weather_ok(client, mocker):
    fake_response = {
        "main": {"temp": 20.4},
        "weather": [{"description": "clear sky", "icon": "01d"}]
    }

    mocker.patch(
        "serwis_info.modules.weather.routes.weather_routes.requests.get"
    ).return_value.json.return_value = fake_response

    res = client.get("/weather/api/simple_weather")

    assert res.status_code == 200
    data = res.get_json()

    assert data["temp"] == 20
    assert data["desc"] == "Clear sky"
    assert data["icon"] == "01d"

#test prognozy
def test_forecast_returns_3_days(client, mocker):
    fake_api_data = {
        "list": [
            {
                "dt_txt": "2026-01-01 12:00:00",
                "main": {"temp": 10, "humidity": 80},
                "wind": {"speed": 5},
                "weather": [{"icon": "01d", "description": "clear sky"}]
            },
            {
                "dt_txt": "2026-01-02 12:00:00",
                "main": {"temp": 12, "humidity": 70},
                "wind": {"speed": 4},
                "weather": [{"icon": "02d", "description": "cloudy"}]
            },
            {
                "dt_txt": "2026-01-03 12:00:00",
                "main": {"temp": 9, "humidity": 60},
                "wind": {"speed": 3},
                "weather": [{"icon": "03d", "description": "rain"}]
            },
        ]
    }

    mocker.patch(
        "serwis_info.modules.weather.routes.weather_routes.requests.get"
    ).return_value.json.return_value = fake_api_data

    res = client.get("/weather/api/forecast")

    assert res.status_code == 200
    data = res.get_json()

    assert isinstance(data, list)
    assert len(data) == 3
    assert "temp" in data[0]
    assert "humidity" in data[0]
