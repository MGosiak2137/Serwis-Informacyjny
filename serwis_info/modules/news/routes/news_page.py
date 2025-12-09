from flask import Blueprint, render_template, request, url_for, redirect
from datetime import datetime, timezone
import json
import os
from flask_login import login_required


from serwis_info.modules.news.services import articles_data_giver

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
        articles = load_articles("crime")
        articles = _sort_articles(articles)
    except Exception as e:
        print(f"Error loading crime articles: {e}")
        articles = []
    return render_template(
        "crime_news.html",
        articles=articles,
        title="Wiadomości kryminalne",
    )


@news_bp.get("/sport")
@login_required
def sport_list():
    try:
        articles = load_articles("sport")
        articles = _sort_articles(articles)
    except Exception as e:
        print(f"Error loading sport articles: {e}")
        articles = []
    return render_template(
        "sport_news.html",
        articles=articles,
        title="Wiadomości sportowe",
    )


@news_bp.get("/detail/<news_id>")
@login_required
def detail(news_id):
    try:
        articles = load_articles("all")
        # znajdź artykuł o podanym id_number
        article = next(
            (a for a in articles if a.get("id_number") == news_id),
            None,
        )
        if article is None:
            return "Artykuł nie został znaleziony", 404
    except Exception as e:
        print(f"Error loading article detail: {e}")
        return "Błąd podczas ładowania artykułu", 500

    return render_template("detail.html", article=article)


@news_bp.get("/search")
@login_required
def search():
    history = _sample_history()
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

    history = _sample_history()
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
def bookmarks():
    return render_template("bookmarks.html")

