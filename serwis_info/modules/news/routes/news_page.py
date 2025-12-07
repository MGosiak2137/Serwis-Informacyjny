from flask import Blueprint, render_template, request, url_for, redirect
from datetime import datetime,timezone
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


@news_bp.get("/")
@login_required
def news_home():
    return render_template("nav_footnews.html")

@news_bp.get("/crime")
def crime_list():
    try:
        articles = load_articles("crime")
        articles = sorted(
            articles,
            key=lambda a: (a.get("published_at") or datetime.min).replace(tzinfo=None),
            reverse=True
        )
    except Exception as e:
        print(f"Error loading crime articles: {e}")
        articles = []
    return render_template("crime_news.html", articles=articles, title="Wiadomości kryminalne")


@news_bp.get("/sport")
def sport_list():
    try:
        articles = load_articles("sport")
        articles = sorted(
            articles,
            key=lambda a: (a.get("published_at") or datetime.min).replace(tzinfo=None),
            reverse=True
        )
    except Exception as e:
        print(f"Error loading sport articles: {e}")
        articles = []
    return render_template("sport_news.html", articles=articles, title="Wiadomości sportowe")


@news_bp.get("/detail/<news_id>")
def detail(news_id):
    try:
        articles = load_articles("all")
        for article in articles:
            if article.get("id_number") == news_id:
                break
        if not article:
            return "Artykuł nie został znaleziony", 404
    except Exception as e:
        print(f"Error loading article detail: {e}")
        return "Błąd podczas ładowania artykułu", 500
    return render_template("detail.html", article=article)


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
    try:
        if scope == "all":
            articles = load_articles("all")
        elif scope == "sport":
            articles = load_articles("sport")
        elif scope == "crime":
            articles = load_articles("crime")
    except:
        print("Error loading articles for search")

    if articles:
        results = []

        if q:
            q_l = q.lower()
            for a in articles:
                if scope != "all" and a.get("category") != scope:
                    continue
                if q_l in (a.get("title") or "").lower() or q_l in " ".join(a.get("content") or []).lower():
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
