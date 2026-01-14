import pytest

@pytest.mark.e2e
def test_weather_alerts_display(page, e2e_server):
    page.goto(f"{e2e_server}/weather/dashboard")

    page.fill("#cityInput", "Warszawa")
    page.click("#searchBtn")

    alerts = page.locator("#alertsContent")
    alerts.wait_for()

    # Może być brak lub lista ostrzeżeń
    assert alerts.inner_text() != ""
