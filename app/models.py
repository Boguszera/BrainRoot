# model i inicjalizacja bazy danych

from flask_sqlalchemy import SQLAlchemy

# inicjalizacja obiektu SQLAlchemy (bazy danych)
db = SQLAlchemy()

# definicja modelu dla bazy slowek
"""
id: klucz podstawowy
word: kolumna przechowujaca slowka
translation: kolumna przechowujaca tlumaczenia
"""


class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    translation = db.Column(db.String(100), nullable=False)

    # definicja metody __repr__ (uzywana do okreslenia, jak obiekt klasy Word zostanie zaprezentowany jako tekst [w celu uzyskania stringa])
    def __repr__(self):
        return f"<Word {self.word} -> {self.translation}"

# funkcja inicjalizujaca baze danych (laczenie instancji SQLAlchemy z aplikacja Flask, tworzenie tabel i kontekst)
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
