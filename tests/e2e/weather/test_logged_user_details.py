from playwright.sync_api import Page, expect


def test_logged_user_sees_detailed_metrics(page: Page, e2e_server):
    # simulate logged user
    page.context.add_cookies([{"name": "username", "value": "alice", "url": e2e_server}])

    # load fixtures
    with open("tests/e2e/fixtures/weather/current_warsaw.json", "r", encoding="utf-8") as f:
        current = f.read()
    with open("tests/e2e/fixtures/weather/air_warsaw.json", "r", encoding="utf-8") as f:
        air = f.read()
    with open("tests/e2e/fixtures/weather/forecast_warsaw.json", "r", encoding="utf-8") as f:
        forecast = f.read()

    # intercept requests
    page.route("https://api.openweathermap.org/data/2.5/weather*", lambda route, req: route.fulfill(status=200, body=current, headers={"Content-Type":"application/json"}))
    page.route("https://api.openweathermap.org/data/2.5/forecast*", lambda route, req: route.fulfill(status=200, body=forecast, headers={"Content-Type":"application/json"}))
    page.route("https://api.openweathermap.org/data/2.5/air_pollution*", lambda route, req: route.fulfill(status=200, body=air, headers={"Content-Type":"application/json"}))

    page.goto(f"{e2e_server}/weather/")
    # ensure username displayed
    expect(page.locator("#usernameDisplay")).to_have_text("alice")

    # search and assert metrics visible
    page.locator("#cityInput").fill("Warsaw")
    page.locator("#searchBtn").click()

    card = page.locator("#weatherInfoContainer .weather-card").first
    expect(card.locator("h2")).to_have_text("Warsaw")
    expect(card).to_contain_text("Temperatura")
    expect(card).to_contain_text("Wilgotność")
    expect(card).to_contain_text("Ciśnienie")
    expect(card).to_contain_text("Wiatr")
    expect(card).to_contain_text("Jakość powietrza")
