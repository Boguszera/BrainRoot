# uruchomienie aplilacji, punkt wyjscia aplikacji do uruchomienia serwera
from app import create_app

# tworzenie instancji aplikacji, ladowanie konfiguracji, inicjalizacja bazy danych
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
