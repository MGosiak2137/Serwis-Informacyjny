import os
import socket
import subprocess
import sys
import time

import pytest

# Dopasowane do Twojego E2E usera
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

    email_input = page.locator('input[placeholder="np. mojmail@example.com"]')
    email_input.wait_for(state="visible", timeout=15000)
    email_input.fill(EMAIL)

    password_input = page.locator('input[type="password"]')
    password_input.wait_for(state="visible", timeout=15000)
    password_input.fill(PASSWORD)

    page.get_by_role("button", name="Zaloguj się").click()

    # Zamiast load_state: czekamy aż pojawi się coś po zalogowaniu
    # U Ciebie na stronie jest "Witaj, <nick>"
    page.get_by_text("Witaj").first.wait_for(timeout=15000)


def test_open_first_article_detail(page, server_base_url):
    ensure_logged_in(page, server_base_url)

    page.goto(f"{server_base_url}/news/", wait_until="domcontentloaded")

    # Na home /news/ linki do detail są w kafelkach (a[href^="/news/detail/"])
    first_link = page.locator('a[href^="/news/detail/"]').first
    first_link.wait_for(state="visible", timeout=20000)

    href = first_link.get_attribute("href")
    assert href and href.startswith("/news/detail/")

    # Klik i czekanie po URL (najstabilniejsze)
    first_link.click()
    page.wait_for_url("**/news/detail/**", timeout=30000)

    # Upewnij się, że detail się naprawdę wyrenderował
    # (u Ciebie jest h1 i/lub button.bookmark-btn)
    page.locator("h1").first.wait_for(state="visible", timeout=30000)

    assert "/news/detail/" in page.url

    body_text = page.locator("body").inner_text()
    assert len(body_text.strip()) > 200
