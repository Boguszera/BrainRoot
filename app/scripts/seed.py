from flask import Flask
from app.models import db, Category, Word
from app.config import Config
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


def seed_data():
    with app.app_context():
        # Sprawdzenie, czy baza już zawiera dane
        result = db.session.execute(text("SELECT COUNT(*) FROM words"))
        if result.fetchone()[0] > 0:
            print("Baza danych już zawiera dane. Seedowanie pominięte.")
            return

        # Lista danych do wstawienia
        words_data = [
            ('Long time no see!', 'Dawno się nie widzieliśmy!', 'top100 zwrotów'),
            ('What have you been up to lately?', 'Co u Ciebie słychać ostatnio?', 'top100 zwrotów'),
            ('I was just about to say the same thing.', 'Właśnie miałem to samo powiedzieć.', 'top100 zwrotów'),
            ('Speaking of which…', 'A propos tego…', 'top100 zwrotów'),
            ('That’s a good point.', 'Słuszna uwaga.', 'top100 zwrotów'),
            ('I couldn’t agree more.', 'W pełni się zgadzam.', 'top100 zwrotów'),
            ('I see what you mean, but…', 'Rozumiem, co masz na myśli, ale...', 'top100 zwrotów'),
            ('Let me put it this way…', 'Ujmę to tak…', 'top100 zwrotów'),
            ('As far as I know…', 'O ile mi wiadomo…', 'top100 zwrotów'),
            ('Correct me if I’m wrong, but…', 'Popraw mnie, jeśli się mylę, ale...', 'top100 zwrotów'),
            ('I’m not really into it.', 'Niezbyt mnie to interesuje.', 'top100 zwrotów'),
            ('It’s not my cup of tea.', 'To nie moja bajka.', 'top100 zwrotów'),
            ('I’m feeling a bit under the weather.', 'Czuję się trochę źle.', 'top100 zwrotów'),
            ('I have mixed feelings about it.', 'Mam mieszane uczucia na ten temat.', 'top100 zwrotów'),
            ('I’d rather not talk about it.', 'Wolałbym o tym nie mówić.', 'top100 zwrotów'),
            ('Could you do me a favor?', 'Czy możesz wyświadczyć mi przysługę?', 'top100 zwrotów'),
            ('Would you mind helping me?', 'Czy mógłbyś mi pomóc?', 'top100 zwrotów'),
            ('Could you clarify that for me?', 'Czy możesz mi to wyjaśnić?', 'top100 zwrotów'),
            ('Can you fill me in on this?', 'Możesz mnie w to wtajemniczyć?', 'top100 zwrotów'),
            ('I’d appreciate it if you could…', 'Byłbym wdzięczny, gdybyś mógł...', 'top100 zwrotów'),
            ('Let’s get down to business.', 'Przejdźmy do rzeczy.', 'top100 zwrotów'),
            ('What’s the agenda for today’s meeting?', 'Jaki jest plan dzisiejszego spotkania?', 'top100 zwrotów'),
            ('Let’s go over the main points.', 'Omówmy główne kwestie.', 'top100 zwrotów'),
            ('We need to wrap this up.', 'Musimy to podsumować.', 'top100 zwrotów'),
            ('Does that make sense?', 'Czy to ma sens?', 'top100 zwrotów'),
            ('Where’s the nearest public transport stop?', 'Gdzie jest najbliższy przystanek?', 'top100 zwrotów'),
            ('How long does it take to get there?', 'Ile czasu zajmuje dotarcie tam?', 'top100 zwrotów'),
            ('What’s the best way to get to…?', 'Jaki jest najlepszy sposób, by dostać się do…?', 'top100 zwrotów'),
            ('Could you recommend a good restaurant nearby?', 'Czy możesz polecić dobrą restaurację w pobliżu?',
             'top100 zwrotów'),
            ('I’d like to check out, please.', 'Chciałbym się wymeldować.', 'top100 zwrotów'),
            ('From what I gather…', 'Z tego, co rozumiem…', 'top100 zwrotów'),
            ('It’s a matter of perspective.', 'To kwestia perspektywy.', 'top100 zwrotów'),
            ('It all boils down to…', 'Sprowadza się to do...', 'top100 zwrotów'),
            ('I can see both sides of the argument.', 'Widzę obie strony argumentu.', 'top100 zwrotów'),
            ('Let’s agree to disagree.', 'Zgódźmy się, że się nie zgadzamy.', 'top100 zwrotów'),
            ('At the end of the day…', 'Koniec końców…', 'top100 zwrotów'),
            ('That’s beside the point.', 'To nie ma nic do rzeczy.', 'top100 zwrotów'),
            ('It’s not as simple as it seems.', 'To nie jest tak proste, jak się wydaje.', 'top100 zwrotów'),
            ('It’s a slippery slope.', 'To śliska sprawa.', 'top100 zwrotów'),
            ('Time will tell.', 'Czas pokaże.', 'top100 zwrotów'),
            ('It’s up to you.', 'To zależy od Ciebie.', 'top100 zwrotów'),
            ('Let me get this straight.', 'Pozwól, że to wyjaśnię.', 'top100 zwrotów'),
            ('I wouldn’t bet on it.', 'Nie postawiłbym na to.', 'top100 zwrotów'),
            ('Let’s keep in touch.', 'Bądźmy w kontakcie.', 'top100 zwrotów'),
            ('It slipped my mind.', 'Wypadło mi z głowy.', 'top100 zwrotów'),
            ('It’s out of my hands.', 'To nie zależy ode mnie.', 'top100 zwrotów'),
            ('Let’s call it a day.', 'Na dziś koniec.', 'top100 zwrotów'),
            ('I’m in the middle of something.', 'Jestem czymś zajęty.', 'top100 zwrotów'),
            ('It rings a bell.', 'Coś mi to mówi.', 'top100 zwrotów'),
            ('No hard feelings.', 'Bez urazy.', 'top100 zwrotów')
        ]

        # Dodanie kategorii do tabeli 'Category', jeśli nie istnieją
        categories = {category_name: Category.query.filter_by(name=category_name).first()
                      for _, _, category_name in words_data}

        # Jeśli kategoria nie istnieje, dodajemy ją
        for category_name in categories:
            if categories[category_name] is None:
                new_category = Category(name=category_name)
                db.session.add(new_category)
                db.session.commit()
                categories[category_name] = new_category

        # Wstawianie słów do tabeli 'words'
        for word, translation, category_name in words_data:
            category = categories[category_name]  # Przypisanie odpowiedniej kategorii
            db.session.execute(text("""
                INSERT INTO words (word, translation, category_id, knowledge_level, is_progress, times_reviewed, lessons_since_last_review) 
                VALUES (:word, :translation, :category_id, 1, 0, 0, 0)
            """), {'word': word, 'translation': translation, 'category_id': category.id})

        db.session.commit()
        print("Dane seedujące zostały dodane do bazy!")


if __name__ == "__main__":
    seed_data()
