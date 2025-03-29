from app.models import db, Category, Word

# testy bazy danych

def test_create_category(app):
    """test dodawaniania nowej kategorii"""
    with app.app_context():
        db.session.query(Category).delete()

        category = Category(name="Sports")
        db.session.add(category)
        db.session.commit()

        assert Category.query.count() == 1
        saved_category = Category.query.first()
        assert saved_category.name == "Sports"

def test_create_word(app):
    """test tworzenia słowa w kategorii"""
    with app.app_context():
        db.session.query(Word).delete()
        db.session.query(Category).delete()
        db.session.commit()

        category = Category(name="Vehicles")
        db.session.add(category)
        db.session.commit()

        word = Word(word="Car", translation="Samochód", category_id=category.id)
        db.session.add(word)
        db.session.commit()

        saved_word = Word.query.first()
        assert saved_word is not None
        assert saved_word.word == "Car"
        assert saved_word.translation == "Samochód"
        assert saved_word.category_id == category.id
