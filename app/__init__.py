# inicjalizacja aplikacji
from Flask import flask
from .config import Config
from .models import db, init_db


def create_app():
    # tworzenie instancji aplikacji
    app = Flask(__name__)

    # wczytanie konfiguracji z pliku config.py
    app.config.from_object(Config)

    # inicjalizacja bazy danych
    init_db(app)
    return app
