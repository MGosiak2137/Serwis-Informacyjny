import os
import subprocess
import time
import socket
import re
import pytest
import sys

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
        [sys.executable, "app.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    try:
        try:
            _wait_for_5000()
        except Exception as e:
            output = ""
            try:
                if proc.stdout:
                    output = proc.stdout.read()
            except Exception:
                output = "<failed to read process stdout>"
            raise RuntimeError(
                "Server did not start on port 5000 in time. Process output:\n" + output
            ) from e
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


def _find_search_input(page):

    cand = page.locator('input[type="search"]')
    if cand.count() > 0:
        return cand.first


    cand = page.locator('input[placeholder*="szuk" i], input[placeholder*="wyszuk" i]')
    if cand.count() > 0:
        return cand.first


    section = page.get_by_text("Wyszukiwarka").first
    section.wait_for(timeout=10000)
    inputs = page.locator("input")
    return inputs.first  # fallback


def test_search_filters_articles(page, server_base_url):
    ensure_logged_in(page, server_base_url)

    page.goto(f"{server_base_url}/news/", wait_until="domcontentloaded")


    first_link = page.locator('a[href^="/news/detail/"]').first
    first_link.wait_for(state="visible", timeout=15000)
    title = first_link.inner_text().strip()
    assert title


    words = re.findall(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{5,}", title)
    query = words[0] if words else title[:6]
    assert query

    search_input = _find_search_input(page)
    search_input.wait_for(state="visible", timeout=15000)


    search_input.fill(query)


    search_input.press("Enter")
    page.wait_for_timeout(500)


    results = page.locator('a[href^="/news/detail/"]')
    assert results.count() > 0


    page_text = page.locator("body").inner_text().lower()
    assert query.lower() in page_text
