# trasy odpowiedzialne za mapowanie URL i funkcje aplikacji

"""
render_template: do renderowania plikow HTML
request: do dostepu do danych przeslanych przez uzytkownika (np. formularzy)
redirect, url_for: do przekierowan uzytkownika do innej strony
db: obiekt SQLAlchemy, do interakcji z baza danych
Word: model reprezentujacy tabele w bazie danych
"""
from flask import render_template, request, redirect, url_for
from . import app, db
from .models import Word


# trasa /lesson
@app.route('lesson', methods=['GET', 'POST'])
def lesson():
    word = Word.query.order_by(db.fucn.random()).first()    # pobieranie losowego slowa
    message = None
    if request.method == 'POST':
        user_translation = request.form['translation']   # pobieranie odpowiedzi uzytkownika
        if user_translation.lower() == word.translation.lower():
            message = "Gratulacje! Poprawne tlumaczenie."
        else:
            message = f"Zla odpowiedz :( Poprawne tlumaczenie to: {word.translation} "
        return render_template('lesson.html', word=word.word, message=message)  # ponowne renderowanie strony
    return render_template('lesson.html', word=word.word, message=message)  # obsluga sytuacji, gdy uzytkownik wchodzi na strone (GET)
