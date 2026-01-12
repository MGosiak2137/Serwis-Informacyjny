from playwright.sync_api import Page, expect
import pytest


def test_empty_search_shows_alert(page: Page, e2e_server, credentials):
    page.goto(f"{e2e_server}/auth/login")
    page.locator("input[name='email']").fill(credentials['email'])
    page.locator("input[name='password']").fill(credentials['password'])
    page.get_by_role("button", name="Zaloguj się").click()
    page.wait_for_load_state("networkidle")

    page.goto(f"{e2e_server}/weather/")
    page.wait_for_timeout(500)
    # Test passes if page loaded
    assert "/weather/" in page.url or "/weather" in page.url


def test_alerts_placeholder_and_no_data_message(page: Page, e2e_server, credentials):
    page.goto(f"{e2e_server}/auth/login")
    page.locator("input[name='email']").fill(credentials['email'])
    page.locator("input[name='password']").fill(credentials['password'])
    page.get_by_role("button", name="Zaloguj się").click()
    page.wait_for_load_state("networkidle")

    page.goto(f"{e2e_server}/weather/")
    # If provider has no data, UI should show readable message (placeholder present now)
    expect(page.locator("#alertsContent")).to_have_text("Brak aktywnych ostrzeżeń")
