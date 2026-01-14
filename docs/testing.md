# Plan testowania (`testing.md`)

> Dokument opisuje **plan testów dla aplikacji webowej** realizowanej w ramach projektu.  
> Plan testowania jest **obowiązkowy** i stanowi część dokumentacji technicznej projektu.

---

## 1. Organizacja testów

- Projekt został podzielony na **moduły**, z których każdy realizowany jest przez osobny zespół.
- **Każdy zespół odpowiada za testy swojego modułu**.
- Każdy zespół przygotowuje **jeden spójny plan testów** dla swojego modułu.
- Plan testów **musi obejmować wszystkie trzy rodzaje testów**:
  - testy jednostkowe (**Unit**),
  - testy integracyjne (**Integration**),
  - testy akceptacyjne (**E2E**).

---

## 2. Wymagania minimalne – zakres testów

### 2.1 Testy jednostkowe (Unit)

Każdy zespół:
- przygotowuje **co najmniej 2–3 testy jednostkowe** dla modułu,
- testuje:
  - funkcje pomocnicze,
  - logikę biznesową,
  - przetwarzanie danych.

**Zakres testów jednostkowych (ważne):**
- ❌ bez uruchamiania Flask,
- ❌ bez warstwy HTTP,
- ❌ bez bazy danych.

**Narzędzia:**
- `pytest`
- mockowanie zależności (jeśli potrzebne)

---

### 2.2 Testy integracyjne (Integration)

Testy integracyjne sprawdzają **poprawność działania endpointów modułu**.

Każdy zespół:
- przygotowuje testy integracyjne dla **swoich endpointów**:
  - endpointów HTML (czy widok się renderuje),
  - endpointów API (czy JSON ma poprawną strukturę).

**Wymagania:**
- użycie `client` z `pytest` (Flask test client),
- mockowanie zewnętrznych API (jeśli występują),
- sprawdzanie:
  - kodów statusu HTTP,
  - struktury odpowiedzi (HTML / JSON).

---

### 2.3 Testy akceptacyjne (E2E)

Testy E2E odwzorowują **realną ścieżkę użytkownika** w aplikacji.

Każdy zespół:
- przygotowuje **co najmniej 1 test E2E dla każdej User Story** przypisanej do modułu,
- wykorzystuje **Playwright**.

Test E2E:
- odwzorowuje realne zachowanie użytkownika,
- testuje aplikację jako całość (frontend + backend),
- korzysta z `e2e_server`.

---

## 3. Uruchamianie testów

### 3.1 Testy jednostkowe
```bash
pytest tests/unit
```

### 3.2 Testy integracyjne
```bash
pytest tests/integration
```

### 3.3 Testy akceptacyjne (E2E)
```bash
pytest tests/e2e
```

---

## 4. Zbiorcze tabele planu testów (obowiązkowe)

> **Wymaganie:** dla **każdego modułu** powinna istnieć **oddzielna tabela**.  
> Format tabeli jest zgodny ze wzorcem ze slajdu (ID / Typ / Co testujemy / Scenariusz-funkcja / Status).

**Status (zalecane oznaczenia):** ⬜ – nie wykonano, ✅ – zaliczony, ❌ – błąd

---

### 4.1 Moduł: Logowanie (Authentication)

| ID     | Typ testu    | Co testujemy                   | Scenariusz / funkcja                     | Status     |
|--------|--------------|--------------------------------|------------------------------------------|------------|
| UT-01  | Unit         | Hashowanie hasła               | User.set_password()                      |  ✅Passed  |
| UT-02  | Unit         | Poprawna weryfikacja hasła     | User.check_password()                    |  ✅Passed  |
| UT-03  | Unit         | Błędna weryfikacja hasła       | User.check_password()                    |  ✅Passed  |
| UT-04  | Unit         | Obsługa pustego hasła          | User.check_password("")                  |  ✅Passed  |
| IT-01  | Integration  | Strona główna serwisu          | GET/                                     |  ✅Passed |
| E2E-01 | E2E          | US-AUTH-001: Logowanie         | Strona logowania się ładuje              |  ✅Passed  |
| E2E-02 | E2E          | US-AUTH-001: Logowanie         | Formularz logowania ma wszystkie pola    |  ✅Passed  |
| E2E-03 | E2E          | US-AUTH-001: Logowanie         | Logowanie z niepoprawnymi danymi         |  ✅Passed  |
| E2E-04 | E2E          | US-AUTH-001: Logowanie         | Logowanie z poprawnymi danymi            |  ✅Passed  |

---

### 4.2 Moduł: Strona główna (Home)

| ID     | Typ testu    | Co testujemy                   | Scenariusz / funkcja                      | Status     |
|--------|--------------|--------------------------------|-------------------------------------------|------------|
| IT-01  | Integration  | Endpoint HTML strony głównej  | GET /main/                                |  ✅Passed   |
| IT-02  | Integration  | Endpoint API kalendarza        | GET /main/api/calendar                    |  ✅Passed   |
| IT-03  | Integration  | Struktura danych kalendarza    | GET /main/api/calendar (struktura JSON)   |  ✅Passed   |
| E2E-01 | E2E          | US-HOME-001: Strona główna     | Strona główna się ładuje                 |  ✅Passed   |
| E2E-02 | E2E          | US-HOME-001: Strona główna     | Navbar jest widoczny                     |  ✅Passed   |
| E2E-03 | E2E          | US-HOME-001: Strona główna     | Karty modułów są widoczne (4 karty)      |  ✅Passed   |
| E2E-04 | E2E          | US-HOME-001: Strona główna     | Stopka jest widoczna                     |  ✅Passed   |

---

### 4.3 Moduł: Kalendarz / Horoskop (Calendar)

| ID     | Typ testu    | Co testujemy                   | Scenariusz / funkcja                      | Status     |
|--------|--------------|--------------------------------|-------------------------------------------|------------|
| IT-01  | Integration  | Endpoint HTML horoskopu        | GET /calendar/horoscope                  |  ✅Passed   |
| IT-02  | Integration  | Endpoint API horoskopu          | GET /calendar/api/horoscope/<sign>       |  ✅Passed   |
| IT-03  | Integration  | Lista znaków zodiaku (API)      | GET /calendar/api/horoscope              |  ✅Passed   |
| E2E-01 | E2E          | US-CAL-001: Horoskop           | Strona horoskopu wymaga logowania        |  ✅Passed   |
| E2E-02 | E2E          | US-CAL-001: Horoskop           | Strona horoskopu ładuje się po zalogowaniu |  ✅Passed   |
| E2E-03 | E2E          | US-CAL-001: Horoskop           | Znaki zodiaku są widoczne                |  ✅Passed   |

---

### 4.4 Moduł: Pogoda (Weather)

| ID     | Typ testu   | Co testujemy                              | Scenariusz / funkcja                                                                                  | Status |
| ------ | ----------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------ |
| UT-01  | Unit        | Logika ostrzeżeń pogodowych               | Generowanie alertów dla niskiej / wysokiej temperatury i silnego wiatru (`test_alerts_logic.py`)      | ✅      |
| UT-02  | Unit        | Przetwarzanie danych prognozy             | Agregacja danych forecast (średnie wartości, dominująca ikona i opis) (`test_forecast_processing.py`) | ✅      |
| UT-03  | Unit        | Logika warstwy serwisowej historii        | Delegowanie operacji do repozytorium (add / fetch / clear) (`test_history_service.py`)                | ✅      |
| UT-04  | Unit        | Budowanie URL warstw mapy                 | Generowanie poprawnego adresu tile OpenWeather (`test_weather_utils.py`)                              | ✅      |
| IT-01  | Integration | Renderowanie widoku HTML                  | Wyświetlenie dashboardu pogodowego (`/weather/dashboard`) (`test_weather_html.py`)                    | ✅      |
| IT-02  | Integration | Endpoint API – konfiguracja               | Pobranie klucza API i URL (`/weather/api/config`) (`test_weather_api.py`)                             | ✅      |
| IT-03  | Integration | Endpoint API – bieżąca pogoda             | Zwracanie uproszczonych danych pogodowych (`/weather/api/simple_weather`)                             | ✅      |
| IT-04  | Integration | Endpoint API – prognoza                   | Zwracanie 3-dniowej prognozy w poprawnym formacie (`/weather/api/forecast`)                           | ✅      |
| IT-05  | Integration | Endpoint API – historia wyszukiwań        | Dodawanie, pobieranie i czyszczenie historii (`/weather/api/history/<user>`)                          | ✅      |
| E2E-01 | E2E         | User Story – podgląd pogody               | Niezalogowany użytkownik widzi pogodę Warszawy lub komunikat awaryjny (`test_US1.py`)                 | ✅      |
| E2E-02 | E2E         | User Story – wyszukiwanie miasta          | Użytkownik wyszukuje miasto i widzi szczegóły pogody (`test_US2.py`)                                  | ✅      |
| E2E-03 | E2E         | User Story – mapa pogodowa                | Użytkownik włącza warstwy pogodowe na mapie (`test_US3.py`)                                           | ✅      |
| E2E-04 | E2E         | User Story – ostrzeżenia pogodowe         | Wyświetlanie ostrzeżeń dla wyszukiwanego miasta (`test_US4.py`)                                       | ✅      |
| E2E-05 | E2E         | User Story – prognoza rozszerzona         | Kalendarz prognozy i widok godzinowy (`test_US5.py`)                                                  | ✅      |
| E2E-06 | E2E         | User Story – przywracanie stanu aplikacji | Automatyczne odtworzenie ostatnio wyszukanych miast (`test_US6.py`)                                   | ✅      |


---

### 4.5 Moduł: Ekonomia (Economy)

| ID     | Typ testu    | Co testujemy                       | Scenariusz / funkcja                              | Status     |
|--------|--------------|-----------------------------------|---------------------------------------------------|------------|
| UT-01  | Unit         | Przetwarzanie danych gieldy       | `interpolate_data()` – interpolacja danych        |  ✅Passed  |
| UT-02  | Unit         | Logika godzin otwarcia rynku      | `is_market_open_for_symbol()` – giełda US         |  ✅Passed  |
| UT-03  | Unit         | Logika godzin otwarcia rynku      | `is_market_open_for_symbol()` – crypto            |  ✅Passed  |
| UT-04  | Unit         | Logika godzin otwarcia rynku      | `is_market_open_for_symbol()` – weekend           |  ✅Passed  |
| UT-05  | Unit         | Pobieranie ceny symbolu           | `get_symbol_price()` – poprawny symbol            |  ✅Passed  |
| UT-06  | Unit         | Obsługa błędnych symboli          | `get_symbol_price()` – symbol nie istnieje        |  ✅Passed  |
| UT-07  | Unit         | Parsowanie symboli ze znakami     | `get_symbol_price()` – symbol z nawiasami        |  ✅Passed  |
| IT-01  | Integration  | Endpoint HTML kursów walut        | GET /currencies/                                  |  ✅Passed  |
| IT-02  | Integration  | Endpoint API – kursy walut        | GET /currencies/api/latest                        |  ✅Passed  |
| IT-03  | Integration  | Struktura danych kursów           | GET /currencies/api/latest (struktura JSON)       |  ✅Passed  |
| IT-04  | Integration  | Obsługa brakujących danych        | GET /currencies/api/latest (brak danych)         |  ✅Passed  |
| IT-05  | Integration  | Endpoint HTML giełdy              | GET /stockmarket/                                 |  ✅Passed  |
| IT-06  | Integration  | Endpoint API – dane intraday       | `get_intraday_data()` – funkcja zwraca dane      |  ✅Passed  |
| IT-07  | Integration  | Obsługa pustych danych            | `get_intraday_data()` – brak danych historycznych|  ✅Passed  |
| IT-08  | Integration  | Obsługa błędów API                | `get_intraday_data()` – błąd połączenia           |  ✅Passed  |
| IT-09  | Integration  | Endpoint API – cena symbolu       | GET /api/get_price/<symbol>                       |  ✅Passed  |
| IT-10  | Integration  | Obsługa symboli ze znakami        | GET /api/get_price/<symbol> (symbol z nawiasami) |  ✅Passed  |
| IT-11  | Integration  | Obsługa błędnych symboli          | GET /api/get_price/<symbol> (symbol invalidu)    |  ✅Passed  |
| IT-12  | Integration  | Strona główna modułu ekonomii     | GET /main_eco/main_eco                            |  ✅Passed  |
| IT-13  | Integration  | Pobranie preferencji użytkownika   | GET /main_eco/get_prefs (wymagane logowanie)      |  ✅Passed  |
| IT-14  | Integration  | Aktualizacja preferencji          | POST /main_eco/update_prefs (wymagane logowanie)  |  ✅Passed  |
| E2E-01 | E2E          | US-ECO-001: Kursy walut           | Zalogowany użytkownik widzi tabelę kursów        |  ✅Passed  |
| E2E-02 | E2E          | US-ECO-001: Kursy walut           | Konwersja walut – wkład danych i wynik            |  ✅Passed  |
| E2E-03 | E2E          | US-ECO-002: Giełda papierów       | Zalogowany użytkownik widzi kategorie indeksów   |  ✅Passed  |
| E2E-04 | E2E          | US-ECO-002: Giełda papierów       | Wybór symbolu i wyświetlenie historycznego wykresu|  ✅Passed  |
| E2E-05 | E2E          | US-ECO-003: Ulubione pozycje      | Użytkownik widzi listę ulubionych pozycji        |  ✅Passed  |
| E2E-06 | E2E          | US-ECO-003: Ulubione pozycje      | Przyciski usuwania ulubionych pozycji są widoczne|  ✅Passed  |
| E2E-07 | E2E          | US-ECO-004: Wyszukiwanie podróży  | Użytkownik wyszukuje podróże (loty i hotele)     |  ✅Passed  |
| E2E-08 | E2E          | US-ECO-004: Wyszukiwanie podróży  | Wyświetlenie wyników wyszukiwania (loty, hotele) |  ✅Passed  |

---

### 4.6 Moduł: Wiadomości (News)

| ID     | Typ testu   | Co testujemy                | Scenariusz / funkcja                                                                 | Status |
|--------|-------------|-----------------------------|--------------------------------------------------------------------------------------|--------|
| UT-01 | Unit        | Parsowanie / ładowanie  | articles_data_giver.load_file_data() — normalizacja artykułów z articles_*.json (id, title, content, published_at) | ✅Passed     |
| UT-02 | Unit        | Normalizacja artykułu   | articles_data_builder.normalize_article() — trim/merge content, normalize image URLs, id gen | ✅Passed     |
| UT-03 | Unit        | Bookmarks service       | bookmarks_service.add/remove/is_bookmarked() — obsługa duplikatów i walidacja danych | ✅Passed     |
| UT-04 | Unit        | History service         | history_service.record_view() / get_view_history() — zapis i pobieranie historii użytkownika | ✅Passed     |
| UT-05 | Unit        | Filtracja / wyszukiwanie| articles_data_giver.search_and_sort() — q, scope, from_date/to_date oraz sortowanie po published_at | ✅Passed     |
| UT-06 | Unit        | Saver / deduplikacja    | articles_saver.aggregate() — deduplikacja po url i dopisywanie do articles_sport.json`/articles_crime.json` | ✅Passed     |
| IT-01 | Integration | Endpoint HTML - home    | GET /news/ — render strony głównej (kafelki + ~10 najnowszych) (US-13, US-34, US-49) | ✅Passed     |
| IT-02 | Integration | Endpoint HTML - crime   | GET /news/crime — lista wiadomości kryminalnych, oznaczenie zakładek (US-32, US-41) | ✅Passed     |
| IT-03 | Integration | Endpoint HTML - sport   | GET /news/sport — lista wiadomości sportowych (US-32) | ✅Passed     |
| IT-04 | Integration | Endpoint HTML - search  | GET /news/search — formularz wyszukiwania i panel historii użytkownika (US-36, US-35) | ✅Passed     |
| IT-05 | Integration | Search results filtering| GET /news/search/results?q=...&scope=... — filtracja po zapytaniu i zakresie dat (test: zawiera "Napad") | ✅Passed     |
| IT-06 | Integration | Detail not found        | GET /news/detail/<id> — brak artykułu -> 404 (test detail_not_found) | ✅Passed     |
| IT-07 | Integration | Bookmarks page          | GET /news/bookmarks — lista zakładek zalogowanego użytkownika (US-41) | ✅Passed     |
| IT-08 | Integration | API add bookmark        | POST /news/api/bookmark/add — poprawne dodanie zakładki, walidacja article_id (tests: success / missing id) | ✅Passed     |
| IT-09 | Integration | API remove bookmark     | POST /news/api/bookmark/remove — poprawne usunięcie zakładki, walidacja article_id (tests: success / missing id) | ✅Passed     |
| E2E-01 | E2E         | User Story                  | „Użytkownik przegląda listę newsów i otwiera szczegóły artykułu”                     | ✅Passed     |
| E2E-02 | E2E         | User Story                  | „Zalogowany użytkownik dodaje i usuwa artykuł z zakładek”                            | ✅Passed     |

---

## 5. Powiązanie testów z User Stories

- Każda **User Story musi mieć co najmniej jeden test E2E**.
- Testy jednostkowe i integracyjne **wspierają** User Stories, ale nie zastępują testów akceptacyjnych.
- Numer User Story (np. `US-101`) powinien pojawiać się:
  - w nazwie testu,
  - w komentarzu w kodzie testu,
  - w tabeli planu testów (np. dopisz w kolumnie „Scenariusz / funkcja” lub w opisie testu).

---

## 6. Raport końcowy z testów (HTML)

Testy uruchamiane są przez **pytest**. Na koniec generowany jest **raport HTML**, który stanowi:

- ✅ **dowód wykonania testów**,
- ✅ część oddawanej dokumentacji projektu.

### Generowanie raportu HTML

```bash
pytest --html=report.html --self-contained-html
```

**Wymaganie:** raport HTML należy dołączyć do repozytorium w katalogu:

```
doc/assets/reports/
```

---

## 7. Statyczna analiza kodu (Linting)

Oprócz testów dynamicznych (Unit / Integration / E2E), w projekcie stosowana jest
**statyczna analiza kodu (linting)**, której celem jest poprawa jakości,
czytelności i spójności kodu źródłowego.

Statyczna analiza:
- **nie zastępuje testów**,
- nie weryfikuje logiki biznesowej,
- stanowi element kontroli jakości i **Definition of Done**.

W projekcie obowiązują dwa podstawowe narzędzia lintujące:
- **Python:** `flake8` (zgodność z PEP 8),
- **JavaScript:** `ESLint`.

---

### 7.1 Python – Flake8 (PEP 8)

W projekcie obowiązuje statyczna analiza kodu Python zgodnie z wytycznymi **PEP 8**,
realizowana z użyciem narzędzia **flake8**.

#### Wymagania
- Kod Python **nie powinien generować błędów flake8**,
- wyjątki są dopuszczalne wyłącznie w przypadkach **świadomych i uzasadnionych**.

#### Uruchamianie lokalnie
```bash
pip install flake8
flake8 .
```

Zaleca się uruchamianie flake8:
- przed wykonaniem commitów,
- przed utworzeniem Pull Requesta.

#### Wyjątki (`# noqa`)
Komentarz `# noqa` powoduje pominięcie danej linii kodu przez flake8.

Przykład:
```python
from module import *  # noqa: F403
```

Zasady:
- stosuj `# noqa` z **konkretnym kodem błędu**,
- użycie musi być **uzasadnione**,
- masowe wyciszanie błędów jest **niezalecane**.

#### Konfiguracja (`.flake8`)
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,venv
```

---

### 7.2 JavaScript – ESLint

Kod JavaScript w projekcie podlega statycznej analizie z użyciem **ESLint**.

#### Wymagania
- Kod JavaScript **nie powinien generować błędów ESLint**,
- wyjątki muszą być **świadome i uzasadnione**.

#### Uruchamianie lokalnie
```bash
npm install
npx eslint .
```

Zaleca się uruchamianie ESLint:
- przed wykonaniem commitów,
- przed utworzeniem Pull Requesta.

#### Wyjątki (`eslint-disable`)

Wyłączanie reguł dopuszczalne jest wyłącznie w uzasadnionych przypadkach.

Przykład (pojedyncza linia):
```js
// eslint-disable-next-line no-console
console.log("Debug info");
```

Przykład (cały plik):
```js
/* eslint-disable no-unused-vars */
```

Zasady:
- wyłączaj **konkretne reguły**, a nie całe narzędzie,
- unikaj wyłączania reguł globalnie bez uzasadnienia.

#### Konfiguracja (`.eslintrc`)
```json
{
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": ["eslint:recommended"],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "rules": {
    "no-console": "warn",
    "no-unused-vars": "warn"
  }
}
```

---

### 7.3 Powiązanie z Definition of Done

Statyczna analiza kodu (flake8, ESLint) jest **elementem Definition of Done**.

Kod, który:
- spełnia wymagania funkcjonalne,
- posiada testy automatyczne,
- ale narusza podstawowe zasady jakości kodu,

**nie jest uznawany za ukończony**.

---

## 8. Uwagi końcowe

- Plan testów jest **częścią Definition of Done**.
- Brak testów E2E dla User Stories oznacza **niezrealizowaną funkcjonalność**.
