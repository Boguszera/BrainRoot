# obraz pythona
FROM python:3.10-slim

# ustawienie katalog roboczy w kontenerze
WORKDIR /app

# kopia pliku requirements.txt
COPY requirements.txt .

# instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# kopia całego projektu do kontenera
COPY . .

# otworzenie protu 5000 (dla flaska)
EXPOSE 5000

# uruchomienie flaska
CMD ["flask", "run", "--host=0.0.0.0"]
