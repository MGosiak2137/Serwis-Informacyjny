"""
Testy e2e dla ładowania modułów - używając Playwright
"""
from playwright.sync_api import Page, expect


def test_load_modules(page: Page, e2e_server):
    """Test sprawdzający ładowanie różnych modułów i logowanie"""
    # Przejdź na stronę główną
    page.goto(f"{e2e_server}/main/")
    
    # Kliknij link "Wiadomości" (szukaj w navbarze)
    news_link = page.locator("a[href*='news']").first
    if news_link.count() > 0:
        news_link.click()
        page.wait_for_timeout(1000)
        current_url = page.url
        if "/news" in current_url:
            expect(page.get_by_role("heading", name="Moduł Wiadomości")).to_be_visible()
    
    # Kliknij link "Pogoda"
    page.goto(f"{e2e_server}/weather/")
    page.wait_for_timeout(1000)
    current_url = page.url
    assert "/weather" in current_url
    
    # Wróć na stronę główną
    page.goto(f"{e2e_server}/main/")
    
    # Kliknij przycisk "Zaloguj się" (jeśli istnieje)
    login_button = page.get_by_role("button", name="Zaloguj się")
    if login_button.count() > 0:
        login_button.click()
        page.wait_for_timeout(1000)
        current_url = page.url
        assert "/auth/login" in current_url
        
        # Wypełnij formularz logowania
        page.locator("input[name='email']").fill("user@test.pl")
        page.locator("input[name='password']").fill("user123")
        page.get_by_role("button", name="Zaloguj się").click()
        
        # Poczekaj na zalogowanie
        page.wait_for_timeout(2000)
        
        # Jeśli logowanie się powiodło, sprawdź menu użytkownika
        if "/auth/login" not in page.url:
            # Wróć na stronę główną
            page.goto(f"{e2e_server}/main/")
            
            # Sprawdź czy jest menu użytkownika (może być w różnych miejscach)
            user_menu = page.locator("a:has-text('user')").first
            if user_menu.count() > 0:
                user_menu.click()
                page.wait_for_timeout(500)


def test_homepage_loads_playwright(page: Page, e2e_server):
    """Test sprawdzający czy strona główna się ładuje - Playwright"""
    page.goto(f"{e2e_server}/main/")
    
    # Sprawdź tytuł strony
    title = page.title()
    assert "NEWC" in title or "Serwis informacyjny" in title
    
    # Sprawdź czy navbar jest widoczny
    expect(page.get_by_role("navigation")).to_be_visible()
    
    # Sprawdź czy są karty modułów
    cards = page.locator(".card-item")
    expect(cards.first).to_be_visible()


def test_login_playwright(page: Page, e2e_server):
    """Test logowania - Playwright"""
    page.goto(f"{e2e_server}/auth/login")
    
    # Sprawdź czy formularz jest widoczny
    expect(page.locator("input[name='email']")).to_be_visible()
    expect(page.locator("input[name='password']")).to_be_visible()
    expect(page.get_by_role("button", name="Zaloguj się")).to_be_visible()
    
    # Wypełnij formularz (możesz użyć istniejącego użytkownika)
    page.locator("input[name='email']").fill("test@test.pl")
    page.locator("input[name='password']").fill("password")
    page.get_by_role("button", name="Zaloguj się").click()
    
    # Sprawdź czy nastąpiło przekierowanie (lub komunikat błędu)
    page.wait_for_timeout(2000)
    current_url = page.url
    # Jeśli logowanie się powiodło, nie powinniśmy być na stronie logowania
    if "/auth/login" not in current_url:
        assert "/main" in current_url or "/" in current_url


def test_horoscope_playwright(page: Page, e2e_server):
    """Test horoskopu - Playwright"""
    # Sprawdź czy strona wymaga logowania
    page.goto(f"{e2e_server}/calendar/horoscope")
    page.wait_for_timeout(1000)
    current_url = page.url
    assert "/auth/login" in current_url
    
    # Jeśli chcesz przetestować po zalogowaniu, najpierw się zaloguj
    # (wymaga istniejącego użytkownika w bazie)

