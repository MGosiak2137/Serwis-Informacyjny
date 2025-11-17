from .connection import c, conn

def get_user_id(username:str) -> int:
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    row = c.fetchone()

    if row:
        return row[0]
    
    c.execute("INSERT INTO users (username) VALUES (?)", (username,))

    conn.commit()
    return c.lastrowid


def set_default_city(user_id: int, city: str):
    c.execute("UPDATE users SET default_city=? WHERE id=?", (city, user_id))
    conn.commit()

    
def get_default_city(user_id: int):
    c.execute("SELECT default_city FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    return row[0] if row else None

def clear_default_city(user_id):
    c.execute("UPDATE users SET default_city=NULL WHERE id=?", (user_id,))
    conn.commit()