#testuje Czy /weather/dashboard: 
#renderuje HTML zawiera kluczowe elementy UI 

def test_weather_dashboard_render(client):
    """
    Sprawdza czy dashboard pogodowy się renderuje
    """
    response = client.get("/weather/dashboard")

    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # podstawowe elementy HTML
    assert "<title>Weather Dashboard</title>" in html
    assert "Panel pogodowy" in html
    assert "Szukaj miasta" in html
