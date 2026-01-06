from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.sqlite import JSON
from .connection import Base

class UserEconomyPreferences(Base):
    __tablename__ = "user_economy_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)
    favorite_actions = Column(JSON, default=[])
    currencies = Column(JSON, default=[])  # Changed from ARRAY to JSON for SQLite compatibility
    search_history = Column(JSON, default=[])
