# BrainRoot
Interaktywna platforma edukacyjna

## O projekcie
**BrainRoot** to aplikacja open-source stworzona w celu szybkiej i efektywnej nauki języków obcych. Aplikacja umożliwia użytkownikom naukę słówek poprzez interaktywne testy, które pomagają w zapamiętywaniu nowych terminów i ich tłumaczeniu. Dzięki prostemu interfejsowi użytkownika i systemowi śledzenia postępów, BrainRoot jest doskonałym narzędziem do codziennej nauki.

### Funkcje aplikacji:
- **Wybór słówek do nauki** – użytkownik otrzymuje losowe słówko do przetłumaczenia.
- **Sprawdzanie odpowiedzi** – aplikacja weryfikuje poprawność tłumaczenia.
- **System komunikatów** – informowanie użytkownika o poprawności jego odpowiedzi.
- **Prosta nawigacja** – przejście do kolejnych słówek i sprawdzanie wyników.

## Struktura projektu
```
BrainRoot/
│
├── app/                           # Aplikacja backendowa (logika aplikacji)
│   ├── __init__.py                # Inicjalizacja aplikacji
│   ├── config.py                  # Plik konfiguracyjny aplikacji i bazy danych
│   ├── models.py                  # Modele bazy danych
│   ├── requirements.txt           # Zależności Pythona do instalacji
│   ├── routes.py                  # Definicje tras (routingu)
│
├── templates/                     # Katalog z szablonami HTML
│   ├── index.html                 # Strona główna
│   ├── lesson.html                # Strona lekcji (z wyświetlanym słówkiem)
│   ├── endlesson.html             # Strona zakończonej lekcji
│
├── static/                        # Katalog z plikami statycznymi (CSS, JS, obrazy)
│   ├── css/                       # Style CSS
│   └── js/                        # Skrypty JavaScript
│
├── .gitignore                     # Ignorowanie plików w Git
├── LICENSE                        # Licencja projektu
└── README.md                      # Dokumentacja projektu (ten plik)
```
## Technologie

- **Flask** 
- **HTML/CSS** 
- **SQLAlchemy** 
- **SQLite** 
- **Python** 

## Instalacja

1. **Instalacja Pythona**:
    Jeśli jeszcze nie masz Pythona 3, zainstaluj go za pomocą poniższych komend (dla systemów opartych na Linuxie):

    ```bash
    sudo dnf install python3
    sudo dnf install python3-pip
    ```

2. **Zainstaluj zależności**:
    Przejdź do katalogu projektu i zainstaluj wymagane biblioteki Pythonowe:

    ```bash
    pip install -r requirements.txt
    ```

3. **Uruchomienie aplikacji**:
    Aby uruchomić aplikację, użyj poniższej komendy:

    ```bash
    python3 run.py
    ```

    Po uruchomieniu aplikacji, możesz otworzyć przeglądarkę i przejść pod adres: `http://127.0.0.1:5000/lesson`.

## Użycie

- **Lekcje** – użytkownicy mogą rozpocząć naukę tłumaczenia słówek na stronie `lesson.html`.

### Dodatkowe informacje
- Jeśli chcesz dodać nowe słówka do bazy danych, możesz edytować odpowiednią tabelę w bazie danych SQLite.
- Możliwość rozbudowy aplikacji o dodatkowe języki oraz tryby nauki.

