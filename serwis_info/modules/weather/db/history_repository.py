from .connection import c, conn

def get_history(user_id: int):
    c.execute("SELECT city FROM history WHERE user_id=? ORDER BY id DESC", (user_id,))
    return c.fetchall()


def add_history_entry(user_id: int, city: str):
    c.execute("INSERT INTO history (user_id, city) VALUES (?, ?)", (user_id, city))
    conn.commit()


def trim_history(user_id: int, limit: int):
    c.execute("""
        DELETE FROM history 
        WHERE id IN (
            SELECT id FROM history
            WHERE user_id=?
            ORDER BY id DESC
            LIMIT  ?
        )
    """, (user_id, limit))
    conn.commit()


def clear_history(user_id: int):
    c.execute("DELETE FROM history WHERE user_id=?", (user_id,))
    conn.commit()


def get_top_cities(user_id: int, limit: int):
    c.execute("""
        SELECT city, COUNT(*) as count 
        FROM history 
        WHERE user_id=? 
        GROUP BY city 
        ORDER BY count DESC 
        LIMIT ?
    """, (user_id, limit))
    return c.fetchall()
