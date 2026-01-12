from playwright.sync_api import Page, expect


def test_logged_user_panel_toggles(page: Page, e2e_server, credentials):
    # Login user first
    page.goto(f"{e2e_server}/auth/login")
    page.locator("input[name='email']").fill(credentials['email'])
    page.locator("input[name='password']").fill(credentials['password'])
    page.get_by_role("button", name="Zaloguj się").click()
    page.wait_for_load_state("networkidle")

    page.goto(f"{e2e_server}/weather/")

    # Toggle panel open
    page.locator("#togglePanelBtn").click()
    expect(page.locator("#panelContent")).to_be_visible()

    # Toggle history options
    page.locator("#toggleHistoryBtn").click()
    expect(page.locator("#historyOptions")).to_be_visible()
