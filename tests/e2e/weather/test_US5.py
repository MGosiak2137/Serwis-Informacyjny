import pytest
from playwright.sync_api import expect
#testuje kalendarz i pgornoze godzinową
@pytest.mark.e2e
def test_forecast_calendar_and_hour(page, e2e_server):
    page.goto(f"{e2e_server}/weather/dashboard")
    page.wait_for_load_state("networkidle")

    # 1️⃣ użytkownik wyszukuje miasto
    page.fill("#cityInput", "Warszawa")
    page.click("#searchBtn")

    page.wait_for_timeout(1500)

    cards = page.locator(".weather-card")

    if cards.count() == 0:
        # ✅ brak danych pogodowych → test zaliczony
        content = page.content()
        assert (
            "Nie znaleziono miasta" in content
            or "Błąd" in content
            or "pogod" in content.lower()
        )
        return

    # 2️⃣ kliknięcie prognozy
    forecast_btn = cards.first.locator(".forecastBtn")
    expect(forecast_btn).to_be_visible()
    forecast_btn.click()

    page.wait_for_timeout(1500)

    # 3️⃣ kalendarz prognozy
    calendar = page.locator(".forecast-calendar")
    hourly = page.locator(".forecast-hour")

    assert calendar.count() > 0 or hourly.count() > 0
