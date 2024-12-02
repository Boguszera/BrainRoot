# trasy odpowiedzialne za mapowanie URL i funkcje aplikacji
from flask import render_template, request, redirect, url_for, session
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
    # pobieranie danych sesji (jesli jest juz zapisane)
    if 'word' in session and 'correct_translation' in session:
        word = session['word']
        correct_translation = session['correct_translation']
    else:
        # losowanie nowego slowa
        word_object = Word.query.order_by(db.func.random()).first()
        if not word_object:  # obsluga sytuacji, kiedy nie ma slow w bazie
            message = "Brak słów w bazie danych. Proszę dodać słowa."
            return render_template('lesson.html', word=None, message=message)

        # zapis nowego slowa i tlumaczenia do sesji
        word = word_object.word
        correct_translation = word_object.translation
        session['word'] = word
        session['correct_translation'] = correct_translation

    message = None
    if request.method == 'POST':
        # pobranie odpowiedzi użytkownika
        user_translation = request.form['translation']
        if user_translation.lower() == correct_translation.lower():
            message = "Gratulacje! Poprawne tłumaczenie."
        else:
            message = f"Zła odpowiedź :( Poprawne tłumaczenie to: {correct_translation}."

        # generowanie nowego slowa
        new_word_object = Word.query.order_by(db.func.random()).first()
        if new_word_object:
            session['word'] = new_word_object.word
            session['correct_translation'] = new_word_object.translation
        else:
            session.pop('word', None)
            session.pop('correct_translation', None)
            message = "Brak więcej słów w bazie danych."

        return render_template('lesson.html', word=new_word_object.word if new_word_object else None, message=message)

    return render_template('lesson.html', word=word, message=message)


