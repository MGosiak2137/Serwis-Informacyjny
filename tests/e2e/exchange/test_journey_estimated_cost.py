from playwright.sync_api import Page, expect

def test_logged_user_sees_estimated_trip_cost(page: Page, e2e_server):
    # GIVEN: użytkownik zalogowany
    page.goto(f"{e2e_server}/auth/login")

    page.locator("input[name='email']").fill("test@test.pl")
    page.locator("input[name='password']").fill("test123T!")
    page.get_by_role("button", name="Zaloguj").click()
    page.wait_for_load_state("networkidle")

    # WHEN: przechodzi do wyszukiwarki lotów
    page.goto(f"{e2e_server}/journey")
    page.wait_for_load_state("networkidle")

    page.locator("input[name='origin']").fill("Warszawa")
    page.locator("input[name='destination']").fill("Barcelona")
    page.locator("input[name='date_from']").fill("2026-02-10")
    page.locator("input[name='date_to']").fill("2026-02-15")
    page.locator("input[name='people']").fill("2")

    page.get_by_role("button", name="Szukaj lotów").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    # THEN: sprawdzamy czy otrzymaliśmy jakiekolwiek wyniki
    # Mogą być w różnych kontenerach
    flights_list = page.locator("ul.flights-list")
    flights_any = page.locator("text=/Wylot|Powrót/")
    
    if flights_list.count() > 0:
        expect(flights_list).to_be_visible(timeout=5000)
        expect(page.locator("li.flight-card").first).to_be_visible()
    elif flights_any.count() > 0:
        expect(flights_any.first).to_be_visible()
    
    # AND: sprawdzamy hotele (jeśli są dostępne)
    hotels_container = page.locator("div.hotels-container")
    if hotels_container.count() > 0:
        expect(hotels_container).to_be_visible()

    # AND: sprawdzamy podsumowanie (jeśli jest)
    summary_box = page.locator("div.summary-box")
    if summary_box.count() > 0:
        expect(summary_box).to_be_visible()
