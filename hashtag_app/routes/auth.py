from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.get("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    return render_template("register.html")


@auth_bp.post("/register")
def register_post():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    display_name = (request.form.get("display_name") or "").strip() or None

    if not email or "@" not in email:
        flash("Введіть коректний email.", "danger")
        return redirect(url_for("auth.register"))
    if len(password) < 6:
        flash("Пароль має бути мінімум 6 символів.", "danger")
        return redirect(url_for("auth.register"))

    existing = User.query.filter_by(email=email).first()
    if existing:
        flash("Користувач з таким email вже існує. Увійдіть.", "warning")
        return redirect(url_for("auth.login"))

    user = User(email=email, display_name=display_name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    flash("Реєстрація успішна!", "success")
    return redirect(url_for("main.index"))


@auth_bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    return render_template("login.html")


@auth_bp.post("/login")
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        flash("Невірний email або пароль.", "danger")
        return redirect(url_for("auth.login"))

    login_user(user)
    flash("Вхід виконано.", "success")
    return redirect(url_for("main.index"))


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з акаунта.", "info")
    return redirect(url_for("main.index"))


