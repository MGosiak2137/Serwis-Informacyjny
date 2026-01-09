# tests/e2e/news/test_news_bookmark_remove.py

from playwright.sync_api import Page


def _wait_until_bookmark_attr(page: Page, desired: str, timeout_ms: int = 20000) -> None:
    page.wait_for_function(
        """
        (desired) => {
          const btn = document.querySelector('button.bookmark-btn');
          if (!btn) return false;
          const v = (btn.getAttribute('data-is-bookmarked') || '').toLowerCase();
          return v === desired;
        }
        """,
        arg=desired,
        timeout=timeout_ms,
    )


def _set_bookmark_state_on_detail(page: Page, desired: str) -> None:
    """
    Na stronie detail: desired = "true"/"false"
    """
    btn = page.locator("button.bookmark-btn").first
    btn.wait_for(state="visible", timeout=20000)

    current = (btn.get_attribute("data-is-bookmarked") or "").lower()
    if current == desired:
        return

    btn.click()
    _wait_until_bookmark_attr(page, desired, timeout_ms=30000)


def _open_bookmarks_via_nav(page: Page) -> None:
    link = page.get_by_role("link", name="Zakładki").first
    link.wait_for(state="visible", timeout=20000)
    link.click()
    page.wait_for_url("**/news/bookmarks", timeout=30000)
    page.wait_for_load_state("domcontentloaded")


from playwright.sync_api import Page


def _remove_bookmark_on_bookmarks_page(page: Page, article_id: str) -> None:
    """
    Usuwa zakładkę na /news/bookmarks klikając zieloną ikonę zakładki
    w tej samej karcie, która ma link do /news/detail/<article_id>.
    """

    # 1) znajdź link do detail w zakładkach
    detail_link = page.locator(f'a[href="/news/detail/{article_id}"]').first
    detail_link.wait_for(state="visible", timeout=20000)

    # 2) weź "kartę" / "kontener" tego wpisu (najbliższy ancestor)
    #    (działa niezależnie czy to <article> czy <div>)
    card = detail_link.locator("xpath=ancestor::*[self::article or self::div][1]")

    # 3) w tej karcie znajdź ikonę/przycisk zakładki (zielona ikonka)
    #    najczęściej to <i class="bi bi-bookmark-fill"> albo podobnie
    icon = card.locator("i.bi-bookmark-fill, i.bi-bookmark").first

    # czasem ikona jest w buttonie – klikniemy button jeśli istnieje
    btn = card.locator("button:has(i.bi-bookmark-fill), button:has(i.bi-bookmark)").first

    if btn.count() > 0:
        btn.wait_for(state="visible", timeout=20000)
        btn.click()
    else:
        # fallback: klik w samą ikonę (czasem nie ma buttona)
        icon.wait_for(state="visible", timeout=20000)
        icon.click(force=True)

    # 4) po kliknięciu wpis powinien zniknąć z zakładek
    page.wait_for_function(
        """
        (id) => !document.querySelector(`a[href="/news/detail/${id}"]`)
        """,
        arg=article_id,
        timeout=30000,
    )



def test_bookmark_remove_flow(
    page,
    server_base_url,
    credentials,
    ensure_logged_in,
    open_first_article_detail,
):
    """
    Kolejność:
    1) zaznacza zakładkę
    2) odświeża stronę
    3) sprawdza czy stan zakładki się nie zmienił
    4) wchodzi do Zakładek z nav i sprawdza czy zakładka jest
    5) usuwa zakładkę na stronie Zakładek
    6) wraca do artykułu i sprawdza, że zakładka jest niezapisana
    """

    page.set_default_timeout(20000)

    login = ensure_logged_in
    open_detail = open_first_article_detail

    # 0) login
    login(page, server_base_url, credentials)

    # 0.5) otwórz detail i weź article_id
    article_id = open_detail(page, server_base_url, section="crime")
    assert article_id, "Nie udało się pobrać data-article-id z przycisku zakładki w detail"

    # 1) zaznacz zakładkę
    _set_bookmark_state_on_detail(page, "true")

    # 2) odśwież detail
    page.reload(wait_until="domcontentloaded")
    page.locator("button.bookmark-btn").first.wait_for(state="visible", timeout=20000)

    # 3) stan nadal true
    persisted = (page.locator("button.bookmark-btn").first.get_attribute("data-is-bookmarked") or "").lower()
    assert persisted == "true"

    # 4) wejdź w Zakładki i sprawdź, że jest wpis
    _open_bookmarks_via_nav(page)
    assert page.locator(f'[data-article-id="{article_id}"]').count() > 0, (
        f"Nie znaleziono zakładki na /news/bookmarks dla article_id={article_id}"
    )

    # 5) usuń ją na stronie zakładek
    _remove_bookmark_on_bookmarks_page(page, article_id)
    assert page.locator(f'[data-article-id="{article_id}"]').count() == 0

    # 6) wróć do detail i sprawdź, że false
    page.goto(f"{server_base_url}/news/detail/{article_id}", wait_until="domcontentloaded")
    page.locator("button.bookmark-btn").first.wait_for(state="visible", timeout=20000)

    _wait_until_bookmark_attr(page, "false", timeout_ms=30000)
    final_state = (page.locator("button.bookmark-btn").first.get_attribute("data-is-bookmarked") or "").lower()
    assert final_state == "false"
