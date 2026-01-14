# Serwis Informacyjny NEWC

**Serwis Informacyjny** to aplikacja webowa (Flask) służąca jako strona informacji z różnych dziedzin: pogody, ekonomii, wiadomości oraz kalendarza. Aplikacja umożliwia użytkownikom dostęp do aktualnych informacji w jednym miejscu.

## Opis (1–3 zdania)

Aplikacja jest przeznaczona dla użytkowników chcących mieć dostęp do aktualnych informacji w jednym miejscu. Rozwiązuje problem rozproszenia informacji z wielu źródeł, oferując kompleksowy serwis informacyjny zawierający dane pogodowe, kursy walut, wiadomości oraz funkcjonalności kalendarzowe. Aplikacja wymaga rejestracji i logowania, aby zapewnić personalizację doświadczenia użytkownika.

---

## Spis treści

- [Szybki start](#szybki-start)
- [Technologie](#technologie)
- [Moduły systemu](#moduły-systemu)
- [Dokumentacja (szczegóły)](#dokumentacja-szczegóły)
- [API (skrót)](#api-skrót)
- [Testowanie (skrót)](#testowanie-skrót)
- [Deployment](#deployment)
- [Proces i zasady pracy](#proces-i-zasady-pracy)
- [Autorzy i zespoły](#autorzy-i-zespoły)

---

## Szybki start

**Cel:** uruchomić aplikację lokalnie.

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/MGosiak2137/Serwis-Informacyjny.git
   cd Serwis-Informacyjny
   ```

2. Utwórz środowisko wirtualne i aktywuj:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```

4. Skonfiguruj zmienne środowiskowe:
   - utwórz plik `.env` na podstawie `.env.example` w katalogu `env/`
   - szczegóły w: [`docs/setup.md`](docs/setup.md)

5. Utwórz bazę danych:
   ```bash
   python create_db.py
   ```

6. Uruchom aplikację:
   ```bash
   python app.py
   ```
   lub
   ```bash
   flask --app app run
   ```

7. Otwórz w przeglądarce:
   - `http://127.0.0.1:5000/`

---

## Widoki aplikacji

### Strona główna
![Strona główna](docs/assets/screenshots/home.png)

Strona główna aplikacji prezentuje karty nawigacyjne do poszczególnych modułów (pogoda, ekonomia, wiadomości, kalendarz). Wyświetla również podglądy danych: aktualną datę, imieniny, numerację dnia roku, informację o świętach, kursy walut (EUR, USD, złoto) oraz najnowsze wiadomości. Dla zalogowanych użytkowników dostępne są dodatkowe opcje zarządzania kontem oraz otworzenie poszczególnych modułów.

### Moduł kalendarza (horoskop)
![Kalendarz](docs/assets/screenshots/calendar.png)

Moduł kalendarza umożliwia przeglądanie tygodniowych horoskopów dla wszystkich znaków zodiaku. Użytkownik może wybrać swój znak zodiaku i zobaczyć prognozę astrologiczną na najbliższy tydzień. Horoskopy są tłumaczone na język polski za pomocą Google Translate API.

### Moduł logowania
![Logowanie](docs/assets/screenshots/auth.png)

Moduł logowania umożliwia użytkownikom rejestrację nowego konta oraz logowanie do istniejącego konta. Po zalogowaniu użytkownik ma dostęp do funkcjonalności wymagających autoryzacji, takich jak horoskopy, preferencje ekonomiczne oraz zarządzanie kontem.

### Moduł pogodowy
![Pogoda](docs/assets/screenshots/weather.png)

Moduł pogodowy dostarcza aktualne informacje o pogodzie oraz prognozy. Umożliwia wyszukiwanie pogody dla różnych miast, wyświetlanie bieżących warunków atmosferycznych (temperatura, opis, ikona), prognozy 3-dniowej oraz interaktywną mapę z warstwami pokazującymi temperaturę, opady, zachmurzenie i wiatr. Dla zalogowanych użytkowników dostępna jest historia wyszukiwań oraz ostrzeżenia pogodowe. Moduł wykorzystuje OpenWeatherMap API.

### Moduł ekonomiczny
![Ekonomia](docs/assets/screenshots/economy.png)

Moduł ekonomiczny oferuje kompleksowe narzędzia do śledzenia danych finansowych. Umożliwia przeglądanie aktualnych kursów walut (EUR, USD, GBP i innych), indeksów giełdowych oraz akcji z różnych rynków (polskie, amerykańskie, europejskie, azjatyckie). Zawiera funkcjonalność wyszukiwania i estymacji kosztów podróży, w tym lotów oraz hoteli. Zalogowani użytkownicy mogą zarządzać preferencjami ekonomicznymi, dodawać ulubione instrumenty finansowe oraz grupować je w zakładki. Moduł integruje się z FreeCurrencyAPI, yfinance, Priceline oraz Booking.com.

### Moduł wiadomości
![Wiadomości](docs/assets/screenshots/news.png)

Moduł wiadomości agreguje najnowsze informacje z różnych kategorii. Prezentuje wiadomości sportowe z Polski (Ekstraklasa, reprezentacja, żużel) oraz wiadomości kryminalne z Krakowa (napady, zatrzymania, komunikaty policji). Użytkownicy mogą przeglądać listy artykułów, czytać szczegóły oraz korzystać z wyszukiwarki. Dla zalogowanych użytkowników dostępne są zakładki (bookmarks) oraz historia przeglądania artykułów. Wiadomości są wyświetlane również w formie karuzeli na stronie głównej aplikacji.
---

## Technologie

- **Python 3.9+** – język programowania backendu
- **Flask** – framework webowy do budowy aplikacji
- **Flask-Login** – zarządzanie sesjami użytkowników
- **Flask-SQLAlchemy** – ORM do pracy z bazą danych
- **SQLite** – baza danych (lokalna)
- **Front-end:** HTML/CSS/JavaScript
- **Testy:** pytest (unit/integration), Playwright (E2E)
- **Hosting:** AWS **typ wdrożenia:** Amazon EC2

---

## Moduły systemu

Projekt został podzielony na moduły realizowane przez zespoły.

- **Strona główna** – agregacja skrótów / nawigacja / widoki wspólne  
  Opis w: [`docs/architecture.md`](docs/architecture.md) 

- **Moduł logowania** – rejestracja, logowanie, zarządzanie kontem użytkownika  
  Dokumentacja modułu: [`docs/architecture/auth.md`](docs/architecture/auth.md) 

- **Moduł kalendarza** – horoskopy, święta, imieniny, data  
  Dokumentacja modułu: [`docs/architecture/calendar.md`](docs/architecture/calendar.md) 

- **Moduł pogodowy** – pobieranie i prezentacja danych pogodowych  
  Dokumentacja modułu: [`docs/architecture/weather.md`](docs/architecture/weather.md) 

- **Moduł ekonomiczny** – pobieranie i prezentacja danych ekonomicznych  
  Dokumentacja modułu: [`docs/architecture/economy.md`](docs/architecture/economy.md) 

- **Moduł wiadomości** – pobieranie i prezentacja wiadomości  
  Dokumentacja modułu: [`docs/architecture/news.md`](docs/architecture/news.md) 

---

## Dokumentacja (szczegóły)

Dokumentacja została podzielona na część ogólną oraz dokumentację modułów.
Zaleca się rozpoczęcie od [`docs/architecture.md`](docs/architecture.md), a następnie przejście do dokumentów modułów.

Pełna dokumentacja techniczna znajduje się w katalogu [`docs/`](docs/).

- Specyfikacja funkcjonalna (User Stories): [`docs/specification/user_stories.md`](docs/specification/user_stories.md)
- Architektura całej aplikacji: [`docs/architecture.md`](docs/architecture.md)
- Architektura modułów:
  - [`docs/architecture/auth.md`](docs/architecture/auth.md) 
  - [`docs/architecture/calendar.md`](docs/architecture/calendar.md) 
  - [`docs/architecture/weather.md`](docs/architecture/weather.md) 
  - [`docs/architecture/economy.md`](docs/architecture/economy.md) 
  - [`docs/architecture/news.md`](docs/architecture/news.md)
- Konfiguracja i `.env`: [`docs/setup.md`](docs/setup.md)
- Referencja API: [`docs/api_reference.md`](docs/api_reference.md)
- Testowanie: [`docs/testing.md`](docs/testing.md)
- Zasady pracy i kontrybucji: [`docs/contribution.md`](docs/contribution.md)
- Prowadzenie projektu (Scrum/Jira/podział zespołów): [`docs/project_management.md`](docs/project_management.md)

---

## API (skrót)

**Uwaga:** Poniższa tabela ma charakter poglądowy.
Pełna i wiążąca specyfikacja API znajduje się w [`docs/api_reference.md`](docs/api_reference.md)

| Metoda | Endpoint | Opis | Moduł |
|------:|----------|------|------|
| GET | `/` | Strona główna | Home |
| GET | `/auth/login` | Formularz logowania | Auth |
| POST | `/auth/login` | Logowanie użytkownika | Auth |
| GET | `/auth/register` | Formularz rejestracji | Auth |
| POST | `/auth/register` | Rejestracja użytkownika | Auth |
| GET | `/auth/logout` | Wylogowanie użytkownika | Auth |
| GET | `/calendar/horoscope` | Widok horoskopów (wymaga logowania) | Calendar |
| GET | `/calendar/api/horoscope/<zodiac_sign>` | API horoskopu dla znaku | Calendar |
| GET | `/main/api/calendar` | API danych kalendarza (data, święta, imieniny) | Calendar |

---

## Testowanie (skrót)

Szczegółowy opis planu testowania: [`docs/testing.md`](docs/testing.md)

Projekt wykorzystuje testy automatyczne oraz statyczną analizę kodu:
- Python: `flake8` (PEP 8),
- JavaScript: `eslint`.

### Unit tests (pytest)
```bash
pytest tests/unit
```

### Testy integracyjne (endpointy HTML i API)
```bash
pytest tests/integration
```

### Testy akceptacyjne (Playwright)
Wymaganie: **min. 1 test akceptacyjny na każde User Story**.

```bash
pytest tests/e2e
```

Raporty z testów można wygenerować poleceniem:
```bash
pytest --html=docs/assets/reports/report.html --self-contained-html
```

---

## Znane ograniczenia

- Aplikacja wykorzystuje SQLite jako bazę danych lokalnie
- Niektóre funkcjonalności wymagają kluczy API (pogoda, ekonomia)
- Tłumaczenie horoskopów korzysta z publicznego API Google Translate 
- Brak obsługi resetowania hasła przez e-mail

---

## Deployment

Projekt jest hostowany na AWS.

- Adres środowiska (URL): https://serwisinformacyjny.eu/
- Sposób wdrożenia: Amazon EC2
- Konfiguracja: Aplikacja Flask uruchomiona na instancji EC2 z konfiguracją środowiska produkcyjnego

---

## Proces i zasady pracy

Projekt był realizowany w Scrum, z backlogiem User Stories oraz sprintami i taskami w Jira.

- Opis procesu (Scrum/Jira/podział zespołów): [`docs/project_management.md`](docs/project_management.md)
- Zasady pracy (Git workflow, PR, DoD): [`docs/contribution.md`](docs/contribution.md)

---

## Autorzy i zespoły

- Zespół A (Home&Calendar&auth): Zarzyka Igor, Górszczak Małgorzata
- Zespół B (Weather): Wójcik Marlena, Nowak Julia
- Zespół C (Economy): Więcek Julian, Pysaniuk Denis
- Zespół D (News): Król Jędrzej, Gawlikowski Michał

---

## Licencja

Do użytku dydaktycznego.
