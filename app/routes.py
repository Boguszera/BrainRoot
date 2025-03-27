# trasy odpowiedzialne za mapowanie URL i funkcje aplikacji
from unicodedata import category

from flask import render_template, request, redirect, url_for, session, flash, session
from . import db
from .models import Word, Category
from .word_service import get_random_word, good_answer, handle_review_cycle, increment_lessons, clean_text, handle_review_cycle
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from .ai_utils import generate_ai_sentence
from app.config import Config
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
    correct_answers = session.get('correct_answers', 0)
    translation_direction = session.get('translation_direction', 'ang-pl')
    word_frequency = session.get('word_frequency', 20)
    ai_mode = session.get('ai_mode', False)  # Pobieramy tryb AI z sesji

    # Obsługa zmiany trybu AI
    if request.method == 'POST' and 'ai_mode' in request.form:
        ai_mode = request.form.get('ai_mode') == 'on'  # Włączamy lub wyłączamy tryb AI
        session['ai_mode'] = ai_mode  # Zapisujemy stan w sesji

    if ai_mode and Config.AI_MODE_ENABLED:
        word, correct_translation = generate_ai_sentence(translation_direction)
    else:
        category_name = session.get('category_name')
        if not category_name:
            categories = Category.query.all()
            if not categories:
                return render_template('lesson.html', categories=[], message="Brak dostępnych kategorii.")
            if request.method == 'POST' and 'category' in request.form:
                category_name = request.form['category']
                session['category_name'] = category_name
            else:
                return render_template('lesson.html', categories=categories)

        # Pobranie lub wylosowanie nowego słowa
        if 'word' in session and 'correct_translation' in session:
            word = session['word']
            correct_translation = session['correct_translation']
        else:
            word_object = get_random_word(category_name)
            if not word_object:
                return render_template('lesson.html', message="Brak słów w bazie danych. Proszę dodać słowa.")

            word, correct_translation = (
            word_object.word, word_object.translation) if translation_direction == 'ang-pl' else (
            word_object.translation, word_object.word)
            session['word'] = word
            session['correct_translation'] = correct_translation

    review_frequency = session.get('review_frequency', 7)
    words_for_review = Word.query.filter(Word.is_progress == False,
                                         Word.lessons_since_last_review >= review_frequency).all()
    is_review = bool(words_for_review)
    review_message = "POWTÓRKA!" if is_review else None

    message = None
    if request.method == 'POST' and 'action' in request.form:
        user_translation = request.form['translation']
        if request.form['action'] == "Sprawdź odpowiedź":
            if clean_text(user_translation) == clean_text(correct_translation):
                good_answer(word)
                message = "Gratulacje! Poprawne tłumaczenie."
                correct_answers += 1
                session['correct_answers'] = correct_answers
            else:
                message = f"Zła odpowiedź :( Poprawne tłumaczenie to: {correct_translation}."
        elif request.form['action'] == "Nie wiem":
            message = f"Poprawne tłumaczenie to: {correct_translation}"

        if is_review:
            handle_review_cycle()
        increment_lessons()

        if correct_answers <= (word_frequency - 1):
            word_object = get_random_word(category_name) if not ai_mode else generate_ai_sentence(translation_direction)
            if word_object:
                word, correct_translation = (
                word_object.word, word_object.translation) if translation_direction == 'ang-pl' else (
                word_object.translation, word_object.word)
                session['word'] = word
                session['correct_translation'] = correct_translation
            else:
                return render_template('endlesson.html')
        else:
            session.clear()
            return render_template('endlesson.html')

    return render_template('lesson.html', word=word, message=message, review_message=review_message, ai_mode=ai_mode)




