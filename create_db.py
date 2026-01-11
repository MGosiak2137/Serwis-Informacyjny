from app import create_app, db
from app import models
from serwis_info.modules.exchange.db.connection import engine, Base
from serwis_info.modules.exchange.db.models import UserEconomyPreferences

app = create_app()

with app.app_context():
    # Utwórz tabele dla głównej aplikacji
    db.create_all()
    print("✓ Tabele głównej aplikacji utworzone.")
    
    # Utwórz tabele dla modułu exchange
    Base.metadata.create_all(bind=engine)
    print("✓ Tabele modułu exchange utworzone.")
    print(f"✓ Baza danych: {Base.metadata.bind.url}")
    print("Baza danych gotowa.")
