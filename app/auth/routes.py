from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app import db
from app.models import User
from app.forms import RegisterForm, LoginForm
from . import auth_bp  # <--- blueprint z __init__.py w tym samym pakiecie



@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # szukamy użytkownika po e-mailu
        user = User.query.filter_by(email=form.email.data).first()

        # sprawdzamy hasło metodą z modelu User
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Zalogowano pomyślnie!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Niepoprawny e-mail lub hasło.", "danger")

    # GET albo błędne dane -> pokaż formularz
    return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # tworzymy nowego usera
        user = User(
            email=form.email.data,
            nickname=form.nickname.data,
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Konto zostało utworzone! Możesz się zalogować.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Zostałaś/eś wylogowana/y.", "info")
    return redirect(url_for("auth.login"))
