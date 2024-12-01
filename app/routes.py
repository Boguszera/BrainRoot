# trasy odpowiedzialne za mapowanie URL i funkcje aplikacji
from flask import render_template, request, redirect, url_for
from . import db
from .models import Word

"""
render_template: do renderowania plikow HTML
request: do dostepu do danych przeslanych przez uzytkownika (np. formularzy)
redirect, url_for: do przekierowan uzytkownika do innej strony
db: obiekt SQLAlchemy, do interakcji z baza danych
Word: model reprezentujacy tabele w bazie danych
"""

# trasa /lesson
def init_routes(app):
    # trasa /lesson
    @app.route('/lesson', methods=['GET', 'POST'])
    def lesson_route():
        return lesson()
def lesson_route():
    return lesson()
def lesson():
    word = Word.query.order_by(db.func.random()).first()    # pobieranie losowego slowa

    # Jeśli nie ma żadnych słów w bazie, wyświetl odpowiedni komunikat
    if word is None:
        message = "Brak słów w bazie danych. Proszę dodać słowa."
        return render_template('lesson.html', word=None, message=message)
    
    message = None
    if request.method == 'POST':
        user_translation = request.form['translation']   # pobieranie odpowiedzi uzytkownika
        if user_translation.lower() == word.translation.lower():
            message = "Gratulacje! Poprawne tlumaczenie."
        else:
            message = f"Zla odpowiedz :( Poprawne tlumaczenie to: {word.translation} "
        return render_template('lesson.html', word=word.word, message=message)  # ponowne renderowanie strony
    return render_template('lesson.html', word=word.word, message=message)  # obsluga sytuacji, gdy uzytkownik wchodzi na strone (GET)


