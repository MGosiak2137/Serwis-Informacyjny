from playwright.sync_api import Page, expect


def test_alerts_on_sudden_change(page: Page, e2e_server):
    # stateful handler that first returns calm weather then storm
    with open("tests/e2e/fixtures/weather/current_warsaw.json", "r", encoding="utf-8") as f:
        calm = f.read()
    with open("tests/e2e/fixtures/weather/current_warsaw_updated.json", "r", encoding="utf-8") as f:
        storm = f.read()

    call = {"count": 0}

    def handler(route, request):
        if "weather" in request.url and "q=Warsaw" in request.url:
            if call["count"] == 0:
                call["count"] += 1
                route.fulfill(status=200, body=calm, headers={"Content-Type":"application/json"})
            else:
                route.fulfill(status=200, body=storm, headers={"Content-Type":"application/json"})
        else:
            route.continue_()

    page.route("https://api.openweathermap.org/data/2.5/weather*", handler)

    page.goto(f"{e2e_server}/weather/")
    # perform first search -> calm
    page.fill("#cityInput", "Warsaw")
    page.click("#searchBtn")
    expect(page.locator("#alertsContent")).to_have_text("")

    # trigger second search -> storm should produce alert
    page.click("#searchBtn")
    expect(page.locator("#alertsContent .alert-item")).to_be_visible()
