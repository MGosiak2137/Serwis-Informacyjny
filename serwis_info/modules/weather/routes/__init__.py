from .dashboard_routes import register_dashboard_routes
from .history_routes import register_history_routes
from .user_routes import register_user_routes

def register_routes(bp):
    register_dashboard_routes(bp)
    register_history_routes(bp)
    register_user_routes(bp)
