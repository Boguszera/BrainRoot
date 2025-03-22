# trasy odpowiedzialne za mapowanie URL i funkcje aplikacji
from unicodedata import category

from flask import render_template, request, redirect, url_for, session, flash, session
from . import db
from .models import Word, Category
from .word_service import get_random_word, good_answer, handle_review_cycle, increment_lessons, clean_text, handle_review_cycle
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
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

    @app.route('/manager', methods=['GET', 'POST'])
    def manager():
        # Pobranie wszystkich kategorii
        categories = Category.query.all()

        if not categories:
            message = "Brak dostępnych kategorii."
            return render_template('manager.html', categories=[], selected_category=None, message=message)

        # Jeśli użytkownik przesyła formularz z wyborem kategorii
        if request.method == 'POST':
            category_id = request.form['category']
            selected_category = Category.query.get(category_id)
            session['selected_category_id'] = category_id
            return render_template('manager.html', selected_category=selected_category,
                                   selected_category_id=category_id, categories=categories)

        # Odczytujemy kategorię z sesji, jeśli istnieje
        selected_category_id = session.get('selected_category_id')

        if selected_category_id:
            selected_category = Category.query.get(selected_category_id)
            return render_template('manager.html', categories=categories, selected_category=selected_category)

        return render_template('manager.html', categories=categories)

    @app.route('/add_category', methods=['POST'])
    def add_category():
        new_category_name = request.form['new_category']
        new_category = Category(name=new_category_name)

        db.session.add(new_category)
        db.session.commit()

        return redirect(url_for('manager'))

    @app.route('/add_word', methods=['POST'])
    def add_word():
        new_word = request.form['new_word']
        new_translation = request.form['new_translation']
        category_id = request.form['category_id']
        selected_category = Category.query.get(category_id)

        word = Word(word=new_word, translation=new_translation, category=selected_category)

        db.session.add(word)
        db.session.commit()

        return redirect(url_for('manager', category=category_id))

    @app.route('/delete_word', methods=['POST'])
    def delete_word():
        word_id = request.form.get('word_id')  # Używamy .get, aby uniknąć KeyError

        if word_id:  # Sprawdzamy, czy word_id jest obecne
            word_to_delete = Word.query.options(joinedload(Word.category)).get(word_id)

            if word_to_delete:
                word_name = word_to_delete.word
                category_id = word_to_delete.category.id  # Zapisz id kategorii

                db.session.delete(word_to_delete)
                db.session.commit()

                del_message = f"Słowo '{word_name}' zostało usunięte."
            else:
                del_message = "Nie znaleziono słowa do usunięcia."
                category_id = None  # Jeżeli słowo nie istnieje, nie przekazujemy id kategorii
        else:
            del_message = "Nie przesłano id słowa."
            category_id = None

        # Przekazujemy kategorie i kategorię do szablonu, by pozostać w tej samej kategorii
        categories = Category.query.all()
        selected_category = Category.query.get(category_id) if category_id else None

        return render_template('manager.html', del_message=del_message,
                               selected_category=selected_category, categories=categories)

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
            return redirect(url_for('settings'))  # Przekierowanie do lekcji po zapisaniu ustawień

        return render_template('settings.html')

    # trasa /lesson
    @app.route('/lesson', methods=['GET', 'POST'])
    def lesson_route():
        return lesson()


def lesson():
    correct_answers = session.get('correct_answers', 0)  # counter poprawnych odpowiedzi (jesli istnieje w sesji pobiera, jesli nie to domyslna wartosc 0)
    category_name = session.get('category_name')
    translation_direction = session.get('translation_direction', 'ang-pl')  # domyślnie angielski na polski
    word_frequency = session.get('word_frequency', 20)

    if not category_name:
        categories = Category.query.all() # przeszukanie kolumny kategorii, wybranie unikalnych wyników i przekazanie w postaci listy krotek
        print("Kategorie w lesson():", categories)  # Logowanie do terminala
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

