import sys
import os

# dodanie katalogu 'app' do ścieżki importu
if 'app' not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

import pytest
from app import create_app
from app.models import db, Word, Category

@pytest.fixture
def app():
    """tworzenie testowej instancji appki flask z bazą"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """zwraca klienta testowego flask"""
    return app.test_client()

@pytest.fixture
def init_db(app):
    """tworzenie przykładowych dane testowe"""
    with app.app_context():
        db.session.query(Word).delete()
        db.session.query(Category).delete()
        db.session.commit()

        category = Category(name="Testowa Kategoria")
        word = Word(word="dog", translation="pies", category=category)
        db.session.add_all([category, word])
        db.session.commit()
