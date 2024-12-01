# inicjalizacja aplikacji
from flask import Flask
from .config import Config
from .models import db, init_db
from .routes import init_routes

def create_app():
    # tworzenie instancji aplikacji
    app = Flask(__name__)

    # wczytanie konfiguracji z pliku config.py
    app.config.from_object(Config)

    # inicjalizacja bazy danych
    init_db(app)

    # Zarejestrowanie tras
    init_routes(app)

    return app