import os
import json

from cffi.cffi_opcode import PRIM_ULONG
from flask import current_app
from google.protobuf.text_format import PrintField

'''
def load_news_preview(limit=3):
    path = os.path.join(
        current_app.root_path,
        "serwis_info",
        "news",
        "static",
        "sport_news_data.json"
    )

    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data[:limit]

    except Exception:
        return []
'''


def load_news_preview(limit=3):
    """
    Ładuje artykuły ze sport i crime, łączy je, sortuje po dacie (najnowsze pierwsz).
    Zwraca limit artykułów z obrazkami.
    """
    from datetime import datetime

    root = current_app.root_path  # .../serwis_info

    sport_path = os.path.join(
        root, "modules", "news", "services", "articles_sport.json"
    )
    crime_path = os.path.join(
        root, "modules", "news", "services", "articles_crime.json"
    )

    all_articles = []

    # Ładuj artykuły sportowe
    try:
        if os.path.exists(sport_path):
            with open(sport_path, "r", encoding="utf-8") as f:
                sport_data = json.load(f)
            if isinstance(sport_data, list):
                all_articles.extend(sport_data)
    except Exception as e:
        current_app.logger.exception("_load_news_preview: błąd czytania articles_sport.json: %s", e)

    # Ładuj artykuły z brodni
    try:
        if os.path.exists(crime_path):
            with open(crime_path, "r", encoding="utf-8") as f:
                crime_data = json.load(f)
            if isinstance(crime_data, list):
                all_articles.extend(crime_data)
    except Exception as e:
        current_app.logger.exception("_load_news_preview: błąd czytania articles_crime.json: %s", e)

    if not all_articles:
        current_app.logger.warning("_load_news_preview: brak artykułów w obu plikach")
        return []

    # Spłaszczanie zagnieżdżonych list
    flattened = []
    for item in all_articles:
        if isinstance(item, list):
            flattened.extend(item)
        else:
            flattened.append(item)


    # Normalizacja i parsowanie dat
    normalized = []

    for entry in flattened:
        if not isinstance(entry, dict):
            continue

        # Parsuj datę
        date_str = entry.get("date")
        try:
            if date_str:
                article_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            else:
                article_date = datetime.min
        except Exception:
            article_date = datetime.min

        images = entry.get("images") or []
        image_url = None
        if isinstance(images, list) and images:
            image_url = images[0]

        # Zajawka z contentu
        summary = ""
        content = entry.get("content")
        if isinstance(content, list) and content:
            summary = content[0]

        if image_url:  # tylko artykuły z obrazkami
            normalized.append(
                {
                    "title": entry.get("title", ""),
                    "summary": summary,
                    "image_url": image_url,
                    "source_url": entry.get("url"),
                    "date": article_date,
                    "category": entry.get("category", ""),
                    "id": entry.get("id_number", ""),
                }
            )



    normalized.sort(key=lambda x: x["date"].replace(tzinfo=None), reverse=True)


    seen_result_ids = set()
    seen_result_titles = set()
    result = []
    skip = False
    skip_category = None

    for news in normalized:
        news_id = news.get("id", "")
        title = news.get("title", "")

        # JEŚLI JUŻ MAMY TEN ID W WYNIKACH - POMIJAM
        if news_id in seen_result_ids:
            continue

        if title in seen_result_titles:
            continue

        if skip:
            if news.get("category", "") == skip_category:
                continue

        seen_result_ids.add(news_id)
        seen_result_titles.add(title)
        result.append(news)

        if len(result) == 2 and not skip:
            category_1 = result[0].get("category", "")
            category_2 = result[1].get("category", "")
            if category_1 == category_2:
                skip = True
                skip_category = category_1

        if len(result) >= limit:
            break


    return result
