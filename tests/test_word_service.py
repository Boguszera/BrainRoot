from app.models import db, Word, Category
from app.word_service import get_random_word, good_answer, clean_text

def test_get_random_word(app):
    """Test losowania słowa z kategorii"""
    with app.app_context():
        db.session.query(Word).delete()
        db.session.query(Category).delete()
        db.session.commit()

        category = Category(name="Animals")
        db.session.add(category)
        db.session.commit()

        word = Word(word="Dog", translation="Pies", category_id=category.id)
        db.session.add(word)
        db.session.commit()

        random_word = get_random_word("Animals")
        assert random_word is not None
        assert random_word.word == "Dog"
        assert random_word.translation == "Pies"

def test_good_answer(app):
    """test zwiększania poziomu znajomości słowa po dobrej odpowiedzi"""
    with app.app_context():
        db.session.query(Word).delete()
        db.session.query(Category).delete()
        db.session.commit()

        category = Category(name="Drinks")
        db.session.add(category)
        db.session.commit()

        word = Word(word="Water", translation="Woda", category_id=category.id, knowledge_level=1)
        db.session.add(word)
        db.session.commit()

        good_answer("Water")

        updated_word = Word.query.filter_by(word="Water").first()
        assert updated_word is not None
        assert updated_word.knowledge_level == 2

def test_clean_text():
    """test formatowania tekstu"""
    assert clean_text(" Kot  ") == "kot"
    assert clean_text("DOG!") == "dog"
    assert clean_text("  ŁĄka!!! ") == "łąka"
