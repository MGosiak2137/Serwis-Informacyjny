from flask import Blueprint, render_template, jsonify, current_app
import os
import json

main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/main",
    template_folder="../templates",
    static_folder="../static",
)

def _load_news_preview(limit=3):
    """
    Zwraca listę maks. `limit` newsów do karuzeli na stronie głównej.

    Najpierw próbujemy wziąć dane z articles_sport.json (tam są obrazki),
    a jeśli się nie uda – fallback do sport_news_data.json.
    Zwracamy uproszczoną listę słowników:
    {
        "title": ...,
        "summary": ...,
        "image_url": ... albo None,
        "source_url": ...
    }
    """
    root = current_app.root_path  # .../serwis_info

    # 1) nowy plik z obrazkami
    articles_path = os.path.join(
        root, "modules", "news", "static", "articles_sport.json"
    )
    # 2) stary plik bez obrazków
    old_sport_path = os.path.join(
        root, "modules", "news", "static", "sport_news_data.json"
    )

    current_app.logger.info(
        "_load_news_preview: sprawdzam %s", articles_path
    )
    current_app.logger.info(
        "_load_news_preview: sprawdzam %s", old_sport_path
    )

    json_path = None
    prefer_articles = False

    if os.path.exists(articles_path):
        json_path = articles_path
        prefer_articles = True
    elif os.path.exists(old_sport_path):
        json_path = old_sport_path

    if json_path is None:
        current_app.logger.warning(
            "_load_news_preview: brak pliku z newsami"
        )
        return []

    current_app.logger.info(
        "_load_news_preview: używam pliku %s", json_path
    )

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        current_app.logger.exception(
            "_load_news_preview: błąd czytania JSON: %s", e
        )
        return []

    # --- przypadek 1: articles_sport.json (lista LIST, w każdej 1 dict) ---
    if prefer_articles:
        if not isinstance(data, list):
            current_app.logger.warning(
                "articles_sport.json nie jest listą"
            )
            return []

        result = []
        for entry_list in data:
            if not entry_list:
                continue

            # element może być listą lub już słownikiem
            if isinstance(entry_list, list):
                entry = entry_list[0]
            else:
                entry = entry_list

            if not isinstance(entry, dict):
                continue

            images = entry.get("images") or []
            image_url = None
            if isinstance(images, list) and images:
                image_url = images[0]

            # bierzemy np. pierwszy fragment contentu jako zajawkę
            summary = ""
            content = entry.get("content")
            if isinstance(content, list) and content:
                summary = content[0]

            result.append(
                {
                    "title": entry.get("title", ""),
                    "summary": summary,
                    "image_url": image_url,
                    "source_url": entry.get("url"),
                }
            )

            if len(result) >= limit:
                break

        return result

    # --- przypadek 2: sport_news_data.json (lista dictów) ---
    if not isinstance(data, list):
        current_app.logger.warning(
            "sport_news_data.json nie jest listą"
        )
        return []

    result = []
    for entry in data[:limit]:
        if not isinstance(entry, dict):
            continue

        result.append(
            {
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "image_url": None,
                "source_url": entry.get("source_url"),
            }
        )

    return result

@main_bp.get("/")
def index():
    news_preview = _load_news_preview(limit=3)
    return render_template("index.html",
                           news_preview=news_preview,
                           body_class="home-page")

@main_bp.get("/api/calendar")
def get_calendar():
    """
    Endpoint używany przez script.js: fetch("/main/api/calendar")
    """
    from serwis_info.modules.main.routes import calendar_service
    data = calendar_service.get_calendar_data()
    return jsonify(data)