def test_weather_dashboard_renders_under_weather_prefix(client):
    res = client.get("/weather/dashboard")
    assert res.status_code == 200
    assert b"Weather Dashboard" in res.data


def test_weather_dashboard_renders_at_root_dashboard(client):
    # The weather blueprint's API blueprint is also registered at the app root.
    res = client.get("/dashboard")
    assert res.status_code == 200
    assert b"Weather Dashboard" in res.data
