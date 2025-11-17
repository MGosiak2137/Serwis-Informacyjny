from ..db.history_repository import (
    add_history_entry, trim_history, get_history, clear_history, get_top_cities
)

HISTORY_LIMIT = 200

def add_city_to_history(user_id, city):
    add_history_entry(user_id, city)
    trim_history(user_id, HISTORY_LIMIT)
