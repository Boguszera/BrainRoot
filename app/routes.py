# trasy odpowiedzialne za mapowanie URL i funkcje aplikacji
from unicodedata import category

from flask import render_template, request, redirect, url_for, session
from . import db
from .models import Word
from .word_service import get_random_word, good_answer

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


def lesson():
    correct_answers = session.get('correct_answers', 0)  # counter poprawnych odpowiedzi (jesli istnieje w sesji pobiera, jesli nie to domyslna wartosc 0)
    category_name = session.get('category_name')

    if not category_name:
        categories = Word.query.with_entities(
            Word.category).distinct().all()  # przeszukanie kolumny kategorii, wybranie unikalnych wyników i przekazanie w postaci listy krotek
        if not categories:
            message = "Brak dostępnych kategorii."
            return render_template('lesson.html', categories=[], category_name=None, message=message)

        if request.method == 'POST':
            selected_category = request.form['category']
            session['category_name'] = selected_category
            category_name = selected_category
        else:
            return render_template('lesson.html', categories=categories, category_name = None)

        # przejscie do lekcji pobieranie danych sesji (jesli jest juz zapisane)
    if 'word' in session and 'correct_translation' in session:
        word = session['word']
        correct_translation = session['correct_translation']
    else:
        # losowanie nowego slowa
        word_object = get_random_word(category_name)
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
        action = request.form.get('action')
        if not action:
            return render_template('lesson.html', word=word, message=message, category_name=category_name)
        user_translation = request.form['translation']
        if action == "Sprawdź odpowiedź":
            if user_translation.lower() == correct_translation.lower():
                good_answer(word)
                message = "Gratulacje! Poprawne tłumaczenie."
                correct_answers += 1
                session['correct_answers'] = correct_answers
            else:
                message = f"Zła odpowiedź :( Poprawne tłumaczenie to: {correct_translation}."
        elif action == "Nie wiem":
            message = f"Poprawne tłumaczenie to: {correct_translation}"
        # generowanie nowego slowa
        new_word_object = get_random_word(category_name)
        if new_word_object and correct_answers <= 20:
            session['word'] = new_word_object.word
            session['correct_translation'] = new_word_object.translation
        else:
            session.pop('word', None)
            session.pop('correct_translation', None)
            session.pop('correct_answers', None)
            session.pop('category_name', None)
            return render_template('endlesson.html')

        return render_template('lesson.html', word=new_word_object.word if new_word_object else None, message=message, category_name=category_name)

    return render_template('lesson.html', word=word, message=message, category_name=category_name)
