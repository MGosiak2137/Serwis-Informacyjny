from .connection import c, conn

DEFAULT_USERNAME = "demo_user"

def get_user_id(username: str | None = None) -> int:
    if not username:
        username = DEFAULT_USERNAME

    c.execute("SELECT id FROM users WHERE username=?", (username,))
    row = c.fetchone()
    if row:
        return row[0]

    # jeśli nie istnieje, utwórz
    c.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    return c.lastrowid
