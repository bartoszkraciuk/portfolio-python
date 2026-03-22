# Projekt Pizzeria

Aplikacja internetowa dla pizzerii, stworzona przy użyciu języka frameworku webowego Python (Django) oraz HTML/CSS. Projekt pozwala na przeglądanie menu pizz, dodawanie ich do koszyka oraz rejestrację użytkowników.

## 🍕 Funkcjonalności

- **Interaktywne Menu:** Przeglądanie dostępnych pizz w formie atrakcyjnych kafelków.
- **Koszyk:** Możliwość określania ilości i dodawania produktów do zamówienia.
- **Konta użytkowników:** System rejestracji i logowania dla klientów.
- **Responsywny Design:** Interfejs dostosowany zarówno do komputerów (Desktop), jak i urządzeń mobilnych (telefony i tablety, poprawnie wyświetlający się na ekranach od szerokości 375px).

## 🛠 Technologie

- **Backend:** Python 3.12
- **Frontend:** HTML5, CSS3

## 🚀 Uruchomienie projektu lokalnie

1. Sklonuj repozytorium na swój komputer.
2. Przejdź do katalogu głównego projektu:
   ```bash
   cd projekt_pizzeria
   ```
3. Aktywuj wirtualne środowisko:
   ```bash
   source venv/bin/activate
   ```
4. Zainstaluj wymagane pakiety (jeśli posiadasz plik `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```
5. Wykonaj migracje bazy danych:
   ```bash
   python manage.py migrate
   ```
6. Uruchom serwer deweloperski:
   ```bash
   python manage.py runserver
   ```
7. Otwórz przeglądarkę i przejdź pod adres `http://127.0.0.1:8000/`.

## 👤 Autor
*Bartosz Kraciuk*
