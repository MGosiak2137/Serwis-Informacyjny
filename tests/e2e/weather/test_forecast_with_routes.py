from playwright.sync_api import Page, expect
import json


def test_forecast_shows_next_days_with_route(page: Page, e2e_server):
    # load fixtures
    with open("tests/e2e/fixtures/weather/current_warsaw.json", "r", encoding="utf-8") as f:
        current = f.read()
    with open("tests/e2e/fixtures/weather/forecast_warsaw.json", "r", encoding="utf-8") as f:
        forecast = f.read()
    with open("tests/e2e/fixtures/weather/air_warsaw.json", "r", encoding="utf-8") as f:
        air = f.read()

    # intercept OpenWeatherMap requests and return deterministic fixtures
    page.route("https://api.openweathermap.org/data/2.5/weather*", lambda route, request: route.fulfill(status=200, body=current, headers={"Content-Type": "application/json"}))
    page.route("https://api.openweathermap.org/data/2.5/forecast*", lambda route, request: route.fulfill(status=200, body=forecast, headers={"Content-Type": "application/json"}))
    page.route("https://api.openweathermap.org/data/2.5/air_pollution*", lambda route, request: route.fulfill(status=200, body=air, headers={"Content-Type": "application/json"}))

    # visit page and perform search
    page.goto(f"{e2e_server}/weather/")
    page.locator("#cityInput").fill("Warsaw")
    page.locator("#searchBtn").click()

    # wait for weather card to appear
    weather_card = page.locator("#weatherInfoContainer .weather-card")
    expect(weather_card).to_have_count(1)

    # click forecast and assert forecast calendar visible
    page.locator(".forecastBtn").first.click()
    expect(page.locator("#forecast_Warsaw .forecast-calendar")).to_be_visible()
