import os
import re
import socket
import subprocess
import sys
import time

import pytest

EMAIL = "e2e@example.com"
PASSWORD = "E2eTest!1"


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


def ensure_logged_in(page, server_base_url: str):
    page.goto(f"{server_base_url}/auth/login", wait_until="domcontentloaded")

    page.locator('input[placeholder="np. mojmail@example.com"]').fill(EMAIL)
    page.locator('input[type="password"]').fill(PASSWORD)

    page.get_by_role("button", name="Zaloguj się").click()
    page.wait_for_load_state("domcontentloaded")


def _pick_query_from_first_article(page, server_base_url: str, section: str = "crime") -> str:
    # Uwaga: listy są pod /news/crime i /news/sport
    page.goto(f"{server_base_url}/news/{section}", wait_until="domcontentloaded")

    # Na listach masz overlay .news-card-link z href do /news/detail/<id>
    first_link = page.locator('a.news-card-link[href^="/news/detail/"]').first
    if first_link.count() == 0:
        # fallback: dowolny link do detail
        first_link = page.locator('a[href^="/news/detail/"]').first

    first_link.wait_for(state="visible", timeout=15000)

    # tytuł artykułu jest w h3 a.news-title-link, ale bierzemy z całej karty jako fallback
    card = first_link.locator("xpath=ancestor::article[1]")
    title_text = ""
    title_loc = card.locator("a.news-title-link").first
    if title_loc.count() > 0:
        title_text = title_loc.inner_text().strip()
    else:
        title_text = card.inner_text().strip()

    assert title_text

    words = re.findall(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{5,}", title_text)
    query = words[0] if words else title_text[:6]
    return query


def test_search_filters_articles(page, server_base_url):
    ensure_logged_in(page, server_base_url)

    query = _pick_query_from_first_article(page, server_base_url, section="crime")
    assert query

    # Wyszukiwarka w Twoim module jest na /news/search
    page.goto(f"{server_base_url}/news/search", wait_until="domcontentloaded")

    # Najpewniejsze: input o nazwie q
    search_input = page.locator('input[name="q"]')
    if search_input.count() == 0:
        # fallback: pierwszy input
        search_input = page.locator("input").first

    search_input.wait_for(state="visible", timeout=15000)
    search_input.fill(query)

    # klik przycisku "Szukaj" jeśli istnieje, inaczej Enter
    btn = page.get_by_role("button", name=re.compile(r"Szukaj|Wyszukaj", re.I))
    if btn.count() > 0:
        btn.first.click()
    else:
        search_input.press("Enter")

    # Wyniki są na /news/search/results?... (albo ten sam template po GET)
    page.wait_for_timeout(500)

    # Sprawdzamy, że są wyniki (linki do detail)
    results = page.locator('a[href^="/news/detail/"]')
    assert results.count() > 0

    # I że fraza jest widoczna na stronie wyników
    body = page.locator("body").inner_text().lower()
    assert query.lower() in body
# File: tests/e2e/news/test_news_search.py
import re
import pytest


def ui_login(page, base_url: str, credentials: dict) -> None:
    page.goto(f"{base_url}/auth/login", wait_until="domcontentloaded")
    page.locator('input[placeholder="np. mojmail@example.com"]').wait_for(state="visible", timeout=15000)
    page.locator('input[placeholder="np. mojmail@example.com"]').fill(credentials["email"])
    page.locator('input[type="password"]').wait_for(state="visible", timeout=15000)
    page.locator('input[type="password"]').fill(credentials["password"])
    page.get_by_role("button", name="Zaloguj się").click()
    page.wait_for_load_state("domcontentloaded")


def _pick_query_from_first_article(page, base_url: str, section: str = "crime") -> str:
    page.goto(f"{base_url}/news/{section}", wait_until="domcontentloaded")

    first_link = page.locator('a.news-card-link[href^="/news/detail/"]').first
    if first_link.count() == 0:
        first_link = page.locator('a[href^="/news/detail/"]').first

    first_link.wait_for(state="visible", timeout=15000)

    card = first_link.locator("xpath=ancestor::article[1]")
    title_text = ""
    title_loc = card.locator("a.news-title-link").first
    if title_loc.count() > 0:
        title_text = title_loc.inner_text().strip()
    else:
        title_text = card.inner_text().strip()

    assert title_text

    words = re.findall(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{5,}", title_text)
    query = words[0] if words else title_text[:6]
    return query


def test_search_filters_articles(page, e2e_server, credentials):
    ui_login(page, e2e_server, credentials)

    query = _pick_query_from_first_article(page, e2e_server, section="crime")
    assert query

    page.goto(f"{e2e_server}/news/search", wait_until="domcontentloaded")

    search_input = page.locator('input[name="q"]')
    if search_input.count() == 0:
        search_input = page.locator("input").first

    search_input.wait_for(state="visible", timeout=15000)
    search_input.fill(query)

    btn = page.get_by_role("button", name=re.compile(r"Szukaj|Wyszukaj", re.I))
    if btn.count() > 0:
        btn.first.click()
    else:
        search_input.press("Enter")

    page.wait_for_timeout(500)

    results = page.locator('a[href^="/news/detail/"]')
    assert results.count() > 0

    body = page.locator("body").inner_text().lower()
    assert query.lower() in body