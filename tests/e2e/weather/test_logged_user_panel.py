from playwright.sync_api import Page, expect


def test_logged_user_panel_toggles(page: Page, e2e_server):
    # Simulate logged user by setting cookie used by weather scripts
    page.context.add_cookies([{"name": "username", "value": "alice", "url": e2e_server}])

    page.goto(f"{e2e_server}/weather/")

    # Toggle panel open
    page.locator("#togglePanelBtn").click()
    expect(page.locator("#panelContent")).to_be_visible()

    # Toggle history options
    page.locator("#toggleHistoryBtn").click()
    expect(page.locator("#historyOptions")).to_be_visible()
