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

    # jeśli serwer już działa na 5000 — nie odpalamy drugi raz
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

    # Stabilne potwierdzenie, że login się udał
    page.get_by_text("Witaj").first.wait_for(timeout=15000)


def test_news_list_renders(page, server_base_url):
    ensure_logged_in(page, server_base_url)

    page.goto(f"{server_base_url}/news/", wait_until="domcontentloaded")

    # Na stronie /news/ masz listę newsów z linkami /news/detail/<id>
    articles = page.locator('a[href^="/news/detail/"]')
    assert articles.count() > 0
