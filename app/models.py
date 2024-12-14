# model i inicjalizacja bazy danych

from flask_sqlalchemy import SQLAlchemy

# inicjalizacja obiektu SQLAlchemy (bazy danych)
db = SQLAlchemy()

# definicja modelu dla bazy slowek
"""
id: klucz podstawowy
word: kolumna przechowujaca słówka
translation: kolumna przechowujaca tlumaczenia
category: kolumna przechowująca kategorie/zestaw słówka
correct_answers: liczba poprawnych odpowiedzi
is_proggres: wskazuje czy słowo jest w trakcie nauki (0 - nie, 1 - tak, 2 - w puli powtórek) 
"""


class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    translation = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    correct_answers = db.Column(db.Integer)
    is_progress = db.Column(db.Integer)


    # definicja metody __repr__ (uzywana do okreslenia, jak obiekt klasy Word zostanie zaprezentowany jako tekst [w celu uzyskania stringa])
    def __repr__(self):
        return f"<Word {self.word} -> {self.translation}"

# funkcja inicjalizujaca baze danych (laczenie instancji SQLAlchemy z aplikacja Flask, tworzenie tabel i kontekst)
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
