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