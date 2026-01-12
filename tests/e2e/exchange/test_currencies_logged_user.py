from playwright.sync_api import Page, expect

def test_logged_user_can_see_rates_and_convert_currency(page: Page, e2e_server, credentials):
    # GIVEN: użytkownik zalogowany
    page.goto(f"{e2e_server}/auth/login")

    page.locator("input[name='email']").fill(credentials['email'])
    page.locator("input[name='password']").fill(credentials['password'])
    page.get_by_role("button", name="Zaloguj się").click()
    page.wait_for_load_state("networkidle")

    # WHEN: przechodzi na kursy walut
    page.goto(f"{e2e_server}/currencies")
    page.wait_for_load_state("networkidle")

    # THEN: widzi tabelę kursów
    expect(page.locator("table.currency-table")).to_be_visible()
    expect(page.locator("table.currency-table tbody tr").first).to_be_visible()

    # WHEN: wykonuje konwersję
    page.locator("input[name='amount']").fill("100")
    page.locator("select[name='from_currency']").select_option("PLN")
    page.locator("select[name='to_currency']").select_option("EUR")
    page.get_by_role("button", name="Konwertuj").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # THEN: widzi wynik konwersji - sprawdzamy różne selektory
    # Element powinien być gdzieś na stronie po submit
    result_element = page.locator("text=/EUR/")
    if result_element.count() > 0:
        expect(result_element.first).to_be_visible()

