from playwright.sync_api import Page, expect
import re

def test_historical_price_data(page: Page, e2e_server):

    # GIVEN: zalogowany użytkownik
    page.goto(f"{e2e_server}/auth/login")
    page.locator("input[name='email']").fill("1233@wp.pl")
    page.locator("input[name='password']").fill("12345678")
    page.get_by_role("button", name="Zaloguj").click()

    # WHEN: przechodzi do giełdy
    page.goto(f"{e2e_server}/stockmarket")

    # wybiera kategorię
    page.get_by_role("link", name="Indeksy - Global").click()

    # wybiera symbol
    page.locator("#select-symbols").select_option("^GSPC")
    page.locator("#load-selected-btn").click()

    # THEN: karta dla symbolu istnieje
    card = page.locator(".index-card[data-symbol='^GSPC']")
    expect(card).to_be_visible()

    # AND: widoczna jest cena
    price = card.locator(".index-price")
    expect(price).to_be_visible()
    expect(price).not_to_have_text("n/d")

    # AND: widoczna jest zmiana (rate)


    rate = card.locator(".index-rate")
    expect(rate).to_be_visible()
    expect(rate).to_have_text(
        re.compile(r"\s*[+-]?\d+(\.\d+)?%\s*")
    )

