from flask import Flask

from .config import Config
from .extensions import db, login_manager, migrate
from .routes.api import api_bp
from .routes.auth import auth_bp
from .routes.main import main_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config())

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    # Для лабораторної: автоматично створюємо таблиці при першому запуску,
    # щоб на Render не блокуватися на міграціях.
    with app.app_context():
        db.create_all()

    return app


