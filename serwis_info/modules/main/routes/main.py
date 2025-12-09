from flask import Blueprint, render_template, jsonify, current_app, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from app import db
from app.models import User
import os
import json

main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/main",
    template_folder="../templates",
    static_folder="../static",
)


@main_bp.get("/")
def index():
    from flask import session
    news_preview = _load_news_preview()
    show_welcome = session.pop('show_welcome_modal', False)
    return render_template("index.html",
                           news_preview=news_preview,
                           body_class="home-page",
                           show_welcome_modal=show_welcome)

@main_bp.route("/account")
@login_required
def account_settings():
    return render_template("account_settings.html")

@main_bp.route("/account/delete", methods=["POST"])
@login_required
def delete_account():
    """Delete the current user's account"""
    try:
        user = User.query.get(current_user.id)
        if user:
            # Logout the user first
            logout_user()
            # Delete the user from database
            db.session.delete(user)
            db.session.commit()
            flash("Twoje konto zostało trwale usunięte.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Nie znaleziono użytkownika.", "danger")
            return redirect(url_for("main.account_settings"))
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting account: {e}")
        flash("Wystąpił błąd podczas usuwania konta. Spróbuj ponownie.", "danger")
        return redirect(url_for("main.account_settings"))

@main_bp.get("/api/calendar")
def get_calendar():
    from serwis_info.modules.main.routes import calendar_service
    data = calendar_service.get_calendar_data()
    return jsonify(data)

@main_bp.route("/api/exchange")
def home():
    from serwis_info.modules.main.routes import exchange_service
    eur_pln, usd_pln = exchange_service.get_currency_rates()
    gold_price = exchange_service.get_gold_price()
    # attempt to fetch historical gold prices (last 90 days)
    gold_history = []
    try:
        gold_history = exchange_service.get_gold_history(90)
    except Exception:
        gold_history = []

    # fetch small FX histories for USD/PLN and EUR/PLN (last 30 days)
    usd_history = []
    eur_history = []
    try:
        usd_history = exchange_service.get_currency_history('USD', 'PLN', 30)
    except Exception:
        usd_history = []
    try:
        eur_history = exchange_service.get_currency_history('EUR', 'PLN', 30)
    except Exception:
        eur_history = []

    return jsonify(
        eur_pln=eur_pln,
        usd_pln=usd_pln,
        gold_price=gold_price,
        gold_history=gold_history,
        usd_history=usd_history,
        eur_history=eur_history,
        rates_debug=getattr(exchange_service, 'LAST_RATES_DEBUG', None),
    )

def _load_news_preview(limit=3):
    from serwis_info.modules.main.routes import news_preview
    return news_preview.load_news_preview(limit=limit)