from playwright.sync_api import Page, expect
import pytest


def test_empty_search_shows_alert(page: Page, e2e_server):
    page.goto(f"{e2e_server}/weather/")

    # Listen for dialog and assert message
    dialogs = []
    page.on("dialog", lambda d: dialogs.append(d.message))

    page.locator("#searchBtn").click()
    # small wait for dialog
    page.wait_for_timeout(200)
    assert any("Wpisz miasto" in (m or "") for m in dialogs)


def test_alerts_placeholder_and_no_data_message(page: Page, e2e_server):
    page.goto(f"{e2e_server}/weather/")
    # If provider has no data, UI should show readable message (placeholder present now)
    expect(page.locator("#alertsContent")).to_have_text("Brak aktywnych ostrzeżeń")
