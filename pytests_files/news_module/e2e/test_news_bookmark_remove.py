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


def ensure_logged_in(page, server_base_url):
    page.goto(f"{server_base_url}/auth/login", wait_until="domcontentloaded")

    email_input = page.locator('input[placeholder="np. mojmail@example.com"]')
    email_input.wait_for(state="visible", timeout=15000)
    email_input.fill(EMAIL)

    password_input = page.locator('input[type="password"]')
    password_input.wait_for(state="visible", timeout=15000)
    password_input.fill(PASSWORD)

    page.get_by_role("button", name="Zaloguj się").click()
    page.wait_for_load_state("domcontentloaded")


def _open_first_article_detail(page, server_base_url):
    page.goto(f"{server_base_url}/news/", wait_until="domcontentloaded")
    page.locator('a[href^="/news/detail/"]').first.click()
    page.wait_for_load_state("domcontentloaded")
    assert "/news/detail/" in page.url


def _set_bookmark_state(page, desired: str):
    """
    desired: "true" albo "false"
    """
    btn = page.locator("button.bookmark-btn").first
    btn.wait_for(state="visible", timeout=15000)

    current = (btn.get_attribute("data-is-bookmarked") or "").lower()
    if current == desired:
        return

    btn.click()
    page.wait_for_timeout(700)

    # czasem atrybut zmienia się z opóźnieniem
    current = (btn.get_attribute("data-is-bookmarked") or "").lower()
    if current != desired:
        page.wait_for_timeout(700)
        current = (btn.get_attribute("data-is-bookmarked") or "").lower()

    assert current == desired


def test_bookmark_can_be_removed_and_stays_removed(page, server_base_url):
    ensure_logged_in(page, server_base_url)
    _open_first_article_detail(page, server_base_url)

    # 1) Upewnij się, że jest zapisany
    _set_bookmark_state(page, "true")

    # 2) Usuń zakładkę
    _set_bookmark_state(page, "false")

    # 3) Odśwież i sprawdź, że nadal false
    page.reload(wait_until="domcontentloaded")
    btn = page.locator("button.bookmark-btn").first
    btn.wait_for(state="visible", timeout=15000)
    persisted = (btn.get_attribute("data-is-bookmarked") or "").lower()
    assert persisted == "false"
