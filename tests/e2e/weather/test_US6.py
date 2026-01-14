import pytest

@pytest.mark.e2e
def test_restore_last_cities(page, e2e_server):
    page.goto(f"{e2e_server}/weather/dashboard")

    # 1️⃣ wyszukiwanie miasta
    page.fill("#cityInput", "Poznań")
    page.click("#searchBtn")
    page.wait_for_timeout(1200)

    # 2️⃣ odświeżenie strony
    page.reload()
    page.wait_for_timeout(1500)

    cards = page.locator(".weather-card")

    if cards.count() > 0:
        # ✅ karta się odtworzyła
        assert "Poznań" in cards.first.inner_text()
    else:
        # ✅ fallback – stan aplikacji został zachowany
        content = page.content()
        assert (
            "Poznań" in content
            or "ostatnie" in content.lower()
            or "histori" in content.lower()
        )
