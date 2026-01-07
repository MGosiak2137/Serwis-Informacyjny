"""
Testy e2e dla strony głównej - Playwright
"""
from playwright.sync_api import Page, expect
import pytest


def test_homepage_loads(page: Page, e2e_server):
    """Test sprawdzający czy strona główna się ładuje"""
    # GIVEN: użytkownik otwiera stronę główną
    page.goto(f"{e2e_server}/main/")
    
    # THEN: strona się załadowała
    title = page.title()
    assert "NEWC" in title or "Serwis informacyjny" in title
    
    # AND: jest element body
    expect(page.locator("body")).to_be_visible()


def test_homepage_has_navbar(page: Page, e2e_server):
    """Test sprawdzający czy navbar jest widoczny"""
    # GIVEN: użytkownik jest na stronie głównej
    page.goto(f"{e2e_server}/main/")
    
    # THEN: navbar jest widoczny
    expect(page.get_by_role("navigation")).to_be_visible()
    
    # AND: navbar zawiera logo lub tekst
    navbar = page.locator(".main-navbar")
    expect(navbar).to_be_visible()


def test_homepage_has_cards(page: Page, e2e_server):
    """Test sprawdzający czy na stronie głównej są karty modułów"""
    # GIVEN: użytkownik jest na stronie głównej
    page.goto(f"{e2e_server}/main/")
    
    # THEN: są karty modułów
    cards = page.locator(".card-item")
    expect(cards.first).to_be_visible()
    
    # AND: jest przynajmniej jedna karta
    expect(cards).to_have_count(4, timeout=5000)  # Kalendarz, News, Pogoda, Ekonomia


def test_homepage_has_footer(page: Page, e2e_server):
    """Test sprawdzający czy stopka jest widoczna"""
    # GIVEN: użytkownik jest na stronie głównej
    page.goto(f"{e2e_server}/main/")
    
    # THEN: stopka jest widoczna
    footer = page.locator(".main-footer")
    expect(footer).to_be_visible()
    
    # AND: stopka zawiera tekst
    expect(footer).to_contain_text("Serwis informacyjny")

