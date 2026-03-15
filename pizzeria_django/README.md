# Pizzeria Django Project

Projekt aplikacji webowej w Django do zarządzania pizzerią. Umożliwia zarządzanie menu, listą klientów oraz składanie zamówień. Aplikacja zawiera również REST API do obsługi menu pizz.

## Setup i Instalacja

Postępuj zgodnie z poniższymi krokami, aby uruchomić projekt lokalnie.

### 1. Wymagania wstępne
- Python 3.x
- `pip`

### 2. Utwórz i aktywuj wirtualne środowisko
Przejdź do głównego katalogu projektu i wykonaj poniższe komendy.

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Zainstaluj zależności
Zainstaluj wymagane pakiety. Zalecane jest posiadanie pliku `requirements.txt`.
```bash
pip install Django djangorestframework
```

### 4. Uruchom migracje bazy danych
Ta komenda utworzy niezbędne tabele w bazie danych.
```bash
python3 manage.py migrate
```

### 5. Stwórz superużytkownika (admina)
Konto to będzie potrzebne do zalogowania się w panelu administracyjnym. Postępuj zgodnie z instrukcjami w terminalu, aby ustawić nazwę, email i hasło.
```bash
python3 manage.py createsuperuser
```

### 6. Uruchom serwer deweloperski
```bash
python3 manage.py runserver
```
Aplikacja będzie dostępna pod adresem `http://127.0.0.1:8000/`.

## Dostępne adresy URL
- **Menu**: http://127.0.0.1:8000/menu/
- **Panel Admina**: http://127.0.0.1:8000/admin/ (użyj danych stworzonych w kroku 5)
- **API (lista pizz)**: http://127.0.0.1:8000/api/pizzas/
