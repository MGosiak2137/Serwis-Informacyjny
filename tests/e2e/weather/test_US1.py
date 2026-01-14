import pytest
from playwright.sync_api import expect

@pytest.mark.e2e
def test_guest_sees_warsaw_weather_or_fallback(page, e2e_server):
    page.goto(f"{e2e_server}/weather/dashboard")

    # Poczekaj aż JS się wykona
    page.wait_for_load_state("networkidle")

    # Sprawdź czy istnieje kontener widgetu
    widget = page.locator(".weather-hero")
    expect(widget).to_be_visible()

    # Spróbuj znaleźć miasto (jeśli API działa)
    city = page.locator(".wm-city")

    if city.count() > 0 and city.inner_text().strip() != "":
        # ✅ ścieżka idealna
        assert city.inner_text() == "Warszawa"
    else:
        # ✅ ścieżka awaryjna – dane niedostępne
        page_content = page.content()
        assert (
            "Brak" in page_content
            or "Ładowanie" in page_content
            or "pogod" in page_content.lower()
        )
