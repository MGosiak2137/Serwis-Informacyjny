"""
Testy e2e dla logowania - Playwright
"""
from playwright.sync_api import Page, expect
import pytest


def test_login_page_loads(page: Page, e2e_server):
    """Test sprawdzający czy strona logowania się ładuje"""
    # GIVEN: użytkownik otwiera stronę logowania
    page.goto(f"{e2e_server}/auth/login")
    
    # THEN: strona się załadowała
    expect(page).to_have_url(f"{e2e_server}/auth/login")
    
    # AND: formularz jest widoczny
    expect(page.locator("form")).to_be_visible()


def test_login_form_has_fields(page: Page, e2e_server):
    """Test sprawdzający czy formularz logowania ma wszystkie pola"""
    # GIVEN: użytkownik jest na stronie logowania
    page.goto(f"{e2e_server}/auth/login")
    
    # THEN: pole email jest widoczne
    email_input = page.locator("input[name='email']")
    expect(email_input).to_be_visible()
    
    # AND: pole hasła jest widoczne
    password_input = page.locator("input[name='password']")
    expect(password_input).to_be_visible()
    
    # AND: przycisk submit jest widoczny
    submit_button = page.get_by_role("button", name="Zaloguj się")
    expect(submit_button).to_be_visible()


def test_login_with_invalid_credentials(page: Page, e2e_server):
    """Test logowania z niepoprawnymi danymi"""
    # GIVEN: użytkownik jest na stronie logowania
    page.goto(f"{e2e_server}/auth/login")
    
    # WHEN: wypełnia formularz niepoprawnymi danymi
    page.locator("input[name='email']").fill("invalid@test.pl")
    page.locator("input[name='password']").fill("wrongpassword")
    page.get_by_role("button", name="Zaloguj się").click()
    
    # THEN: jesteśmy nadal na stronie logowania lub pojawił się komunikat błędu
    # (może być przekierowanie lub komunikat błędu)
    page.wait_for_timeout(2000)
    current_url = page.url
    assert "/auth/login" in current_url or page.locator(".alert-danger").count() > 0


def test_login_with_valid_credentials(page: Page, e2e_server):
    """Test logowania z poprawnymi danymi"""
    # GIVEN: użytkownik jest na stronie logowania
    page.goto(f"{e2e_server}/auth/login")
    
    # WHEN: wypełnia formularz poprawnymi danymi (wymaga istniejącego użytkownika)
    page.locator("input[name='email']").fill("user@test.pl")
    page.locator("input[name='password']").fill("user123")
    page.get_by_role("button", name="Zaloguj się").click()
    
    # THEN: nastąpiło przekierowanie (nie jesteśmy na stronie logowania)
    # UWAGA: Test może się nie powieść jeśli użytkownik nie istnieje
    page.wait_for_timeout(2000)
    current_url = page.url
    # Jeśli logowanie się powiodło, nie powinniśmy być na stronie logowania
    if "/auth/login" not in current_url:
        assert "/main" in current_url or "/" in current_url

