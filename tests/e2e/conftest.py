"""
Konfiguracja Playwright dla testów e2e (NEWS)
"""
import os
import socket
import subprocess
import sys
import time

import pytest
from playwright.sync_api import sync_playwright, Browser, Page

EMAIL = "test@test.pl"
PASSWORD = "Password!1"


def _wait_for_5000(timeout: float = 25.0) -> None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(("127.0.0.1", 5000), timeout=0.5):
                return
        except OSError:
            time.sleep(0.2)
    raise RuntimeError("Server did not start on port 5000 in time")


@pytest.fixture(scope="session")
def browser() -> Browser:
    with sync_playwright() as p:
        # przy --headed i tak będzie okno; headless=False jest spoko do debug
        br = p.chromium.launch(headless=False)
        yield br
        br.close()


@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    context = browser.new_context()
    pg = context.new_page()
    yield pg
    context.close()


@pytest.fixture(scope="session")
def server_base_url():
    env = os.environ.copy()
    env["NEWS_DB_PATH"] = r"serwis_info\modules\news\test_news.db"

    # jeśli serwer już działa — nie odpalamy drugi raz
    try:
        with socket.create_connection(("127.0.0.1", 5000), timeout=0.5):
            yield "http://127.0.0.1:5000"
            return
    except OSError:
        pass

    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    try:
        _wait_for_5000()
        yield "http://127.0.0.1:5000"
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


@pytest.fixture(scope="session")
def credentials():
    return EMAIL, PASSWORD


@pytest.fixture
def ensure_logged_in():
    """
    Zwraca funkcję: ensure_logged_in(page, base_url, credentials)
    (jako fixture, więc w testach nie robisz żadnych importów)
    """
    def _login(page: Page, server_base_url: str, credentials_tuple):
        email, password = credentials_tuple

        page.goto(f"{server_base_url}/auth/login", wait_until="domcontentloaded")

        page.locator('input[placeholder="np. mojmail@example.com"]').fill(email)
        page.locator('input[type="password"]').fill(password)

        page.get_by_role("button", name="Zaloguj się").click()

        # potwierdzenie że jesteśmy zalogowani (masz "Witaj, ...")
        page.get_by_text("Witaj").first.wait_for(timeout=20000)

    return _login


@pytest.fixture
def open_first_article_detail():
    """
    Zwraca funkcję: open_first_article_detail(page, base_url, section="crime")
    Klucz: NIE używamy wait_for_url() (bo czeka na 'load' i potrafi wisieć).
    """
    def _open(page: Page, server_base_url: str, section: str = "crime") -> str:
        # idziemy na listę
        page.goto(f"{server_base_url}/news/{section}", wait_until="domcontentloaded")

        # bierzemy pierwszy link do detalu
        link = page.locator('a[href^="/news/detail/"]').first
        link.wait_for(state="visible", timeout=20000)
        href = link.get_attribute("href")
        assert href, "Brak href w linku do detalu"

        # idziemy bezpośrednio na detail (commit = najszybsze i nie wisi na 'load')
        page.goto(f"{server_base_url}{href}", wait_until="commit", timeout=60000)

        # upewniamy się że jesteśmy na /news/detail/
        assert "/news/detail/" in page.url, f"Nie weszło na detail, url={page.url}"

        # i czekamy na element z detail, który potwierdza render
        page.locator("button.bookmark-btn").first.wait_for(state="visible", timeout=60000)

        # zwróć id artykułu (przyda się w testach)
        btn = page.locator("button.bookmark-btn").first
        article_id = btn.get_attribute("data-article-id") or ""
        return article_id

    return _open
