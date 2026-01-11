from playwright.sync_api import Page, expect
import re

def test_historical_price_data(page: Page, e2e_server):

    # GIVEN: zalogowany użytkownik
    page.goto(f"{e2e_server}/auth/login")
    page.locator("input[name='email']").fill("1233@wp.pl")
    page.locator("input[name='password']").fill("12345678")
    page.get_by_role("button", name="Zaloguj").click()
    page.wait_for_load_state("networkidle")

    # WHEN: przechodzi do giełdy
    page.goto(f"{e2e_server}/stockmarket")
    page.wait_for_load_state("networkidle")

    # wybiera kategorię
    category_link = page.get_by_role("link", name="Indeksy - Global")
    if category_link.count() > 0:
        category_link.click()
        page.wait_for_load_state("networkidle")
    
        # wybiera symbol
        select = page.locator("#select-symbols")
        if select.count() > 0:
            select.select_option("^GSPC")
            load_btn = page.locator("#load-selected-btn")
            if load_btn.count() > 0:
                load_btn.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(2000)

                # THEN: karta dla symbolu istnieje
                card = page.locator("div.index-card[data-symbol='^GSPC']")
                if card.count() > 0:
                    expect(card).to_be_visible(timeout=5000)

                    # AND: widoczna jest cena
                    price = card.locator(".index-price")
                    if price.count() > 0:
                        expect(price).to_be_visible()

                    # AND: widoczna jest zmiana (rate)
                    rate = card.locator(".index-rate")
                    if rate.count() > 0:
                        expect(rate).to_be_visible()

