from .connection import c, conn
from datetime import datetime

def add_bookmark(user_id, article_id, article_title, article_category=None, article_summary=None, article_source=None, article_url=None):
    """Dodaj artykuł do bookmarków użytkownika"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        c.execute("""
            INSERT INTO bookmarks (user_id, article_id, article_title, article_category, article_summary, article_source, article_url, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, article_id, article_title, article_category, article_summary, article_source, article_url, timestamp))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding bookmark: {e}")
        return False

def remove_bookmark(user_id, article_id):
    """Usuń artykuł z bookmarków użytkownika"""
    try:
        c.execute("DELETE FROM bookmarks WHERE user_id=? AND article_id=?", (user_id, article_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error removing bookmark: {e}")
        return False

def get_user_bookmarks(user_id):
    """Pobierz wszystkie bookmarki użytkownika"""
    try:
        c.execute("""
            SELECT id, article_id, article_title, article_category, article_summary, article_source, article_url, timestamp
            FROM bookmarks
            WHERE user_id=?
            ORDER BY timestamp DESC
        """, (user_id,))
        rows = c.fetchall()
        return [{
            "bookmark_id": row[0],
            "article_id": row[1],
            "article_title": row[2],
            "article_category": row[3],
            "article_summary": row[4],
            "article_source": row[5],
            "article_url": row[6],
            "timestamp": row[7]
        } for row in rows]
    except Exception as e:
        print(f"Error getting bookmarks: {e}")
        return []

def is_bookmarked(user_id, article_id):
    """Sprawdź czy artykuł jest w bookmarkach użytkownika"""
    try:
        c.execute("SELECT id FROM bookmarks WHERE user_id=? AND article_id=?", (user_id, article_id))
        return c.fetchone() is not None
    except Exception as e:
        print(f"Error checking bookmark: {e}")
        return False

