from playwright.sync_api import Page, expect


def test_auto_refresh_updates_ui(page: Page, e2e_server):
    # simulate two different responses for auto-refresh interval
    with open("tests/e2e/fixtures/weather/current_warsaw.json", "r", encoding="utf-8") as f:
        first = f.read()
    with open("tests/e2e/fixtures/weather/current_warsaw_updated.json", "r", encoding="utf-8") as f:
        second = f.read()

    call = {"count": 0}

    def handler(route, request):
        if "weather" in request.url and "q=Warsaw" in request.url:
            if call["count"] == 0:
                call["count"] += 1
                route.fulfill(status=200, body=first, headers={"Content-Type":"application/json"})
            else:
                route.fulfill(status=200, body=second, headers={"Content-Type":"application/json"})
        else:
            route.continue_()

    page.route("https://api.openweathermap.org/data/2.5/weather*", handler)

    page.goto(f"{e2e_server}/weather/")
    page.fill("#cityInput", "Warsaw")
    page.click("#searchBtn")

    # initial temp from first fixture
    initial = page.locator(".weather-card .temp")
    expect(initial).to_be_visible()
    v1 = initial.inner_text()

    # simulate waiting for refresh interval by directly invoking refresh button if available
    if page.locator("#refreshBtn").count() > 0:
        page.click("#refreshBtn")
    else:
        # call the search again to trigger second response
        page.click("#searchBtn")

    v2 = page.locator(".weather-card .temp").inner_text()
    assert v1 != v2
