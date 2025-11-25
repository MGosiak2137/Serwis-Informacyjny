from app import create_app, db
from app import models

app = create_app()

with app.app_context():
    db.create_all()
    print("Baza danych gotowa.")
