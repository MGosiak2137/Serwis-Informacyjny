from ..db.bookmarks_repository import (
    add_bookmark,
    remove_bookmark,
    get_user_bookmarks,
    is_bookmarked
)

def add_article_to_bookmarks(user_id, article_id, article_title, article_category=None, article_summary=None, article_source=None, article_url=None):
    """Dodaj artykuł do zakładek użytkownika"""
    return add_bookmark(user_id, article_id, article_title, article_category, article_summary, article_source, article_url)

def remove_article_from_bookmarks(user_id, article_id):
    """Usuń artykuł z zakładek użytkownika"""
    return remove_bookmark(user_id, article_id)

def fetch_user_bookmarks(user_id):
    """Pobierz wszystkie zakładki użytkownika"""
    return get_user_bookmarks(user_id)

def check_if_bookmarked(user_id, article_id):
    """Sprawdź czy artykuł jest w zakładkach"""
    return is_bookmarked(user_id, article_id)

