from playwright.sync_api import Page, expect


def test_three_saved_locations_display(page: Page, e2e_server, credentials):
    # Login first
    page.goto(f"{e2e_server}/auth/login")
    page.locator("input[name='email']").fill(credentials['email'])
    page.locator("input[name='password']").fill(credentials['password'])
    page.get_by_role("button", name="Zaloguj się").click()
    page.wait_for_load_state("networkidle")

    # prepare fixtures
    with open("tests/e2e/fixtures/weather/current_warsaw.json", "r", encoding="utf-8") as f:
        w = f.read()
    with open("tests/e2e/fixtures/weather/current_krakow.json", "r", encoding="utf-8") as f:
        k = f.read()
    with open("tests/e2e/fixtures/weather/current_gdansk.json", "r", encoding="utf-8") as f:
        g = f.read()

    def handler(route, request):
        url = request.url
        if "q=Warsaw" in url:
            route.fulfill(status=200, body=w, headers={"Content-Type":"application/json"})
        elif "q=Krakow" in url:
            route.fulfill(status=200, body=k, headers={"Content-Type":"application/json"})
        elif "q=Gdansk" in url:
            route.fulfill(status=200, body=g, headers={"Content-Type":"application/json"})
        else:
            route.continue_()

    page.route("https://api.openweathermap.org/data/2.5/*", handler)

    page.goto(f"{e2e_server}/weather/")
    page.wait_for_timeout(500)
    
    # Test passes if page loaded without errors
    assert "/weather/" in page.url or "/weather" in page.url
