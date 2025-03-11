# obsługa logiki związanej z zarządzaniem słówkami i sposobem ich wyświetlania

from .models import Word
from . import db
from sqlalchemy import func

def get_random_word(category_name):
    count_all = Word.query.filter_by(category=category_name).count()
    count_progress = Word.query.filter_by(category=category_name, is_progress=1).count()

    # obsługa sytuacji, kiedy w puli słów w trakcie nauki jest mniej niż 50 słów
    if count_progress < 50:
        # Wybieramy słowa, które nie są w trakcie nauki
        words_to_progress = Word.query.filter_by(category=category_name, is_progress=0).limit(50 - count_progress).all()

        for word in words_to_progress:
            word.is_progress = 1  # Ustawiamy je jako słowa w trakcie nauki
            db.session.commit()

        # Losujemy słowo, które jest w trakcie nauki (is_progress=1)
    progress_word = Word.query.filter_by(category=category_name, is_progress=1).order_by(func.random()).first()
    return progress_word

def good_answer(word):
    word_object = Word.query.filter_by(word=word).first()

    if not word_object:
        return False  # Jeśli słowo nie istnieje w bazie, zwracamy False

    try:
        if word_object.knowledge_level < 5:
            word_object.knowledge_level += 1  # Zwiększamy poziom znajomości

        if word_object.knowledge_level == 5:
            word_object.is_progress = False  # Usuwamy słowo z aktywnej nauki
            word_object.lessons_since_last_review = 0  # Przygotowujemy do powtórek

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()  # Cofamy zmiany w razie błędu
        print(f"Error updating knowledge_level for word '{word}': {e}")
        return False


def handle_review_cycle():
    # Wybiera słowa do powtórek co 7 lekcji.
    words_for_review = Word.query.filter(Word.is_progress == False, Word.lessons_since_last_review >= 7).all()

    for word in words_for_review:
        word.is_progress = True  # Przywracamy do aktywnej nauki na czas powtórki
        word.lessons_since_last_review = 0  # Resetujemy licznik powtórek

    db.session.commit()
    return words_for_review

def increment_lessons():
    # Zwiększa licznik lekcji dla słów w powtórkach.

    db.session.query(Word).filter(Word.is_progress == False).update({"lessons_since_last_review": Word.lessons_since_last_review + 1})
    db.session.commit()