# ustawiamy bazowy obraz
FROM python:3.9-slim-buster

# ustawiamy katalog roboczy na /app
WORKDIR /app

# kopiujemy plik zależności do katalogu /app
COPY requirements.txt .

# instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# kopiujemy pliki aplikacji do katalogu /app
COPY backend.py .

# ustawiamy zmienną środowiskową FLASK_APP
ENV FLASK_APP=backend.py
ENV DATABASE_LINK=mongodb://szymon:dxFxazbvuV5GkuHW@127.0.0.1:27017/?authMechanism=DEFAULT
# eksponujemy port 5000
EXPOSE 3000

# uruchamiamy aplikację przy starcie kontenera
CMD ["flask", "run", "--host=0.0.0.0"]