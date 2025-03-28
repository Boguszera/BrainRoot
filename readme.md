# BrainRoot
Interaktywna platforma edukacyjna

## O projekcie
**BrainRoot** to aplikacja open-source stworzona w celu szybkiej i efektywnej nauki języków obcych. Aplikacja umożliwia użytkownikom naukę słówek poprzez interaktywne testy, które pomagają w zapamiętywaniu nowych terminów i ich tłumaczeniu. Dzięki prostemu interfejsowi użytkownika i systemowi śledzenia postępów, BrainRoot jest doskonałym narzędziem do codziennej nauki.

### Funkcje aplikacji:
- **Wybór słówek do nauki** – użytkownik otrzymuje losowe słówko do przetłumaczenia.
- **Sprawdzanie odpowiedzi** – aplikacja weryfikuje poprawność tłumaczenia.
- **System komunikatów** – informowanie użytkownika o poprawności jego odpowiedzi.
- **Prosta nawigacja** – przejście do kolejnych słówek i sprawdzanie wyników.
- **Zarządzanie zestawami** – użytkownicy mogą tworzyć, usuwać oraz kategoryzować własne zestawy słówek w aplikacji.

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
│   ├── scripts/                    # Skrypty pomocnicze
│   │   ├── seed.py                 # Skrypt dodający presety do bazy danych
│
├── templates/                     # Katalog z szablonami HTML
│   ├── index.html                 # Strona główna
│   ├── lesson.html                # Strona lekcji (z wyświetlanym słówkiem)
│   ├── endlesson.html             # Strona zakończonej lekcji
│   ├── settings.html              # Strona konfiguracyjna
│   ├── manager.html               # Strona zarządzania zestawami
│
├── static/                        # Katalog z plikami statycznymi (CSS, JS, obrazy)
│   ├── css/                       # Style CSS
│   └── js/                        # Skrypty JavaScript
│
├── .env.example                   # Przykładowe zmienne środowiskowe
├── .gitignore                     # Ignorowanie plików w Git
├── .dockerignore                  # Ignorowanie plików w Dockerze
├── Dockerfile                     # Plik konfiguracyjny dla Dockera
├── LICENSE                        # Licencja projektu
└── README.md                      # Dokumentacja projektu (ten plik)
```

## Technologie
- **Flask**
- **HTML/CSS**
- **SQLAlchemy**
- **SQLite**
- **Python**
- **Docker**

## Instalacja aplikacji BrainRoot

### Opcja 1: Instalacja bez Dockera

#### Windows
1. Pobierz i zainstaluj Python z [python.org](https://python.org).
2. Upewnij się, że zaznaczasz opcję **Add Python to PATH** podczas instalacji.

#### macOS
1. Użyj **Homebrew**, aby zainstalować Pythona:
    ```bash
    brew install python
    ```

2. Skonfiguruj zmienne środowiskowe.  
   Skopiuj przykładowy plik `.env.example` do `.env`:
    ```bash
    cp .env.example .env
    ```

3. Zainstaluj zależności:
    ```bash
    pip install -r requirements.txt
    ```

4. Uruchom aplikację:
    ```bash
    python3 run.py
    ```

#### Linux
1. Zainstaluj Pythona:
    ```bash
    sudo apt update && sudo apt install python3 python3-pip
    ```

2. Skonfiguruj zmienne środowiskowe:
    ```bash
    cp .env.example .env
    ```

3. Zainstaluj zależności:
    ```bash
    pip install -r requirements.txt
    ```

4. Uruchom aplikację:
    ```bash
    python3 run.py
    ```

---

### Opcja 2: Instalacja z Dockerem

1. Zainstaluj Dockera:
    - **Ubuntu/Debian**: `sudo apt update && sudo apt install docker.io`
    - **Fedora**: `sudo dnf install docker-ce docker-ce-cli containerd.io`

2. Uruchom Dockera:
    ```bash
    sudo systemctl start docker
    sudo systemctl enable docker
    ```

3. Zbuduj obraz Dockera:
    ```bash
    docker build -t brainroot-app .
    ```

4. Uruchom kontener:
    ```bash
    docker run --env-file .env -p 5000:5000 brainroot-app
    ```

Aplikacja będzie dostępna pod [http://localhost:5000](http://localhost:5000).

---

## Konfiguracja zmiennych środowiskowych

Plik `.env` zawiera ustawienia aplikacji. Przykładowy plik `.env.example`:

```ini
SECRET_KEY=my_secret_key
DATABASE_URL=sqlite:///words.db
```

## Użycie

- **Zarządzanie zestawami** – użytkownicy mogą dodawać i usuwać własne zestawy słówek oraz je kategoryzować na stronie `manager.html`.
- **Lekcje** – użytkownicy mogą rozpocząć naukę tłumaczenia słówek na stronie `lesson.html`.


