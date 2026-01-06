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
    first_link = page.locator('a[href^="/news/detail/"]').first
    first_link.wait_for(state="visible", timeout=15000)
    first_link.click()
    page.wait_for_load_state("domcontentloaded")
    assert "/news/detail/" in page.url


def test_bookmark_persists_after_refresh(page, server_base_url):
    ensure_logged_in(page, server_base_url)
    _open_first_article_detail(page, server_base_url)

    bookmark_btn = page.locator("button.bookmark-btn").first
    bookmark_btn.wait_for(state="visible", timeout=15000)

    # Stan początkowy
    initial = (bookmark_btn.get_attribute("data-is-bookmarked") or "").lower()

    # Klikamy, żeby zmienić stan (zwykle false -> true, ale może już być true)
    bookmark_btn.click()
    page.wait_for_timeout(500)  # krótko, bo stan często ustawia JS / fetch

    # Jeśli po kliknięciu nadal jest false, kliknij jeszcze raz (czasem UI odświeża atrybut po chwili)
    after_click = (bookmark_btn.get_attribute("data-is-bookmarked") or "").lower()
    if initial == after_click:
        page.wait_for_timeout(700)
        after_click = (bookmark_btn.get_attribute("data-is-bookmarked") or "").lower()

    # Chcemy, żeby finalnie był zapisany (true)
    if after_click != "true":
        bookmark_btn.click()
        page.wait_for_timeout(700)
        after_click = (bookmark_btn.get_attribute("data-is-bookmarked") or "").lower()

    assert after_click == "true"

    # Odśwież i sprawdź, że nadal zapisany
    page.reload(wait_until="domcontentloaded")
    bookmark_btn = page.locator("button.bookmark-btn").first
    bookmark_btn.wait_for(state="visible", timeout=15000)

    persisted = (bookmark_btn.get_attribute("data-is-bookmarked") or "").lower()
    assert persisted == "true"
