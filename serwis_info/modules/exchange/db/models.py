from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from .connection import Base

class UserEconomyPreferences(Base):
    __tablename__ = "user_economy_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    favorite_actions = Column(JSON, default=[])
    currencies = Column(ARRAY(String), default=[])
    search_history = Column(JSON, default=[])
