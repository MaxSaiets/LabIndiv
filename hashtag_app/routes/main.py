from collections import Counter
from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

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
        flash("Ім'я занадто довге.", "danger")
        return redirect(url_for("main.profile"))

    current_user.display_name = display_name or None
    db.session.commit()
    flash("Профіль оновлено.", "success")
    return redirect(url_for("main.profile"))


@main_bp.get("/statistics")
@login_required
def statistics():
    """Сторінка статистики з візуалізацією результатів."""
    user_requests = HashtagRequest.query.filter_by(user_id=current_user.id).all()
    
    # Загальна статистика
    total_requests = len(user_requests)
    total_with_ai = sum(1 for r in user_requests if r.ai_summary)
    
    # Статистика по днях (останні 30 днів)
    days_data = {}
    for i in range(30):
        date = (datetime.utcnow() - timedelta(days=i)).date()
        days_data[date.isoformat()] = 0
    
    for req in user_requests:
        date_key = req.created_at.date().isoformat()
        if date_key in days_data:
            days_data[date_key] += 1
    
    # Найпопулярніші хештеги
    all_hashtags = []
    for req in user_requests:
        hashtags = req.hashtags.split()
        all_hashtags.extend([h.replace("#", "") for h in hashtags])
    
    top_hashtags = Counter(all_hashtags).most_common(10)
    
    # Статистика використання ШІ
    ai_usage = {
        "with_ai": total_with_ai,
        "without_ai": total_requests - total_with_ai,
    }
    
    return render_template(
        "statistics.html",
        total_requests=total_requests,
        total_with_ai=total_with_ai,
        days_data=days_data,
        top_hashtags=top_hashtags,
        ai_usage=ai_usage,
    )


