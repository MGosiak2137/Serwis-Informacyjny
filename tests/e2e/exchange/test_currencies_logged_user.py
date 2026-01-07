from playwright.sync_api import Page, expect

def test_logged_user_can_see_rates_and_convert_currency(page: Page, e2e_server):
    # GIVEN: użytkownik zalogowany
    page.goto(f"{e2e_server}/auth/login")

    page.locator("input[name='email']").fill("test@test.pl")
    page.locator("input[name='password']").fill("test123T!")
    page.get_by_role("button", name="Zaloguj").click()

    # potwierdzenie logowania
    #expect(page.get_by_role("link", name="Wyloguj")).to_be_visible()

    # WHEN: przechodzi na kursy walut
    page.goto(f"{e2e_server}/currencies")

    # THEN: widzi tabelę kursów
    expect(page.locator("table.currency-table")).to_be_visible()
    expect(page.locator("table.currency-table tbody tr").first).to_be_visible()

    # WHEN: wykonuje konwersję
    page.locator("input[name='amount']").fill("100")
    page.locator("select[name='from_currency']").select_option("PLN")
    page.locator("select[name='to_currency']").select_option("EUR")
    page.get_by_role("button", name="Konwertuj").click()

    # THEN: widzi wynik konwersji
    expect(page.locator("p.converter-result")).to_be_visible()
    expect(page.locator("p.converter-result")).to_contain_text("EUR")
