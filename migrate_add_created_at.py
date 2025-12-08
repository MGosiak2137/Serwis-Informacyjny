from app import create_app, db
from app.models import User
from datetime import datetime

app = create_app()

with app.app_context():
    try:
        try:
            db.session.execute(db.text("SELECT created_at FROM user LIMIT 1"))
            print("Column 'created_at' already exists. Migration not needed.")
        except Exception:
            # Column doesn't exist, add it
            print("Adding 'created_at' column to user table...")
            
            # SQLite ALTER TABLE ADD COLUMN
            db.session.execute(db.text("ALTER TABLE user ADD COLUMN created_at DATETIME"))
            db.session.commit()
            print("Column 'created_at' added successfully.")
            
            # Set default value for existing users (use current time as fallback)
            default_date = datetime.utcnow()
            db.session.execute(
                db.text("UPDATE user SET created_at = :date WHERE created_at IS NULL"),
                {"date": default_date}
            )
            db.session.commit()
            print(f"Set default creation date ({default_date}) for existing users.")
        
        print("Migration completed successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error during migration: {e}")
        print("Please check your database manually.")
