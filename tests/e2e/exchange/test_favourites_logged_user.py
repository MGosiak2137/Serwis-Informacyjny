from playwright.sync_api import Page, expect

def test_favourites_positions(page: Page, e2e_server, credentials):

    # GIVEN: zalogowany użytkownik
    page.goto(f"{e2e_server}/auth/login")
    page.locator("input[name='email']").fill(credentials['email'])
    page.locator("input[name='password']").fill(credentials['password'])
    page.get_by_role("button", name="Zaloguj się").click()
    page.wait_for_load_state("networkidle")

    page.goto(f"{e2e_server}/main_eco/main_eco")
    page.wait_for_load_state("networkidle")

    expect(page.locator("h2:has-text('Ulubione pozycje w module ekonomicznym')")).to_be_visible()

    fav_actions = page.locator("#favorite-actions-list")
    currencies = page.locator("#currencies-list")
    history = page.locator("#search-history-list")

    expect(fav_actions).to_be_attached()
    expect(currencies).to_be_attached()
    expect(history).to_be_attached()

    if fav_actions.locator("li").count() > 0:
        expect(fav_actions.locator(".remove-btn").first).to_be_visible()

    if currencies.locator("li").count() > 0:
        expect(currencies.locator(".remove-btn").first).to_be_visible()

    if history.locator("li").count() > 0:
        expect(history.locator(".remove-btn").first).to_be_visible()
