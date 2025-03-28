# konfiguracja aplikacji
import os
from dotenv import load_dotenv

# ładowanie zmiennych z pliku .env
load_dotenv()

class Config:
    # Klucz do zabezpieczania sesji i formularzy
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

    # URL bazy danych
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///default.db')

    # Włączenie/wyłączenie śledzenia zmian w bazie danych
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ustawienie trybu debugowania
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'

    # Ustawienie środowiska Flask (development/production)
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
