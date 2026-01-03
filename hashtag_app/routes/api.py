from flask import Blueprint, jsonify, request
from flask_login import current_user

from ..extensions import db
from ..hashtags import generate_hashtags
from ..models import HashtagRequest

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.post("/generate")
def api_generate():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({"ok": False, "error": "empty_text"}), 400

    hashtags, keywords = generate_hashtags(text)
    saved = False

    if current_user.is_authenticated and hashtags:
        rec = HashtagRequest(
            user_id=current_user.id,
            post_text=text,
            hashtags=" ".join(hashtags),
        )
        db.session.add(rec)
        db.session.commit()
        saved = True

    return jsonify(
        {
            "ok": True,
            "hashtags": hashtags,
            "keywords": keywords,
            "saved": saved,
        }
    )


