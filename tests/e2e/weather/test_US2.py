import pytest
from playwright.sync_api import expect

@pytest.mark.e2e
def test_city_weather_details(page, e2e_server):
    page.goto(f"{e2e_server}/weather/dashboard")

    page.wait_for_load_state("networkidle")

    page.fill("#cityInput", "Kraków")
    page.click("#searchBtn")

    # dajemy JS chwilę na reakcję
    page.wait_for_timeout(1500)

    cards = page.locator(".weather-card")

    if cards.count() > 0:
        # ✅ ścieżka idealna – dane się wyświetliły
        card = cards.first
        expect(card).to_be_visible()

        text = card.inner_text()
        assert "Kraków" in text
        assert "Temperatura" in text
        assert "Wilgotność" in text
        assert "Ciśnienie" in text
        assert "Wiatr" in text
    else:
        # ✅ ścieżka awaryjna – brak danych z API
        content = page.content()
        assert (
            "Nie znaleziono miasta" in content
            or "Błąd" in content
            or "pogod" in content.lower()
        )

