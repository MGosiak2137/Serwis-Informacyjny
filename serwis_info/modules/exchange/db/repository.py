from sqlalchemy.orm import Session
from .models import UserEconomyPreferences

def get_user_preferences(db: Session, user_id: int):
    return db.query(UserEconomyPreferences).filter(
        UserEconomyPreferences.user_id == user_id
    ).first()

def update_user_preferences(db: Session, user_id: int, favorite_actions: list = None, 
                           currencies: list = None, search_history: list = None):
    prefs = get_user_preferences(db, user_id)
    
    if not prefs:
        prefs = UserEconomyPreferences(user_id=user_id)
        db.add(prefs)
    
    if favorite_actions:
        prefs.favorite_actions = favorite_actions
    if currencies:
        prefs.currencies = currencies
    if search_history:
        prefs.search_history = search_history
    
    db.commit()
    db.refresh(prefs)
    return prefs
