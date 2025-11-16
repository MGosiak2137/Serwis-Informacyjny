from .connection import c, conn

def get_user_id(username:str) -> int:
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    row = c.fetchone()

    if row:
        return row[0]
    
    c.execute("INSERT ITNO users (username) VALUES (?)", (username,))
    conn.commit()
    return c.lastrowid


def set_default_city(user_id: int, city: str):
    c.execute("UPDATE users SET default_city=? WHERE id=?", (city, user_id))
    conn.commit()