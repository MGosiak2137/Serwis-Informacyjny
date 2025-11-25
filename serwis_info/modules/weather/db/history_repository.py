from .connection import c, conn
from datetime import datetime

def add_history_entry(username, query):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO history (username, query, timestamp) VALUES (?, ?, ?)", (username, query, timestamp))
    conn.commit()

def get_history(username):
    c.execute("SELECT query, timestamp FROM history WHERE username=? ORDER BY id DESC", (username,))
    return [{"city": row[0], "timestamp": row[1]} for row in c.fetchall()]

def get_history_last3(username):
    c.execute("SELECT query, timestamp FROM history WHERE username=? ORDER BY id DESC LIMIT 3", (username,))
    return [{"city": row[0], "timestamp": row[1]} for row in c.fetchall()]

def clear_history(username):
    c.execute("DELETE FROM history WHERE username=?", (username,))
    conn.commit()
