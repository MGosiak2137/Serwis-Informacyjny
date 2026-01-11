from flask import Blueprint, render_template, jsonify, current_app, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user
from app import db
from app.models import User
from app.forms import ChangePasswordForm
import os
import json
import threading

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

@main_bp.route("/account/more-options")
@login_required
def account_more_options():
    # Check if there's an error parameter (from failed password change)
    # If so, repopulate form with errors from flash messages
    form = ChangePasswordForm()
    return render_template("account_more_options.html", form=form)

@main_bp.route("/account/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    # Check if request came from more-options page
    from_more_options = request.args.get("from") == "more-options" or request.form.get("from") == "more-options"
    
    if form.validate_on_submit():
        # Verify current password
        user = User.query.get(current_user.id)
        if not user.check_password(form.current_password.data):
            flash("Obecne hasło jest niepoprawne.", "danger")
            if from_more_options:
                return render_template("account_more_options.html", form=form)
            return render_template("change_password.html", form=form)
        
        # Check if new password is different from current password
        if user.check_password(form.new_password.data):
            flash("Nowe hasło musi różnić się od obecnego hasła.", "danger")
            if from_more_options:
                return render_template("account_more_options.html", form=form)
            return render_template("change_password.html", form=form)
        
        # Update password
        try:
            user.set_password(form.new_password.data)
            db.session.commit()
            # Logout user after successful password change for security
            logout_user()
            flash("Hasło zostało pomyślnie zmienione. Zaloguj się ponownie używając nowego hasła.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error changing password: {e}")
            flash("Wystąpił błąd podczas zmiany hasła. Spróbuj ponownie.", "danger")
            if from_more_options:
                return render_template("account_more_options.html", form=form)
            return render_template("change_password.html", form=form)
    
    # Handle GET requests or validation failures - render appropriate template
    if from_more_options:
        return render_template("account_more_options.html", form=form)
    
    return render_template("change_password.html", form=form)

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

    # Serve gold data immediately from cache (fast)
    gold_history = []
    try:
        gold_history = exchange_service.get_gold_history(90)
    except Exception:
        gold_history = []

    # Use cached latest price (fast) rather than blocking network call
    gold_price = exchange_service.get_cached_latest_price()

    # Obtain last known FX rates quickly from in-memory cache (may be None)
    eur_pln, usd_pln = exchange_service.get_last_rates()

    # If we don't have rates yet, trigger a background refresh (non-blocking)
    if eur_pln is None or usd_pln is None:
        try:
            threading.Thread(target=exchange_service.get_currency_rates, daemon=True).start()
        except Exception:
            pass

    # fetch small FX histories for USD/PLN and EUR/PLN (last 30 days) — prefer fast cached histories and refresh in background if short
    usd_history = []
    eur_history = []
    try:
        usd_history = exchange_service.get_cached_currency_history('USD', 'PLN', 30)
    except Exception:
        usd_history = []
    try:
        eur_history = exchange_service.get_cached_currency_history('EUR', 'PLN', 30)
    except Exception:
        eur_history = []

    # if cached histories are missing or too short, trigger a background fetch to populate them
    try:
        if not usd_history or len(usd_history) < 30:
            threading.Thread(target=exchange_service.get_currency_history, args=('USD', 'PLN', 30), daemon=True).start()
    except Exception:
        pass
    try:
        if not eur_history or len(eur_history) < 30:
            threading.Thread(target=exchange_service.get_currency_history, args=('EUR', 'PLN', 30), daemon=True).start()
    except Exception:
        pass

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