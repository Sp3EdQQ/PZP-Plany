# React + Python Selenium Scraper

Aplikacja do scrapowania strony [plany.ubb.edu.pl](https://plany.ubb.edu.pl) przy użyciu frontendu React (z Tailwind CSS) oraz backendu w Pythonie wykorzystującego Selenium.

## Funkcjonalności
- Pobieranie danych o planach zajęć z serwisu [plany.ubb.edu.pl](https://plany.ubb.edu.pl)
- Prezentacja danych w przyjaznym interfejsie użytkownika
- Backend obsługujący scrapowanie i dostarczający dane do frontendu

## Technologie
- **Frontend**: React, Tailwind CSS
- **Backend**: Python, Selenium, Flask (lub FastAPI)

## Instalacja i uruchomienie
### 1. Klonowanie repozytorium
```sh
git clone git@github.com:Inexpli/PZP-Plany.git
cd PZP-Plany
```

### 2. Backend
#### Instalacja zależności
```
cd backend
python -m venv ./venv
.\.venv\Scripts\activate
pip install -r requirements.txt
``` 
### 3. Frontend
#### Instalacja zależności
Wymagane jest posiadanie Node.js (zalecana wersja 16+).
```sh
cd frontend
npm install
```

#### Uruchomienie frontendu
```sh
npm run dev
```

### 4. Korzystanie z aplikacji
