from .connection import c, conn
import json

def ensure_user_eco_preferences_exists(user_id):
    """Upewnij się, że użytkownik ma rekord w user_eco_preferences"""
    c.execute("SELECT id FROM user_eco_preferences WHERE id=?", (user_id,))
    if not c.fetchone():
        c.execute("""
            INSERT INTO user_eco_preferences (id, favorite_actions, currencies, search_history)
            VALUES (?, ?, ?, ?)
        """, (user_id, '[]', '[]', '[]'))
        conn.commit()

def get_preferences(user_id):
    ensure_user_eco_preferences_exists(user_id)
    
    c.execute("SELECT favorite_actions, currencies, search_history FROM user_eco_preferences WHERE id=?", (user_id,))
    row = c.fetchone()
    if row:
        return {
            "favorite_actions": json.loads(row[0]) if row[0] else [],
            "currencies": json.loads(row[1]) if row[1] else [],
            "search_history": json.loads(row[2]) if row[2] else []
        }
    return {"favorite_actions": [], "currencies": [], "search_history": []}

def update_preferences(user_id, favorite_actions=None, currencies=None, search_history=None):
    ensure_user_eco_preferences_exists(user_id)
    
    prefs = get_preferences(user_id)
    if favorite_actions is not None:
        prefs["favorite_actions"] = favorite_actions
    if currencies is not None:
        prefs["currencies"] = currencies
    if search_history is not None:
        prefs["search_history"] = search_history

    c.execute("""
        UPDATE user_eco_preferences
        SET favorite_actions=?, currencies=?, search_history=?
        WHERE id=?
    """, (
        json.dumps(prefs["favorite_actions"]),
        json.dumps(prefs["currencies"]),
        json.dumps(prefs["search_history"]),
        user_id
    ))
    conn.commit()
