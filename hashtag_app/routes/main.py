from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..models import HashtagRequest

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template("index.html")


@main_bp.get("/history")
@login_required
def history():
    items = (
        HashtagRequest.query.filter_by(user_id=current_user.id)
        .order_by(HashtagRequest.created_at.desc())
        .limit(50)
        .all()
    )
    return render_template("history.html", items=items)


@main_bp.get("/profile")
@login_required
def profile():
    total = (
        HashtagRequest.query.filter_by(user_id=current_user.id).count()
        if current_user.is_authenticated
        else 0
    )
    return render_template("profile.html", total=total)


@main_bp.post("/profile")
@login_required
def profile_post():
    display_name = (request.form.get("display_name") or "").strip()
    if display_name and len(display_name) > 120:
        flash("Ім’я занадто довге.", "danger")
        return redirect(url_for("main.profile"))

    current_user.display_name = display_name or None
    db.session.commit()
    flash("Профіль оновлено.", "success")
    return redirect(url_for("main.profile"))


