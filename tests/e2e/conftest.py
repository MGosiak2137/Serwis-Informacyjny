"""
Konfiguracja Playwright dla testów e2e
"""
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def browser():
    """Fixture do inicjalizacji przeglądarki Playwright"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser):
    """Fixture tworzący nową stronę dla każdego testu"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="module")
def e2e_server():
    """Fixture zwracający bazowy URL aplikacji"""
    return "http://localhost:5000"

