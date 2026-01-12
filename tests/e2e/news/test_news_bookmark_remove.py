from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import time


def _get_bookmark_state_detail(page: Page) -> str:
    """
    Zwraca 'true'/'false' dla przycisku zakładki na stronie detail.
    Najpierw próbuje data-is-bookmarked, a jeśli front tego nie aktualizuje,
    to robi fallback na klasę ikony (bi-bookmark-fill).
    """
    btn = page.locator("button.bookmark-btn").first
    if btn.count() == 0:
        return "false"

    attr = (btn.get_attribute("data-is-bookmarked") or "").lower().strip()
    if attr in ("true", "false"):
        return attr

    # fallback: ikona (często tylko to jest aktualizowane przez JS)
    icon_fill = btn.locator("i.bi-bookmark-fill").count() > 0
    return "true" if icon_fill else "false"


def _wait_until_bookmark_attr(page: Page, desired: str, timeout_ms: int = 20000) -> None:
    desired = desired.lower().strip()
    deadline = time.time() + timeout_ms / 1000.0

    while True:
        state = _get_bookmark_state_detail(page)
        if state == desired:
            print(f"DEBUG: bookmark state reached desired='{desired}'")
            return

        if time.time() >= deadline:
            raise AssertionError(f"Timeout waiting for bookmark state='{desired}', current='{state}'")

        time.sleep(0.05)


def _set_bookmark_state_on_detail(page: Page, desired: str, max_retries: int = 3) -> None:
    desired = desired.lower().strip()

    btn = page.locator("button.bookmark-btn").first
    btn.wait_for(state="visible", timeout=20000)

    article_id = btn.get_attribute("data-article-id") or btn.get_attribute("data-id") or ""
    current = _get_bookmark_state_detail(page)
    print("DEBUG before click, state:", current, "article_id:", article_id)

    if current == desired:
        return

    for attempt in range(1, max_retries + 1):
        try:
            def _predicate(resp):
                try:
                    if "/news/api/bookmark/" not in resp.url:
                        return False
                    if resp.request.method not in ("POST", "DELETE", "PUT"):
                        return False
                    return True
                except Exception:
                    return False

            with page.expect_response(_predicate, timeout=15000) as resp_info:
                btn.click()
            resp = resp_info.value
            print(f"DEBUG network response status: {resp.status} url: {resp.url} attempt:{attempt}")

            if resp.status in (200, 204):
                _wait_until_bookmark_attr(page, desired, timeout_ms=30000)
                after = _get_bookmark_state_detail(page)
                print("DEBUG after wait, state:", after)

                # stabilizacja
                time.sleep(0.15)
                still = _get_bookmark_state_detail(page)
                if after == desired and still == desired:
                    return
                else:
                    print(f"DEBUG attempt {attempt}: state flipped (after={after}, still={still})")
            else:
                print(f"DEBUG unexpected status {resp.status} on attempt {attempt}")

        except PlaywrightTimeoutError:
            print(f"DEBUG attempt {attempt}: timeout waiting for network response")
        except AssertionError as e:
            print(f"DEBUG attempt {attempt}: assertion/wait error: {e}")

        time.sleep(0.2)

    final = _get_bookmark_state_detail(page)
    raise AssertionError(f"Failed to set bookmark to '{desired}', final state='{final}'")


def _open_bookmarks_via_nav(page: Page) -> None:
    link = page.get_by_role("link", name="Zakładki").first
    link.wait_for(state="visible", timeout=20000)
    link.click()
    page.wait_for_url("**/news/bookmarks", timeout=30000)
    page.wait_for_load_state("domcontentloaded")


def _remove_bookmark_on_bookmarks_page(page: Page, article_id: str) -> None:
    detail_link = page.locator(f'a[href="/news/detail/{article_id}"]').first
    detail_link.wait_for(state="visible", timeout=20000)

    card = detail_link.locator("xpath=ancestor::*[self::article or self::div][1]")

    # klik w przycisk (preferowane), a jak nie ma, to w ikonę
    btn = card.locator("button:has(i.bi-bookmark-fill), button:has(i.bi-bookmark)").first
    icon = card.locator("i.bi-bookmark-fill, i.bi-bookmark").first

    if btn.count() > 0:
        btn.wait_for(state="visible", timeout=20000)
        btn.click()
    else:
        icon.wait_for(state="visible", timeout=20000)
        icon.click(force=True)

    page.wait_for_function(
        """
        (id) => !document.querySelector(`a[href="/news/detail/${id}"]`)
        """,
        arg=article_id,
        timeout=30000,
    )


def ui_login(page: Page, base_url: str, credentials: dict) -> None:
    page.goto(f"{base_url}/auth/login", wait_until="domcontentloaded")
    page.locator('input[placeholder="np. mojmail@example.com"]').wait_for(state="visible", timeout=15000)
    page.locator('input[placeholder="np. mojmail@example.com"]').fill(credentials["email"])
    page.locator('input[type="password"]').wait_for(state="visible", timeout=15000)
    page.locator('input[type="password"]').fill(credentials["password"])
    page.get_by_role("button", name="Zaloguj się").click()
    page.get_by_text("Witaj").first.wait_for(timeout=15000)


def open_first_article_detail(page: Page, base_url: str, section: str = "crime") -> str:
    page.goto(f"{base_url}/news/{section}", wait_until="domcontentloaded")

    first_link = page.locator('a[href^="/news/detail/"]').first
    first_link.wait_for(state="visible", timeout=20000)
    first_link.click()
    page.wait_for_url("**/news/detail/**", timeout=30000)

    btn = page.locator("button.bookmark-btn").first
    btn.wait_for(state="visible", timeout=15000)

    article_id = btn.get_attribute("data-article-id") or btn.get_attribute("data-id") or ""
    if not article_id:
        url = page.url
        if "/news/detail/" in url:
            article_id = url.split("/news/detail/")[-1].split("/")[0]

    assert article_id, "Nie udało się pobrać article_id z detail"
    return article_id


def test_bookmark_remove_flow(page, e2e_server, credentials):
    page.set_default_timeout(20000)

    ui_login(page, e2e_server, credentials)

    article_id = open_first_article_detail(page, e2e_server, section="crime")
    assert article_id, "Nie udało się pobrać article_id z detail"

    # 1) Ustaw zakładkę na true (na detail)
    _set_bookmark_state_on_detail(page, "true")

    # 2) Reload i upewnij się, że stan jest zapisany
    page.reload(wait_until="domcontentloaded")
    page.locator("button.bookmark-btn").first.wait_for(state="visible", timeout=20000)

    persisted = _get_bookmark_state_detail(page)
    assert persisted == "true"

    # 3) Przejdź do zakładek i usuń
    _open_bookmarks_via_nav(page)

    # tutaj nie zakładamy, że jest data-article-id w DOM zakładek,
    # bo u Ciebie usuwanie działało po linku /news/detail/<id>
    assert page.locator(f'a[href="/news/detail/{article_id}"]').count() > 0, (
        f"Nie znaleziono zakładki na /news/bookmarks dla article_id={article_id}"
    )

    _remove_bookmark_on_bookmarks_page(page, article_id)
    assert page.locator(f'a[href="/news/detail/{article_id}"]').count() == 0

    # 4) Wróć na detail i sprawdź, że jest false
    page.goto(f"{e2e_server}/news/detail/{article_id}", wait_until="domcontentloaded")
    page.locator("button.bookmark-btn").first.wait_for(state="visible", timeout=20000)

    _wait_until_bookmark_attr(page, "false", timeout_ms=30000)
    final_state = _get_bookmark_state_detail(page)
    assert final_state == "false"
