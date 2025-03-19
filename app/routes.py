# trasy odpowiedzialne za mapowanie URL i funkcje aplikacji
from unicodedata import category

from flask import render_template, request, redirect, url_for, session, flash, session
from . import db
from .models import Word
from .word_service import get_random_word, good_answer, handle_review_cycle, increment_lessons, clean_text, handle_review_cycle

"""
render_template: do renderowania plikow HTML
request: do dostepu do danych przeslanych przez uzytkownika (np. formularzy)
redirect, url_for: do przekierowan uzytkownika do innej strony
db: obiekt SQLAlchemy, do interakcji z baza danych
Word: model reprezentujacy tabele w bazie danych
"""

# trasa /lesson
def init_routes(app):
    # trasa dla strony głównej
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/settings', methods=['GET', 'POST'])
    def settings():
        if request.method == 'POST':
            # pobierz dane z formularza
            translation_direction = request.form.get('translation_direction')  # ang -> pl lub pl -> ang
            review_frequency = int(request.form.get('review_frequency', 7))  # domyślnie 7 lekcji
            words_frequency = int(request.form.get('words_frequency', 20))  # domyślnie 20 słów

            # zapisz do sesji
            session['translation_direction'] = translation_direction
            session['review_frequency'] = int(review_frequency)
            session['word_frequency'] = int(words_frequency)

            flash("Ustawienia zapisane!", "success")
            print(f"ZAPISUJĘ USTAWIENIA: {session}")
            return redirect(url_for('settings'))  # Przekierowanie do lekcji po zapisaniu ustawień

        return render_template('settings.html')

    # trasa /lesson
    @app.route('/lesson', methods=['GET', 'POST'])
    def lesson_route():
        return lesson()


def lesson():
    correct_answers = session.get('correct_answers', 0)  # counter poprawnych odpowiedzi (jesli istnieje w sesji pobiera, jesli nie to domyslna wartosc 0)
    category_name = session.get('category_name')
    translation_direction = session.get('translation_direction')  # domyślnie angielski na polski
    word_frequency = session.get('word_frequency', 20)

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
            return render_template('lesson.html', categories=categories, category_name=None)

    # przejscie do lekcji, pobieranie danych sesji (jesli sa juz zapisane)
    if 'word' in session and 'correct_translation' in session:
        word = session['word']
        correct_translation = session['correct_translation']
    else:
        # losowanie nowego słowa
        word_object = get_random_word(category_name)
        if not word_object:  # Jeśli brak słów w bazie
            message = "Brak słów w bazie danych. Proszę dodać słowa."
            return render_template('lesson.html', word=None, message=message)

        # obsługa kierunku tłumaczenia, zapis tlumaczenia do sesji
        if translation_direction == 'ang-pl':
            word = word_object.word
            correct_translation = word_object.translation
        else:
            word = word_object.translation  # Odwracamy kierunek
            correct_translation = word_object.word

        session['word'] = word
        session['correct_translation'] = correct_translation

    # obsługa powtórki
    review_frequency = session.get('review_frequency', 7) # pobieranie wartości z ustawień użytkownia
    words_for_review = Word.query.filter(Word.is_progress == False,
                                         Word.lessons_since_last_review >= review_frequency).all()

    is_review = bool(words_for_review)  # aktywacja trybu powtórek (jeśli są słowa do powtórki)
    review_message = "POWTÓRKA!" if is_review else None

    message = None
    if request.method == 'POST':
        # obsługa odpowiedzi użytkownika
        action = request.form.get('action')
        if not action:
            return render_template('lesson.html', word=word, message=message, category_name=category_name, review_message=review_message)

        user_translation = request.form['translation']

        if action == "Sprawdź odpowiedź":
            if clean_text(user_translation) == clean_text(correct_translation):
                good_answer(word)
                message = "Gratulacje! Poprawne tłumaczenie."
                correct_answers += 1
                session['correct_answers'] = correct_answers
            else:
                message = f"Zła odpowiedź :( Poprawne tłumaczenie to: {correct_translation}."
        elif action == "Nie wiem":
            message = f"Poprawne tłumaczenie to: {correct_translation}"

        # co 7 lekcji aktywujemy powtórki
        if is_review:
            handle_review_cycle()
        increment_lessons()

        # generowanie nowego słowa
        new_word_object = get_random_word(category_name)
        if new_word_object and correct_answers <= (word_frequency - 1):
            if translation_direction == 'ang-pl':
                session['word'] = new_word_object.word
                session['correct_translation'] = new_word_object.translation
            else:
                session['word'] = new_word_object.translation
                session['correct_translation'] = new_word_object.word
        else:
            session.pop('word', None)
            session.pop('correct_translation', None)
            session.pop('correct_answers', None)
            session.pop('category_name', None)
            return render_template('endlesson.html')  # Zwrócenie odpowiedzi

        return render_template('lesson.html', word=session['word'], message=message, category_name=category_name, review_message=review_message)

    # ostateczny render
    return render_template('lesson.html', word=word, message=message, category_name=category_name, review_message=review_message)

