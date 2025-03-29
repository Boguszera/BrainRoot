from app.models import db, Category, Word

# testy endpointów

def test_index(client):
    """test indeks"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data  # Sprawdzenie, czy zwrócono HTML

def test_manager_with_categories(client, app):
    """test wyświetlania kategorii na stronie managera"""
    with app.app_context():
        category = Category(name="Testowa Kategoria")
        db.session.add(category)
        db.session.commit()

        response = client.get("/manager")
        assert response.status_code == 200
        assert b"Testowa Kategoria" in response.data

def test_add_category(client, app):
    """test dodawania kategorii"""
    with app.app_context():
        db.session.query(Category).delete()
        db.session.commit()

        response = client.post("/add_category", data={"new_category": "Animals"}, follow_redirects=True)
        assert response.status_code == 200
        assert Category.query.filter_by(name="Animals").first() is not None

def test_add_word(client, app):
    """test dodawania słowa do kategorii"""
    with app.app_context():
        db.session.query(Word).delete()
        db.session.query(Category).delete()
        db.session.commit()

        category = Category(name="Fruits")
        db.session.add(category)
        db.session.commit()

        response = client.post("/add_word", data={
            "new_word": "Apple",
            "new_translation": "Jabłko",
            "category_id": category.id
        }, follow_redirects=True)

        assert response.status_code == 200
        saved_word = Word.query.filter_by(word="Apple").first()
        assert saved_word is not None
        assert saved_word.translation == "Jabłko"
        assert saved_word.category_id == category.id

def test_delete_word(client, app):
    """test usuwania słowa"""
    with app.app_context():
        db.session.query(Word).delete()
        db.session.query(Category).delete()
        db.session.commit()

        category = Category(name="Colors")
        db.session.add(category)
        db.session.commit()

        word = Word(word="Red", translation="Czerwony", category_id=category.id)
        db.session.add(word)
        db.session.commit()

        response = client.post("/delete_word", data={"word_id": word.id}, follow_redirects=True)

        assert response.status_code == 200
        assert db.session.get(Word, word.id) is None
