# Serwis Informacyjny NEWC

**Serwis Informacyjny** to aplikacja webowa (Flask) służąca jako strona informacji z różnych dziedzin: pogody, ekonomii, wiadomości oraz kalendarza. Aplikacja umożliwia użytkownikom dostęp do aktualnych informacji w jednym miejscu.

## Opis (1–3 zdania)

Aplikacja jest przeznaczona dla użytkowników chcących mieć dostęp do aktualnych informacji w jednym miejscu. Rozwiązuje problem rozproszenia informacji z wielu źródeł, oferując kompleksowy serwis informacyjny zawierający dane pogodowe, kursy walut, wiadomości oraz funkcjonalności kalendarzowe. Aplikacja wymaga rejestracji i logowania, aby zapewnić spersonalizowanie użytkownika.

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
   git clone <TU_UZUPEŁNIĆ_ADRES_REPO>
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
   - szczegóły w: [`setup.md`](setup.md)

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
![Strona główna](assets/screenshots/home.png)

### Moduł kalendarza (horoskop)
![Kalendarz](assets/screenshots/calendar.png)

### Moduł logowania
![Logowanie](assets/screenshots/auth.png)

**(tu trzeba podopisywać)**
---

## Technologie

- **Python 3.9+** – język programowania backendu
- **Flask** – framework webowy do budowy aplikacji
- **Flask-Login** – zarządzanie sesjami użytkowników
- **Flask-SQLAlchemy** – ORM do pracy z bazą danych
- **SQLite** – baza danych (lokalna)
- **Front-end:** HTML/CSS/JavaScript
- **Testy:** pytest (unit/integration), Playwright (E2E)
- **Hosting:** AWS **(typ wdrożenia: ?????? nie wiem)**

---

## Moduły systemu

Projekt został podzielony na moduły realizowane przez zespoły.

- **Strona główna** – agregacja skrótów / nawigacja / widoki wspólne  
  Dokumentacja modułu: [`architecture/home.md`](architecture/home.md) 

- **Moduł logowania** – rejestracja, logowanie, zarządzanie kontem użytkownika  
  Dokumentacja modułu: [`architecture/auth.md`](architecture/auth.md) 

- **Moduł kalendarza** – horoskopy, święta, imieniny, data  
  Dokumentacja modułu: [`architecture/calendar.md`](architecture/calendar.md) 

- **Moduł pogodowy** – pobieranie i prezentacja danych pogodowych  
  Dokumentacja modułu: [`architecture/weather.md`](architecture/weather.md) *(w przygotowaniu)*

- **Moduł ekonomiczny** – pobieranie i prezentacja danych ekonomicznych  
  Dokumentacja modułu: [`architecture/economy.md`](architecture/economy.md) *(w przygotowaniu)*

- **Moduł wiadomości** – pobieranie i prezentacja wiadomości  
  Dokumentacja modułu: [`architecture/news.md`](architecture/news.md) *(w przygotowaniu)*

---

## Dokumentacja (szczegóły)

Dokumentacja została podzielona na część ogólną oraz dokumentację modułów.
Zaleca się rozpoczęcie od [`architecture.md`](architecture.md), a następnie przejście do dokumentów modułów.

Pełna dokumentacja techniczna znajduje się w katalogu [`./`](./).

- Specyfikacja funkcjonalna (User Stories): [`specification/user_stories.md`](specification/user_stories.md)
- Architektura całej aplikacji: [`architecture.md`](architecture.md)
- Architektura modułów:
  - [`architecture/home.md`](architecture/home.md) 
  - [`architecture/auth.md`](architecture/auth.md) 
  - [`architecture/calendar.md`](architecture/calendar.md) 
  - [`architecture/weather.md`](architecture/weather.md) *(w przygotowaniu)*
  - [`architecture/economy.md`](architecture/economy.md) *(w przygotowaniu)*
  - [`architecture/news.md`](architecture/news.md) *(w przygotowaniu)*
- Konfiguracja i `.env`: [`setup.md`](setup.md)
- Referencja API: [`api_reference.md`](api_reference.md)
- Testowanie: [`testing.md`](testing.md)
- Zasady pracy i kontrybucji: [`contribution.md`](contribution.md)
- Prowadzenie projektu (Scrum/Jira/podział zespołów): [`project_management.md`](project_management.md)

---

## API (skrót)

**Uwaga:** Poniższa tabela ma charakter poglądowy.
Pełna i wiążąca specyfikacja API znajduje się w [`api_reference.md`](api_reference.md)

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

Szczegółowy opis planu testowania: [`testing.md`](testing.md)

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

- Adres środowiska (URL): **TU_UZUPEŁNIĆ**
- Sposób wdrożenia: **?**
- Konfiguracja: **nie wiem???**

---

## Proces i zasady pracy

Projekt był realizowany w Scrum, z backlogiem User Stories oraz sprintami i taskami w Jira.

- Opis procesu (Scrum/Jira/podział zespołów): [`project_management.md`](project_management.md)
- Zasady pracy (Git workflow, PR, DoD): [`contribution.md`](contribution.md)

---

## Autorzy i zespoły

- Zespół A (Home&Calendar&auth): Zarzyka Igor, Górszczak Małgorzata
- Zespół B (Weather): Wójcik Marlena, Nowak Julia
- Zespół C (Economy): Więcek Julian, Pysaniuk Denis
- Zespół D (News): Król Jędrzej, Gawlikowski Michał

---

## Licencja

Do użytku dydaktycznego.
