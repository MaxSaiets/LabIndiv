from flask import Blueprint, jsonify, request
from flask_login import current_user

from ..extensions import db
from ..hashtags import generate_hashtags
from ..models import HashtagRequest
from ..ai_summarizer import summarize_text
from ..ai_colab import get_colab_summarizer

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.post("/generate")
def api_generate():
    """
    Генерує хештеги для тексту з використанням ШІ для створення резюме.
    """
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    use_ai = payload.get("use_ai", True)  # Чи використовувати ШІ (за замовчуванням так)
    
    if not text:
        return jsonify({"ok": False, "error": "empty_text"}), 400

    # Генерація резюме за допомогою ШІ
    ai_summary = None
    if use_ai and len(text) > 50:  # Використовуємо ШІ тільки для довгих текстів
        # Спочатку пробуємо Google Colab (якщо налаштовано), потім Hugging Face
        colab_summarizer = get_colab_summarizer()
        if colab_summarizer:
            ai_summary = colab_summarizer.summarize(text, max_length=150, min_length=30)
        
        # Якщо Colab не налаштовано або не спрацював, використовуємо Hugging Face
        if not ai_summary:
            ai_summary = summarize_text(text, max_length=150, min_length=30)
    
    # Генеруємо хештеги на основі резюме (якщо є) або оригінального тексту
    source_text = ai_summary if ai_summary else text
    hashtags, keywords = generate_hashtags(source_text)
    
    saved = False

    if current_user.is_authenticated and hashtags:
        rec = HashtagRequest(
            user_id=current_user.id,
            post_text=text,
            hashtags=" ".join(hashtags),
            ai_summary=ai_summary,
        )
        db.session.add(rec)
        db.session.commit()
        saved = True

    return jsonify(
        {
            "ok": True,
            "hashtags": hashtags,
            "keywords": keywords,
            "ai_summary": ai_summary,
            "saved": saved,
        }
    )


