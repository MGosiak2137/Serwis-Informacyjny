import pytest
#testuje System ostrzeżeń pogodowych 
@pytest.mark.e2e
def test_weather_alerts_display(page, e2e_server):
    page.goto(f"{e2e_server}/weather/dashboard")

    page.fill("#cityInput", "Warszawa")
    page.click("#searchBtn")
#czy kontener nie jest pusty
    alerts = page.locator("#alertsContent")
    alerts.wait_for()

    # Może być brak lub lista ostrzeżeń
    assert alerts.inner_text() != ""
    #Testuje, czy użytkownik zawsze dostaje informację zwrotną 
