import os
import subprocess
import time
import socket
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

    page.locator('input[placeholder="np. mojmail@example.com"]').fill(EMAIL)
    page.locator('input[type="password"]').fill(PASSWORD)
    page.get_by_role("button", name="Zaloguj się").click()
    page.wait_for_load_state("domcontentloaded")


def test_article_appears_in_history(page, server_base_url):
    ensure_logged_in(page, server_base_url)


    page.goto(f"{server_base_url}/news/", wait_until="domcontentloaded")
    first_link = page.locator('a[href^="/news/detail/"]').first
    title = first_link.inner_text().strip()
    assert title


    first_link.click()
    page.wait_for_load_state("domcontentloaded")
    assert "/news/detail/" in page.url


    page.goto(f"{server_base_url}/news/history", wait_until="domcontentloaded")


    assert page.locator(f"text={title}").count() > 0
