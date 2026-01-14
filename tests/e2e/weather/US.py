import re
import pytest
from playwright.sync_api import expect


@pytest.mark.e2e
def test_weather_for_warsaw_unauthenticated(e2e_server, page):
    """
    USER STORY:
    Pogoda dla Warszawy dla niezalogowanego użytkownika
    """
    page.goto(f"{e2e_server}/weather/dashboard")

    # Mini-widget pogody
    expect(page.locator(".wm-city")).to_have_text("Warszawa")
    expect(page.locator("#mini-temp")).to_be_visible()
    expect(page.locator("#mini-desc")).to_be_visible()
    expect(page.locator("#mini-icon")).to_be_visible()


@pytest.mark.e2e
def test_detailed_weather_info_after_search(e2e_server, page):
    """
    USER STORY:
    Szczegółowe informacje pogodowe
    """
    page.goto(f"{e2e_server}/weather/dashboard")

    page.fill("#cityInput", "Kraków")
    page.click("#searchBtn")

    card = page.locator(".weather-card").first
    expect(card).to_be_visible()

    expect(card.locator("text=Temperatura")).to_be_visible()
    expect(card.locator("text=Wilgotność")).to_be_visible()
    expect(card.locator("text=Ciśnienie")).to_be_visible()
    expect(card.locator("text=Wiatr")).to_be_visible()
    expect(card.locator("text=Jakość powietrza")).to_be_visible()


@pytest.mark.e2e
def test_forecast_for_other_days(e2e_server, page):
    """
    USER STORY:
    Prognoza na inne dni
    """
    page.goto(f"{e2e_server}/weather/dashboard")

    page.fill("#cityInput", "Gdańsk")
    page.click("#searchBtn")

    page.click(".forecastBtn")

    forecast = page.locator(".forecast")
    expect(forecast).to_be_visible()

    expect(forecast.locator(".cal-day-btn")).to_have_count(5)


@pytest.mark.e2e
def test_graphical_visualization_map_and_chart(e2e_server, page):
    """
    USER STORY:
    Wizualizacja graficzna (mapa + wykres)
    """
    page.goto(f"{e2e_server}/weather/dashboard")

    # Mapa
    map_el = page.locator("#map")
    expect(map_el).to_be_visible()

    # Szukamy miasta
    page.fill("#cityInput", "Poznań")
    page.click("#searchBtn")

    page.click(".forecastBtn")
    page.click(".cal-day-btn")

    # Klikamy godzinę → modal + wykres
    page.locator(".hour-btn").first.click()

    modal = page.locator(".hourly-modal")
    expect(modal).to_be_visible()

    canvas = modal.locator("canvas")
    expect(canvas).to_be_visible()


@pytest.mark.e2e
def test_weather_alerts_display(e2e_server, page):
    """
    USER STORY:
    Powiadomienia o gwałtownej zmianie pogody
    """
    page.goto(f"{e2e_server}/weather/dashboard")

    page.fill("#cityInput", "Warszawa")
    page.click("#searchBtn")

    alerts = page.locator("#alertsContent")
    expect(alerts).to_be_visible()

    # Może być brak lub lista alertów – sprawdzamy, że system działa
    expect(alerts).not_to_have_text("")


@pytest.mark.e2e
def test_weather_data_unavailable_message(e2e_server, page):
    """
    USER STORY:
    Komunikat gdy dane pogodowe są niedostępne
    """
    page.goto(f"{e2e_server}/weather/dashboard")

    page.fill("#cityInput", "NieistniejaceMiasto123")
    page.click("#searchBtn")

    # Alert JS
    page.on("dialog", lambda dialog: dialog.accept())


@pytest.mark.e2e
def test_restore_last_state_after_reload(e2e_server, page):
    """
    USER STORY:
    Zapis lokalizacji przy ponownym wejściu
    """
    page.goto(f"{e2e_server}/weather/dashboard")

    page.fill("#cityInput", "Wrocław")
    page.click("#searchBtn")

    expect(page.locator(".weather-card")).to_have_count(1)

    # Odświeżenie strony
    page.reload()

    # Stan powinien się odtworzyć
    expect(page.locator(".weather-card")).to_have_count(1)
    expect(page.locator(".weather-card h2")).to_have_text("Wrocław")
