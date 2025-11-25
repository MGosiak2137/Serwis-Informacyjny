import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "users.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# tabela użytkowników
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE
)
""")

# tabela historii
c.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    query TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
""")

conn.commit()
print(">>> USING DATABASE:", DB_PATH)
