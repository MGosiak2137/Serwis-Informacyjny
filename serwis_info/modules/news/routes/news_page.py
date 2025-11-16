from flask import Blueprint, render_template, request, url_for, redirect
from datetime import datetime
import json
import os


news_bp = Blueprint(
    "news",
    __name__,
    template_folder="../templates",
    static_folder="../static",
    url_prefix="/news",
)


def _sample_articles():
    now = datetime.utcnow()
    return [
        {
            "id": 1,
            "title": "Napad na sklep w centrum Krakowa",
            "published_at": now,
            "source_name": "Policja Małopolska",
            "summary": "Policja zatrzymała podejrzanego o napad na sklep przy ul. Długiej.",
            "source_url": None,
            "category": "crime",
            "league": None,
        },
        {
            "id": 2,
            "title": "Ekstraklasa: remis w meczu na szczycie",
            "published_at": now,
            "source_name": "Ekstraklasa",
            "summary": "Spotkanie lidera z wiceliderem zakończyło się remisem 2:2.",
            "source_url": None,
            "category": "sport",
            "league": "Ekstraklasa",
        },
    ]


def _sample_history():
    return [
        {"query": "napad", "created_at": datetime.utcnow()},
        {"query": "Wisła", "created_at": datetime.utcnow()},
    ]

@news_bp.get("/")
def news_home():
    return render_template("nav_footnews.html")

@news_bp.get("/crime")
def crime_list():
    articles = [a for a in _sample_articles() if a.get("category") == "crime"]
    return render_template("crime_news.html", articles=articles)


@news_bp.get("/sport")
def sport_list():
    # 1. Spróbuj wczytać zeskrapowane newsy sportowe z pliku JSON
    scraped = _load_scraped_sports()

    # 2. Fallback – jeśli nie ma pliku albo jest pusty, dorzuć przykładowe
    if scraped:
        articles = scraped
    else:
        articles = [a for a in _sample_articles() if a.get("category") == "sport"]

    # 3. (opcjonalnie) posortuj po dacie malejąco, jeśli chcesz nowsze na górze
    articles = sorted(
        articles,
        key=lambda a: a.get("published_at") or datetime.min,
        reverse=True,
    )

    return render_template("sport_news.html", articles=articles)


@news_bp.get("/search")
def search():
    history = _sample_history()
    return render_template( "news_search.html", results=None, history=history,q="",scope="all",from_date="",to_date="", )

@news_bp.get("/search/results")
def search_results():
    q = request.args.get("q")
    scope = request.args.get("scope", "all")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")




    # very small in-memory filter over sample articles
    articles = _sample_articles()
    results = []
    if q:
        q_l = q.lower()
        for a in articles:
            if scope != "all" and a.get("category") != scope:
                continue
            if q_l in (a.get("title") or "").lower() or q_l in (a.get("summary") or "").lower():
                results.append(a)

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


@news_bp.get("/detail/<int:news_id>")
def detail(news_id):
    articles = _sample_articles()
    item = next((a for a in articles if a["id"] == news_id), None)
    return render_template("detail.html", article=item)



#DO SCRAPOWANIA PRZYŁADOWE

def _load_scraped_sports():
    try:
        json_path = os.path.join(os.path.dirname(__file__), '../../..', 'sport_news_data.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for article in data:
                    if isinstance(article.get('published_at'), str):
                        article['published_at'] = datetime.fromisoformat(article['published_at'].replace('Z', '+00:00'))
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
