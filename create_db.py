from app import create_app, db
from app import models
from serwis_info.modules.exchange.db.connection import engine, Base
from serwis_info.modules.exchange.db.models import UserEconomyPreferences
from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime
from app.models import User

app = create_app()

with app.app_context():
    # Utwórz tabele dla głównej aplikacji
    db.create_all()
    print("[OK] Tabele glownej aplikacji utworzone.")
    
    # Dodaj tabelę user do metadata modułu exchange, aby klucz obcy działał
    # Używamy tego samego engine, więc tabela już istnieje, ale musimy ją zarejestrować w metadata
    user_table = Table(
        'user',
        Base.metadata,
        Column('id', Integer, primary_key=True),
        Column('email', String(120)),
        Column('nickname', String(64)),
        Column('password_hash', String(200)),
        Column('created_at', DateTime),
        extend_existing=True
    )
    
    # Utwórz tabele dla modułu exchange
    Base.metadata.create_all(bind=engine)
    print("[OK] Tabele modulu exchange utworzone.")
    print(f"[OK] Baza danych: {engine.url}")
    print("Baza danych gotowa.")
