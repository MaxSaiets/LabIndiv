import os


class Config:
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
        self.SQLALCHEMY_DATABASE_URI = _normalize_database_url(
            os.getenv("DATABASE_URL", "sqlite:///local.db")
        )
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        # Hugging Face API налаштування
        self.HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
        self.HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "facebook/bart-large-cnn")
        # Google Colab альтернатива (якщо використовується власна модель)
        self.COLAB_API_URL = os.getenv("COLAB_API_URL")  # URL до API на Google Colab


def _normalize_database_url(url: str) -> str:
    # Render often provides postgres://... which SQLAlchemy doesn’t accept directly.
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


