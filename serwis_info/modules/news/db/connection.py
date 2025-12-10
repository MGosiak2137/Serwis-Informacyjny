import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "news.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# tabela użytkowników
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE
)
""")

# tabela bookmarków artykułów
c.execute("""
CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    article_id TEXT NOT NULL,
    article_title TEXT NOT NULL,
    article_category TEXT,
    article_summary TEXT,
    article_source TEXT,
    article_url TEXT,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, article_id)
)
""")

conn.commit()
print(">>> USING DATABASE:", DB_PATH)

