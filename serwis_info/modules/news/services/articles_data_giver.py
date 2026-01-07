from flask import (Blueprint, render_template, request, url_for, redirect)
from datetime import datetime, timezone
import json
import os


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


def load_file_data(file_path):
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', 'services', file_path)
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)


                # Spłaszczanie, jeśli data to lista list
                if data and isinstance(data, list) and isinstance(data[0], list):
                    articles = [item for sublist in data for item in sublist]

                else:
                    articles = data



                # Przetwarzaj artykuły
                for idx, article in enumerate(articles):
                    article['id'] = idx + 1
                    if article.get('date'):
                        try:
                            # parse ISO formats; handle trailing Z
                            s = article['date']
                            if isinstance(s, str) and s.endswith('Z'):
                                s = s.replace('Z', '+00:00')
                            dt = datetime.fromisoformat(s)
                            # Normalize to UTC and make tz-aware
                            if dt.tzinfo is None:
                                dt = dt.replace(tzinfo=timezone.utc)
                            else:
                                dt = dt.astimezone(timezone.utc)
                            article['published_at'] = dt
                        except Exception:
                            article['published_at'] = datetime.utcnow().replace(tzinfo=timezone.utc)
                    else:
                        # set default as UTC-aware now
                        article['published_at'] = datetime.utcnow().replace(tzinfo=timezone.utc)

                return articles
        else:
            print(f"DEBUG: Plik {json_path} nie istnieje.")
    except Exception as e:
        print(f"Error loading sports articles: {e}")
    return []




def load_articles(type_name):
    try:
        if type_name == "sport":
            data = load_file_data('articles_sport.json')
        elif type_name == "crime":
            data = load_file_data('articles_crime.json')
        elif type_name == "all":
            data_sport = load_file_data('articles_sport.json')
            data_crime = load_file_data('articles_crime.json')
            data = data_sport + data_crime
        return data
    except Exception as e:
        print(f"Error loading articles of type {type_name}: {e}")
        return []