from flask import Blueprint, render_template, jsonify, current_app, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user
from app import db
from app.models import User
from app.forms import ChangePasswordForm
import os
import json

main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/main",
    template_folder="../templates",
    static_folder="../static",
)

def _load_news_preview(limit=3):
    """
    Zwraca listę maks. `limit` newsów do karuzeli na stronie głównej.

    Najpierw próbujemy wziąć dane z articles_sport.json (tam są obrazki),
    a jeśli się nie uda – fallback do sport_news_data.json.
    Zwracamy uproszczoną listę słowników:
    {
        "title": ...,
        "summary": ...,
        "image_url": ... albo None,
        "source_url": ...
    }
    """
    root = current_app.root_path  # .../serwis_info

    # 1) nowy plik z obrazkami
    articles_path = os.path.join(
        root, "modules", "news", "static", "articles_sport.json"
    )
    # 2) stary plik bez obrazków
    old_sport_path = os.path.join(
        root, "modules", "news", "static", "sport_news_data.json"
    )

    current_app.logger.info(
        "_load_news_preview: sprawdzam %s", articles_path
    )
    current_app.logger.info(
        "_load_news_preview: sprawdzam %s", old_sport_path
    )

    json_path = None
    prefer_articles = False

    if os.path.exists(articles_path):
        json_path = articles_path
        prefer_articles = True
    elif os.path.exists(old_sport_path):
        json_path = old_sport_path

    if json_path is None:
        current_app.logger.warning(
            "_load_news_preview: brak pliku z newsami"
        )
        return []

    current_app.logger.info(
        "_load_news_preview: używam pliku %s", json_path
    )

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        current_app.logger.exception(
            "_load_news_preview: błąd czytania JSON: %s", e
        )
        return []

    # --- przypadek 1: articles_sport.json (lista LIST, w każdej 1 dict) ---
    if prefer_articles:
        if not isinstance(data, list):
            current_app.logger.warning(
                "articles_sport.json nie jest listą"
            )
            return []

        result = []
        for entry_list in data:
            if not entry_list:
                continue

            # element może być listą lub już słownikiem
            if isinstance(entry_list, list):
                entry = entry_list[0]
            else:
                entry = entry_list

            if not isinstance(entry, dict):
                continue

            images = entry.get("images") or []
            image_url = None
            if isinstance(images, list) and images:
                image_url = images[0]

            # bierzemy np. pierwszy fragment contentu jako zajawkę
            summary = ""
            content = entry.get("content")
            if isinstance(content, list) and content:
                summary = content[0]

            result.append(
                {
                    "title": entry.get("title", ""),
                    "summary": summary,
                    "image_url": image_url,
                    "source_url": entry.get("url"),
                }
            )

            if len(result) >= limit:
                break

        return result

    # --- przypadek 2: sport_news_data.json (lista dictów) ---
    if not isinstance(data, list):
        current_app.logger.warning(
            "sport_news_data.json nie jest listą"
        )
        return []

    result = []
    for entry in data[:limit]:
        if not isinstance(entry, dict):
            continue

        result.append(
            {
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "image_url": None,
                "source_url": entry.get("source_url"),
            }
        )

    return result

@main_bp.get("/")
def index():
    from flask import session
    news_preview = _load_news_preview(limit=3)
    show_welcome = session.pop('show_welcome_modal', False)
    return render_template("index.html",
                           news_preview=news_preview,
                           body_class="home-page",
                           show_welcome_modal=show_welcome)

@main_bp.route("/account")
@login_required
def account_settings():
    return render_template("account_settings.html")

@main_bp.route("/account/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Verify current password
        user = User.query.get(current_user.id)
        if not user.check_password(form.current_password.data):
            flash("Obecne hasło jest niepoprawne.", "danger")
            return render_template("change_password.html", form=form)
        
        # Check if new password is different from current password
        if user.check_password(form.new_password.data):
            flash("Nowe hasło musi różnić się od obecnego hasła.", "danger")
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
