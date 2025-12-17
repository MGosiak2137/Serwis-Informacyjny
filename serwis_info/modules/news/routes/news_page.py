from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from datetime import datetime, timezone
import json
import os
from flask_login import login_required, current_user


from serwis_info.modules.news.services import articles_data_giver
from serwis_info.modules.news.services import bookmarks_service
from serwis_info.modules.news.services import history_service

_sample_articles = articles_data_giver._sample_articles
_sample_history = articles_data_giver._sample_history
load_articles = articles_data_giver.load_articles


news_bp = Blueprint(
    "news",
    __name__,
    template_folder="../templates",
    static_folder="../static",
    url_prefix="/news",
)


def _sort_articles(articles):
    """Sortuj artykuły malejąco po dacie publikacji (tak jak w listach)."""
    return sorted(
        articles,
        key=lambda a: (a.get("published_at") or datetime.min).replace(tzinfo=None),
        reverse=True,
    )


@news_bp.route("/")
@login_required
def news_home():
    """Strona główna modułu newsowego – dwa kafelki + 5 ostatnich newsów."""
    try:
        crime_articles = load_articles("crime")
        crime_articles = _sort_articles(crime_articles)
    except Exception as e:
        print(f"Error loading crime articles for home: {e}")
        crime_articles = []

    try:
        sport_articles = load_articles("sport")
        sport_articles = _sort_articles(sport_articles)
    except Exception as e:
        print(f"Error loading sport articles for home: {e}")
        sport_articles = []

    crime_latest = crime_articles[:5]
    sport_latest = sport_articles[:5]


    return render_template(
        "nav_footnews.html",
        crime_latest=crime_latest,
        sport_latest=sport_latest,
    )


@news_bp.get("/crime")
@login_required
def crime_list():
    try:
        articles = _sort_articles(load_articles("crime"))
    except Exception as e:
        print(f"Error loading crime articles: {e}")
        articles = []

    # >>> bierzemy z bookmarks_service / repo
    try:
        user_bookmarks = bookmarks_service.fetch_user_bookmarks(current_user.id) or []
        bookmarked_ids = {str(b["article_id"]) for b in user_bookmarks}
    except Exception as e:
        print(f"Error loading bookmarked_ids: {e}")
        bookmarked_ids = set()

    return render_template(
        "crime_news.html",
        articles=articles,
        title="Wiadomości kryminalne",
        bookmarked_ids=bookmarked_ids,
    )



@news_bp.get("/sport")
@login_required
def sport_list():
    try:
        articles = _sort_articles(load_articles("sport"))
    except Exception as e:
        print(f"Error loading sport articles: {e}")
        articles = []

    try:
        user_bookmarks = bookmarks_service.fetch_user_bookmarks(current_user.id) or []
        bookmarked_ids = {str(b["article_id"]) for b in user_bookmarks}
    except Exception as e:
        print(f"Error loading bookmarked_ids: {e}")
        bookmarked_ids = set()

    return render_template(
        "sport_news.html",
        articles=articles,
        title="Wiadomości sportowe",
        bookmarked_ids=bookmarked_ids,
    )




@news_bp.get("/detail/<news_id>")
@login_required
def detail(news_id):
    try:
        articles = load_articles("all")
        article = next((a for a in articles if a.get("id_number") == news_id), None)
        if article is None:
            return "Artykuł nie został znaleziony", 404
    except Exception as e:
        print(f"Error loading article detail: {e}")
        return "Błąd podczas ładowania artykułu", 500

    # >>> TO JEST SYNCHRONIZACJA ZAKŁADKI (ważne)
    try:
        # bookmarks_repository.is_bookmarked(user_id, article_id)
        is_bookmarked_flag = bookmarks_service.is_bookmarked(current_user.id, news_id)
    except Exception as e:
        print(f"Error checking is_bookmarked in detail: {e}")
        is_bookmarked_flag = False

    try:
        history_service.record_view(current_user.id, article)
    except Exception as e:
        print(f"Error recording viewed article: {e}")


    return render_template("detail.html", article=article, is_bookmarked=is_bookmarked_flag)



@news_bp.get("/search")
@login_required
def search():
    try:
        history = history_service.get_view_history(current_user.id, limit=10)
    except Exception as e:
        print(f"Error loading view history: {e}")
        history = []

    return render_template(
        "news_search.html",
        results=None,
        history=history,
        q="",
        scope="all",
        from_date="",
        to_date="",
    )


@news_bp.get("/search/results")
@login_required
def search_results():
    q = request.args.get("q")
    scope = request.args.get("scope", "all")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    articles = []
    results = []

    try:
        if scope == "all":
            articles = load_articles("all")
        elif scope == "sport":
            articles = load_articles("sport")
        elif scope == "crime":
            articles = load_articles("crime")
    except Exception as e:
        print(f"Error loading articles for search: {e}")
        articles = []

    if articles:
        if q:
            q_l = q.lower()
            for a in articles:
                if scope != "all" and a.get("category") != scope:
                    continue
                text = (a.get("title") or "") + " " + " ".join(a.get("content") or [])
                if q_l in text.lower():
                    results.append(a)
        else:
            results = articles

    try:
        history = history_service.get_view_history(current_user.id, limit=10)
    except Exception as e:
        print(f"Error loading view history: {e}")
        history = []


    return render_template(
        "news_search.html",
        results=results,
        history=history,
        q=q,
        scope=scope,
        from_date=from_date,
        to_date=to_date,
    )


# ========== SCRAPOWANE SPORTY – przykładowe ==========

def _load_scraped_sports():
    try:
        json_path = os.path.join(
            os.path.dirname(__file__),
            "../../..",
            "sport_news_data.json",
        )
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for article in data:
                    if isinstance(article.get("published_at"), str):
                        article["published_at"] = datetime.fromisoformat(
                            article["published_at"].replace("Z", "+00:00")
                        )
                return data
    except Exception as e:
        print(f"Error loading scraped sports data: {e}")
    return []


@news_bp.get("/sport/scraped")
def sport_scraped():
    articles = _load_scraped_sports()
    if not articles:
        articles = [a for a in _sample_articles() if a.get("category") == "sport"]
    return render_template("sport_scraped.html", articles=articles)

@news_bp.get("/bookmarks")
@login_required
def bookmarks():
    # Pobierz zakładki zalogowanego użytkownika i przekaż je do szablonu
    try:
        user_bookmarks = bookmarks_service.fetch_user_bookmarks(current_user.id) or []
        # Normalizuj nazwy pól, żeby szablon mógł korzystać z `summary` i `category`
        for b in user_bookmarks:
            # repo zwraca article_summary/article_category; wystawimy też krótsze klucze
            if 'summary' not in b:
                b['summary'] = b.get('article_summary')
            if 'category' not in b:
                b['category'] = b.get('article_category')
        return render_template("bookmarks.html", bookmarked_articles=user_bookmarks)
    except Exception as e:
        print(f"Error loading bookmarks page: {e}")
        return render_template("bookmarks.html", bookmarked_articles=[])


# API endpoints for bookmarks
@news_bp.post('/api/bookmark/add')
@login_required
def api_bookmark_add():
    """API: Dodaj artykuł do zakładek dla zalogowanego użytkownika."""
    try:
        data = request.get_json() or {}
        article_id = data.get('article_id')
        title = data.get('article_title') or ''
        category = data.get('article_category') or None
        summary = data.get('article_summary') or None
        source = data.get('article_source') or None
        url = data.get('article_url') or None

        if not article_id:
            return jsonify({'success': False, 'error': 'Brak article_id'}), 400

        ok = bookmarks_service.add_article_to_bookmarks(current_user.id, article_id, title, category, summary, source, url)
        if ok:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'DB error'}), 500

    except Exception as e:
        print(f"Error in api_bookmark_add: {e}")
        return jsonify({'success': False, 'error': 'Internal error'}), 500


@news_bp.post('/api/bookmark/remove')
@login_required
def api_bookmark_remove():
    """API: Usuń artykuł z zakładek zalogowanego użytkownika."""
    try:
        data = request.get_json() or {}
        article_id = data.get('article_id')
        if not article_id:
            return jsonify({'success': False, 'error': 'Brak article_id'}), 400

        ok = bookmarks_service.remove_article_from_bookmarks(current_user.id, article_id)
        if ok:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'DB error'}), 500
    except Exception as e:
        print(f"Error in api_bookmark_remove: {e}")
        return jsonify({'success': False, 'error': 'Internal error'}), 500