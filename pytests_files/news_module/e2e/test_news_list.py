import os
import subprocess
import time
import socket
import pytest

EMAIL = "e2e@example.com"
PASSWORD = "E2eTest!1"


def _wait_for_5000(timeout: float = 20.0) -> None:
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

    proc = subprocess.Popen(
        ["python", "app.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
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


EMAIL = "e2e@example.com"
PASSWORD = "E2eTest!1"

def ensure_logged_in(page, server_base_url):
    page.goto(f"{server_base_url}/auth/login", wait_until="domcontentloaded")

    # stabilny selektor po placeholderze z Twojego UI
    email_input = page.locator('input[placeholder="np. mojmail@example.com"]')
    email_input.wait_for(state="visible", timeout=15000)
    email_input.fill(EMAIL)

    password_input = page.locator('input[type="password"]')
    password_input.wait_for(state="visible", timeout=15000)
    password_input.fill(PASSWORD)

    page.get_by_role("button", name="Zaloguj się").click()
    page.wait_for_load_state("domcontentloaded")


def test_news_list_renders(page, server_base_url):
    ensure_logged_in(page, server_base_url)

    page.goto(f"{server_base_url}/news/", wait_until="domcontentloaded")
    articles = page.locator('a[href^="/news/detail/"]')
    assert articles.count() > 0


