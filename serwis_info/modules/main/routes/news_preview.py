import os
import json
from flask import current_app

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
