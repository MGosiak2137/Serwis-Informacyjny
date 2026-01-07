from ..db.history_repository import (
    add_viewed_article,
    get_recent_viewed_articles
)


def record_view(user_id: int, article: dict) -> None:
    # Bezpieczne pobranie pól
    article_id = str(article.get("id_number") or article.get("id") or "")
    if not article_id:
        return

    title = (article.get("title") or "").strip() or "Bez tytułu"

    add_viewed_article(
        user_id=user_id,
        article_id=article_id,
        article_title=title,
    )


def get_view_history(user_id: int, limit: int = 10) -> list[dict]:
    return get_recent_viewed_articles(user_id=user_id, limit=limit)

