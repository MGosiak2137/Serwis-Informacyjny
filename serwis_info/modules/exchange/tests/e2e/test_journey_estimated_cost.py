from playwright.sync_api import Page, expect

def test_logged_user_sees_estimated_trip_cost(page: Page, e2e_server):
    # GIVEN: użytkownik zalogowany
    page.goto(f"{e2e_server}/auth/login")

    page.locator("input[name='email']").fill("test@test.pl")
    page.locator("input[name='password']").fill("test123T!")
    page.get_by_role("button", name="Zaloguj").click()

    #expect(page.get_by_role("link", name="Wyloguj")).to_be_visible()

    # WHEN: przechodzi do wyszukiwarki lotów
    page.goto(f"{e2e_server}/journey")

    page.locator("input[name='origin']").fill("Warszawa")
    page.locator("input[name='destination']").fill("Barcelona")
    page.locator("input[name='date_from']").fill("2026-02-10")
    page.locator("input[name='date_to']").fill("2026-02-15")
    page.locator("input[name='people']").fill("2")

    page.get_by_role("button", name="Szukaj lotów").click()

    # THEN: widzi listę lotów
    expect(page.locator("ul.flights-list")).to_be_visible()
    expect(page.locator("li.flight-card").first).to_be_visible()

    # AND: widzi hotele (jeśli API zwróci)
    expect(page.locator("div.hotels-container")).to_be_visible()

    # AND: widzi podsumowanie kosztów
    expect(page.locator("div.summary-box")).to_be_visible()
    expect(page.locator("div.summary-box")).to_contain_text("Razem")
    expect(page.locator("div.summary-box")).to_contain_text("PLN")
