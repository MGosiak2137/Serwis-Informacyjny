from playwright.sync_api import Page, expect


def test_restore_previous_locations_after_login(page: Page, e2e_server):
    # simulate logged user and saved state before app loads
    page.context.add_cookies([{"name": "username", "value": "alice", "url": e2e_server}])
    # set localStorage for username before scripts run
    page.add_init_script("window.localStorage.setItem('weather_last_state_alice', JSON.stringify(['Warsaw','Krakow']));")

    # prepare fixtures mapping based on request URL
    with open("tests/e2e/fixtures/weather/current_warsaw.json", "r", encoding="utf-8") as f:
        w = f.read()
    with open("tests/e2e/fixtures/weather/air_warsaw.json", "r", encoding="utf-8") as f:
        wa = f.read()
    with open("tests/e2e/fixtures/weather/current_krakow.json", "r", encoding="utf-8") as f:
        k = f.read()
    with open("tests/e2e/fixtures/weather/air_krakow.json", "r", encoding="utf-8") as f:
        ka = f.read()
    with open("tests/e2e/fixtures/weather/forecast_warsaw.json", "r", encoding="utf-8") as f:
        fc = f.read()

    def route_handler(route, request):
        url = request.url
        if "q=Warsaw" in url or "/weather?q=Warsaw" in url or "lat=52" in url:
            if "air_pollution" in url:
                route.fulfill(status=200, body=wa, headers={"Content-Type":"application/json"})
            elif "forecast" in url:
                route.fulfill(status=200, body=fc, headers={"Content-Type":"application/json"})
            else:
                route.fulfill(status=200, body=w, headers={"Content-Type":"application/json"})
        elif "q=Krakow" in url or "lat=50" in url:
            if "air_pollution" in url:
                route.fulfill(status=200, body=ka, headers={"Content-Type":"application/json"})
            elif "forecast" in url:
                route.fulfill(status=200, body=fc, headers={"Content-Type":"application/json"})
            else:
                route.fulfill(status=200, body=k, headers={"Content-Type":"application/json"})
        else:
            route.continue_()

    page.route("https://api.openweathermap.org/data/2.5/*", route_handler)
    page.route("https://api.openweathermap.org/data/2.5/forecast*", route_handler)

    page.goto(f"{e2e_server}/weather/")

    # after autoLoadLastCities app should have two cards
    cards = page.locator("#weatherInfoContainer .weather-card")
    expect(cards).to_have_count(2)

    # history section toggled via panel
    page.locator("#togglePanelBtn").click()
    page.locator("#toggleHistoryBtn").click()
    page.locator("#showHistoryBtn").click()
    expect(page.locator("#historyList li")).to_have_count(0)  # history loaded but may be empty in fixtures
