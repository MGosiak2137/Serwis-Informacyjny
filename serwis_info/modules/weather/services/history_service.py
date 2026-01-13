from ..db.history_repository import add_history_entry, get_history, clear_history

def add_city_to_history(username, city):
    add_history_entry(username, city)

def fetch_history(username):
    return get_history(username)



def clear_user_history(username):
    clear_history(username)
