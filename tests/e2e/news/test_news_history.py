import os
import socket
import subprocess
import sys
import time

import pytest

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
def server_base_url():
    env = os.environ.copy()
    env["NEWS_DB_PATH"] = r"serwis_info\modules\news\test_news.db"

    # Jeśli serwer już działa — nie uruchamiamy ponownie
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


def ensure_logged_in(page, server_base_url: str) -> None:
    page.goto(f"{server_base_url}/auth/login", wait_until="domcontentloaded")

    page.locator('input[placeholder="np. mojmail@example.com"]').fill(EMAIL)
    page.locator('input[type="password"]').fill(PASSWORD)

    page.get_by_role("button", name="Zaloguj się").click()

    # stabilne potwierdzenie logowania
    page.get_by_text("Witaj").first.wait_for(timeout=15000)


def test_article_appears_in_history(page, server_base_url):
    ensure_logged_in(page, server_base_url)

    # 1) Wejdź na /news/ i otwórz pierwszy artykuł
    page.goto(f"{server_base_url}/news/", wait_until="domcontentloaded")

    first_link = page.locator('a[href^="/news/detail/"]').first
    first_link.wait_for(state="visible", timeout=20000)

    href = first_link.get_attribute("href")
    assert href and href.startswith("/news/detail/")

    # weź tytuł z detail (najpewniejsze), a nie z linka
    first_link.click()
    page.wait_for_url("**/news/detail/**", timeout=30000)

    h1 = page.locator("h1").first
    h1.wait_for(state="visible", timeout=30000)
    title = h1.inner_text().strip()
    assert title

    # 2) Przejdź do strony, która u Ciebie renderuje historię: /news/search
    page.goto(f"{server_base_url}/news/search", wait_until="domcontentloaded")

    # 3) Sprawdź, że tytuł pojawił się w historii
    # (robimy contains-match, bo czasem są skróty/ellipsis)
    page.get_by_text(title, exact=False).first.wait_for(timeout=15000)
    assert page.get_by_text(title, exact=False).count() > 0
# File: tests/e2e/news/test_news_history.py
import pytest


def ui_login(page, base_url: str, credentials: dict) -> None:
    page.goto(f"{base_url}/auth/login", wait_until="domcontentloaded")
    page.locator('input[placeholder="np. mojmail@example.com"]').wait_for(state="visible", timeout=15000)
    page.locator('input[placeholder="np. mojmail@example.com"]').fill(credentials["email"])
    page.locator('input[type="password"]').wait_for(state="visible", timeout=15000)
    page.locator('input[type="password"]').fill(credentials["password"])
    page.get_by_role("button", name="Zaloguj się").click()
    page.get_by_text("Witaj").first.wait_for(timeout=15000)


def test_article_appears_in_history(page, e2e_server, credentials):
    ui_login(page, e2e_server, credentials)

    page.goto(f"{e2e_server}/news/", wait_until="domcontentloaded")

    first_link = page.locator('a[href^="/news/detail/"]').first
    first_link.wait_for(state="visible", timeout=20000)

    href = first_link.get_attribute("href")
    assert href and href.startswith("/news/detail/")

    first_link.click()
    page.wait_for_url("**/news/detail/**", timeout=30000)

    h1 = page.locator("h1").first
    h1.wait_for(state="visible", timeout=30000)
    title = h1.inner_text().strip()
    assert title

    page.goto(f"{e2e_server}/news/search", wait_until="domcontentloaded")

    page.get_by_text(title, exact=False).first.wait_for(timeout=15000)
    assert page.get_by_text(title, exact=False).count() > 0