import json
from datetime import datetime, timedelta


def _make_articles():
    now = datetime.utcnow()
    return [
        {
            "id": 1,
            "id_number": "1",
            "title": "Napad w Krakowie",
            "category": "crime",
            "content": ["To jest skrót."],
            "published_at": now - timedelta(hours=1),
        },
        {
            "id": 2,
            "id_number": "2",
            "title": "Mecz Ekstraklasy",
            "category": "sport",
            "content": ["Relacja z meczu."],
            "published_at": now,
        },
    ]


def test_news_home_ok(client, fake_login, monkeypatch):
    import serwis_info.modules.news.routes.news_page as news_page

    sample = _make_articles()

    def fake_load(kind):
        if kind == "crime":
            return [a for a in sample if a["category"] == "crime"]
        if kind == "sport":
            return [a for a in sample if a["category"] == "sport"]
        return sample

    monkeypatch.setattr(news_page, "load_articles", fake_load)

    resp = client.get("/news/")
    assert resp.status_code == 200


def test_crime_list_ok(client, fake_login, monkeypatch):
    import serwis_info.modules.news.routes.news_page as news_page

    sample = [a for a in _make_articles() if a["category"] == "crime"]
    monkeypatch.setattr(news_page, "load_articles", lambda kind: sample)

    # bookmarks service stub
    class _BS:
        @staticmethod
        def fetch_user_bookmarks(user_id):
            return [{"article_id": "1"}]

    monkeypatch.setattr(news_page, "bookmarks_service", _BS)

    resp = client.get("/news/crime")
    assert resp.status_code == 200
    # Akceptuj zarówno wersję bez ogonków, jak i poprawną z diakrytykami
    assert (b"Wiadomosci" in resp.data) or ("Wiadomości".encode("utf-8") in resp.data)


def test_sport_list_ok(client, fake_login, monkeypatch):
    import serwis_info.modules.news.routes.news_page as news_page
    sample = [a for a in _make_articles() if a["category"] == "sport"]
    monkeypatch.setattr(news_page, "load_articles", lambda kind: sample)

    class _BS:
        @staticmethod
        def fetch_user_bookmarks(user_id):
            return [{"article_id": "2"}]

    monkeypatch.setattr(news_page, "bookmarks_service", _BS)

    resp = client.get("/news/sport")
    assert resp.status_code == 200


def test_search_page_ok(client, fake_login):
    resp = client.get("/news/search")
    assert resp.status_code == 200


def test_search_results_filters_by_query(client, fake_login, monkeypatch):
    import serwis_info.modules.news.routes.news_page as news_page

    monkeypatch.setattr(news_page, "load_articles", lambda kind: _make_articles())

    class _HS:
        @staticmethod
        def get_view_history(user_id, limit=10):
            return []

    monkeypatch.setattr(news_page, "history_service", _HS)

    resp = client.get("/news/search/results?q=Napad&scope=all")
    assert resp.status_code == 200
    assert b"Napad" in resp.data


def test_detail_not_found(client, fake_login, monkeypatch):
    import serwis_info.modules.news.routes.news_page as news_page
    monkeypatch.setattr(news_page, "load_articles", lambda kind: _make_articles())

    # also stub used services to avoid side effects
    class _BS:
        @staticmethod
        def is_bookmarked(user_id, article_id):
            return False

    class _HS:
        @staticmethod
        def record_view(user_id, article):
            return None

    monkeypatch.setattr(news_page, "bookmarks_service", _BS)
    monkeypatch.setattr(news_page, "history_service", _HS)

    resp = client.get("/news/detail/999")
    assert resp.status_code == 404


def test_bookmarks_page_ok(client, fake_login, monkeypatch):
    import serwis_info.modules.news.routes.news_page as news_page

    class _BS:
        @staticmethod
        def fetch_user_bookmarks(user_id):
            return [
                {
                    "article_id": "2",
                    "article_title": "Mecz Ekstraklasy",
                    "article_summary": "Relacja z meczu.",
                    "article_category": "sport",
                }
            ]

    monkeypatch.setattr(news_page, "bookmarks_service", _BS)

    resp = client.get("/news/bookmarks")
    assert resp.status_code == 200
    assert b"Mecz Ekstraklasy" in resp.data


def test_api_bookmark_add_success(client, fake_login, monkeypatch):
    import serwis_info.modules.news.routes.news_page as news_page

    class _BS:
        @staticmethod
        def add_article_to_bookmarks(*args, **kwargs):
            return True

    monkeypatch.setattr(news_page, "bookmarks_service", _BS)

    payload = {
        "article_id": "123",
        "article_title": "Tytu2",
    }
    resp = client.post(
        "/news/api/bookmark/add",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True


def test_api_bookmark_add_missing_id(client, fake_login):
    resp = client.post(
        "/news/api/bookmark/add",
        data=json.dumps({"article_title": "X"}),
        content_type="application/json",
    )
    assert resp.status_code == 400


def test_api_bookmark_remove_success(client, fake_login, monkeypatch):
    import serwis_info.modules.news.routes.news_page as news_page

    class _BS:
        @staticmethod
        def remove_article_from_bookmarks(*args, **kwargs):
            return True

    monkeypatch.setattr(news_page, "bookmarks_service", _BS)

    resp = client.post(
        "/news/api/bookmark/remove",
        data=json.dumps({"article_id": "123"}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True


def test_api_bookmark_remove_missing_id(client, fake_login):
    resp = client.post(
        "/news/api/bookmark/remove",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert resp.status_code == 400
