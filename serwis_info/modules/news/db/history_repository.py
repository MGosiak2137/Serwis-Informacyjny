from datetime import datetime
from .connection import c, conn


def add_viewed_article(
    user_id: int,
    article_id: str,
    article_title: str,
) -> bool:
    viewed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Jeśli już istnieje, to aktualizuj "viewed_at" + dane (ostatnie wejście wygrywa)
        c.execute(
            """
            INSERT INTO articles_history (user_id, article_id, article_title, viewed_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, article_id) DO UPDATE SET
                article_title=excluded.article_title,
                viewed_at=excluded.viewed_at
            """,
            (user_id, article_id, article_title, viewed_at),
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding viewed article: {e}")
        return False


def get_recent_viewed_articles(user_id: int, limit: int = 10) -> list[dict]:
    try:
        c.execute(
            """
            SELECT article_id, article_title, viewed_at
            FROM articles_history
            WHERE user_id=?
            ORDER BY viewed_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        )
        rows = c.fetchall()
        return [
            {
                "article_id": row[0],
                "article_title": row[1],
                "viewed_at": row[2],
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Error getting viewed history: {e}")
        return []

