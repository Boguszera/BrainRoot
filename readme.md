#BrainRoot
Interaktywna platforma edukacyjna

## O projekcie
BrainRoot to aplikacja open-source stworzona do szybkiej i efektywnej nauki

1. Struktura projektu:

FuckingFluent/
│
├── app/                           # Aplikacja backendowa
│   ├── __init__.py                # Inicjalizacja aplikacji
│   ├── config.py                  # Plik konfiguracyjny aplikacji i bazy danych
│   ├── models.py                  # Modele bazy danych
│   ├── requirements.txt           # Zależności Pythona do instalacji
│
├── src/                           # Pliki frontendowe
│   ├── index.html                 # Strona główna
│   ├── lesson.html                # Strona lekcji
│   ├── login.html                 # Strona logowania
│   ├── register.html              # Strona rejestracji
│   ├── css/                       # Style CSS
│   └── js/                        # Skrypty JavaScript
│
├── .gitignore                     # Ignorowanie plików w Git
├── LICENSE                        # Licencja projektu
└── README.md                      # Dokumentacja projektu

1. python3, pip
sudo dnf install python3
sudo dnf install python3-pip
pip install --upgrade pip

pip install -r requirements.txt
