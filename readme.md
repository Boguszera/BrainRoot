# BrainRoot
Interaktywna platforma edukacyjna

![CI](https://img.shields.io/github/workflow/status/boguszera/brainroot/Test-and-Deploy?label=CI)
![Tests](https://img.shields.io/github/workflow/status/boguszera/brainroot/Test?label=Tests)

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
│   ├── scripts/                   # Skrypty pomocnicze
│   │   ├── seed.py                # Skrypt dodający presety do bazy danych
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
├── docker-compose.yml             # Plik konfiguracyjny dla Docker Compose
├── LICENSE                        # Licencja projektu
├── README.md                      # Dokumentacja projektu (ten plik)
├── tests/                         # Katalog z testami aplikacji
│   ├── __init__.py                # Inicjalizacja testów
│   ├── test_routes.py             # Testy tras aplikacji
│   ├── test_models.py             # Testy modeli
│   └── test_config.py             # Testy konfiguracji
└── .github/                       # Katalog dla GitHub Actions CI/CD
    └── workflows/
        └── ci.yml                 # Workflow CI dla GitHub Actions

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

### Opcja 2: Instalacja z Dockerem i Docker Compose

1. **Zainstaluj Dockera i Docker Compose**:
    - **Windows**:
        1. Pobierz i zainstaluj [Docker Desktop dla Windows](https://www.docker.com/products/docker-desktop).
        2. Upewnij się, że włączona jest obsługa kontenerów WSL 2 (Windows Subsystem for Linux), ponieważ Docker Desktop wymaga tej technologii na Windowsie.
        3. Docker Compose jest zainstalowane automatycznie wraz z Docker Desktop, więc nie musisz go instalować osobno.
    
    - **Ubuntu/Debian**:
        ```bash
        sudo apt update && sudo apt install docker.io docker-compose
        ```

    - **Fedora**:
        ```bash
        sudo dnf install docker-ce docker-ce-cli containerd.io docker-compose
        ```

2. **Uruchom Dockera**:
    - **Windows**: Po zainstalowaniu Docker Desktop, uruchom aplikację Docker Desktop i upewnij się, że jest aktywna.
    - **Linux (Ubuntu/Debian/Fedora)**: Uruchom Docker przy pomocy systemd:
        ```bash
        sudo systemctl start docker
        sudo systemctl enable docker
        ```

3. **Uruchom Docker Compose**:
    W katalogu projektu, w którym znajduje się plik `docker-compose.yml`, uruchom następującą komendę:
    ```bash
    docker-compose up --build
    ```

    Ta komenda:
    - Zbuduje obraz kontenera na podstawie pliku `Dockerfile`.
    - Uruchomi kontener aplikacji i bazy danych (w tym przypadku SQLite, ale w przyszłości możesz zmienić na PostgreSQL lub inną bazę danych).
    - Mapuje port 5000 z kontenera na port 5000 lokalnie, dzięki czemu aplikacja będzie dostępna pod `http://localhost:5000`.

4. **Zatrzymanie kontenerów**:
    Aby zatrzymać kontenery, użyj komendy:
    ```bash
    docker-compose down
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


