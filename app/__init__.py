# inicjalizacja aplikacji
from flask import Flask
from .config import Config
from .models import db, init_db
from .routes import init_routes
from app.scripts.seed import seed_data
from .api import api_bp

def create_app():
    # tworzenie instancji aplikacji
    app = Flask(__name__)

    # wczytanie konfiguracji z pliku config.py
    app.config.from_object(Config)

    # inicjalizacja bazy danych
    init_db(app)

    # automatyczne dodanie presetów
    with app.app_context():
        seed_data()

    # blueprint registration
    app.register_blueprint(api.api_bp, url_prefix='/api')

    # Zarejestrowanie tras
    init_routes(app)

    return app