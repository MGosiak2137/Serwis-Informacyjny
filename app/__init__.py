# app/__init__.py
from serwis_info.create_app import create_app, db, login_manager

__all__ = ["create_app", "db", "login_manager"]
