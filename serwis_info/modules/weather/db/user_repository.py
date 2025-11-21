from .connection import c, conn

def get_user_id(username:str) -> int:
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    row = c.fetchone()

    if row:
        return row[0]
    
    c.execute("INSERT INTO users (username) VALUES (?)", (username,))

    conn.commit()
    return c.lastrowid


