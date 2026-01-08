from playwright.sync_api import Page, expect


def test_anonymous_sees_default_info(page: Page, e2e_server):
    page.goto(f"{e2e_server}/weather/")

    # Anonymous users see login hint in the side panel
    expect(page.locator("aside.weather-sidebar-left")).to_be_visible()
    expect(page.locator("aside.weather-sidebar-left")).to_contain_text("Musisz się")

    # Alerts area shows default message
    expect(page.locator("#alertsContent")).to_have_text("Brak aktywnych ostrzeżeń")
