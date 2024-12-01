# konfiguracja aplikacji
import os

class Config:
    # klucz do zabezpieczania sesji i formularzy, pobierany ze zmiennej srodowiskowej
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

    # konfiguracja bazy danych
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    #okreslenie lokalizacji bazy danych
    SQLALCHEMY_DATABASE_URI = (f"sqlite:///{os.path.join(BASE_DIR, 'words.db')}")

    #wylaczenie sledzenia zmian w celu oszczednosci zasobow
    SQLALCHEMY_TRACK_MODIFICATIONS = False
