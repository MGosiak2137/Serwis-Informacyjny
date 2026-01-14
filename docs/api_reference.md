# Referencja API (`api_reference.md`)

> **Cel dokumentu**  
> Ten plik stanowi **jedno źródło prawdy o wszystkich endpointach aplikacji**  
> (zarówno HTML, jak i API JSON).  
> Jest podstawą do **testów integracyjnych** oraz formalnym **kontraktem API** dla całego projektu.

Dokument zawiera **wszystkie endpointy aplikacji** (HTML i JSON) z **kompletnymi i jednoznacznymi opisami**. Szczegóły architektury modułów znajdują się w plikach `docs/architecture/<module>.md`. Dokument umożliwia napisanie **testów integracyjnych bez zaglądania do kodu**.

---

## 1. Informacje ogólne

- **Base URL (lokalnie):** `http://localhost:5000`
- **Base URL (produkcyjnie):** `https://serwisinformacyjny.eu/`
- **Format danych (API):** JSON
- **Kodowanie:** UTF-8
- **Framework:** Flask

---

## 2. Konwencje odpowiedzi (API JSON)

Aplikacja nie stosuje jednolitego formatu odpowiedzi dla wszystkich endpointów. Każdy endpoint zwraca dane w formacie odpowiednim dla swojej funkcjonalności:

- **Sukces:** Endpointy zwracają dane bezpośrednio (np. obiekty JSON, listy) lub obiekty z polami `status`, `success`
- **Błąd:** Endpointy zwracają obiekty z polami `error` lub `status: "error"` oraz odpowiednie kody HTTP (400, 404, 500)
- **Autoryzacja:** Endpointy wymagające logowania zwracają 302 (redirect) lub 401 dla niezalogowanych użytkowników

---

## 3. Lista endpointów (skrót / spis treści)

Poniższa tabela jest **pełnym spisem endpointów aplikacji**. Każdy endpoint wymieniony tutaj jest opisany szczegółowo w dalszej części dokumentu.

| Metoda | Endpoint | Typ | Krótki opis | Moduł | Auth |
|------:|----------|-----|-------------|-------|------|
| GET | `/` | HTML | Strona główna aplikacji | Home | - |
| GET | `/main/` | HTML | Strona główna aplikacji (redirect z `/`) | Home | - |
| GET | `/main/account` | HTML | Ustawienia konta użytkownika | Home | + |
| GET | `/main/account/more-options` | HTML | Dodatkowe opcje konta | Home | + |
| GET/POST | `/main/account/change-password` | HTML | Zmiana hasła | Home | + |
| POST | `/main/account/delete` | HTML | Usunięcie konta | Home | + |
| GET | `/main/api/calendar` | JSON | Dane kalendarza (data, święta, imieniny) | Home | - |
| GET | `/main/api/exchange` | JSON | Dane ekonomiczne dla strony głównej | Home | - |
| GET/POST | `/auth/login` | HTML | Formularz logowania | Auth | - |
| GET/POST | `/auth/register` | HTML | Formularz rejestracji | Auth | - |
| GET | `/auth/logout` | HTML | Wylogowanie użytkownika | Auth | + |
| GET | `/calendar/horoscope` | HTML | Widok horoskopów | Calendar | + |
| GET | `/calendar/api/horoscope/<zodiac_sign>` | JSON | Horoskop dla znaku zodiaku | Calendar | - |
| GET | `/calendar/api/horoscope` | JSON | Lista dostępnych znaków zodiaku | Calendar | - |
| GET | `/weather/dashboard` | HTML | Panel pogodowy (wymaga logowania) | Weather | + |
| GET | `/weather/` | HTML | Panel pogodowy (alternatywna ścieżka) | Weather | + |
| GET | `/api/config` | JSON | Konfiguracja API pogodowego | Weather | - |
| GET | `/api/simple_weather` | JSON | Proste dane pogodowe dla Warszawy | Weather | - |
| GET | `/api/forecast` | JSON | Prognoza pogody 3-dniowa dla Warszawy | Weather | - |
| GET | `/api/history/<username>` | JSON | Historia wyszukiwań pogody użytkownika | Weather | + |
| GET | `/api/history_last3/<username>` | JSON | Ostatnie 3 wyszukiwania pogody | Weather | + |
| POST | `/api/history/<username>` | JSON | Dodanie miasta do historii | Weather | + |
| DELETE | `/api/history/<username>` | JSON | Usunięcie historii wyszukiwań | Weather | + |
| GET | `/main_eco/main_eco` | HTML | Strona główna modułu ekonomicznego | Economy | + |
| GET | `/main_eco/get-preferences` | JSON | Pobranie preferencji ekonomicznych | Economy | + |
| PUT | `/main_eco/update-preferences` | JSON | Aktualizacja preferencji ekonomicznych | Economy | + |
| GET | `/main_eco/api/price/<symbol>` | JSON | Aktualna cena instrumentu finansowego | Economy | - |
| GET | `/currencies/` | HTML | Strona kursów walut | Economy | - |
| GET | `/currencies/api/latest` | JSON | Aktualne kursy walut | Economy | - |
| POST | `/currencies/convert` | HTML | Konwersja walut (formularz) | Economy | - |
| GET | `/stockmarket/` | HTML | Strona indeksów giełdowych i akcji | Economy | - |
| GET | `/stockmarket/data` | JSON | Dane historyczne dla symboli | Economy | - |
| GET | `/stockmarket/ticker` | JSON | Ceny top instrumentów finansowych | Economy | - |
| GET | `/journey/` | HTML | Wyszukiwanie lotów i hoteli | Economy | - |
| GET | `/news/` | HTML | Strona główna modułu wiadomości | News | + |
| GET | `/news/crime` | HTML | Lista wiadomości kryminalnych | News | + |
| GET | `/news/sport` | HTML | Lista wiadomości sportowych | News | + |
| GET | `/news/detail/<news_id>` | HTML | Szczegóły artykułu | News | + |
| GET | `/news/search` | HTML | Formularz wyszukiwania wiadomości | News | + |
| GET | `/news/search/results` | HTML | Wyniki wyszukiwania wiadomości | News | + |
| GET | `/news/sport/scraped` | HTML | Scrapowane wiadomości sportowe | News | - |
| GET | `/news/bookmarks` | HTML | Zakładki użytkownika | News | + |
| POST | `/news/api/bookmark/add` | JSON | Dodanie artykułu do zakładek | News | + |
| POST | `/news/api/bookmark/remove` | JSON | Usunięcie artykułu z zakładek | News | + |

**Legenda:**
- **Auth:** + = wymaga logowania, - = dostępne bez logowania

---

## 4. Endpointy HTML

---

### 4.1 Moduł: Home

#### 4.1.1 GET `/` → redirect `/main/`

**Moduł:** Home  

**Opis:**  
Przekierowuje na stronę główną aplikacji (`/main/`).

**Parametry:** brak  

**Odpowiedź:**  
HTTP 302 redirect do `/main/`.

**Powiązana User Story:** US-HOME-001

---

#### 4.1.2 GET `/main/`

**Moduł:** Home  

**Opis:**  
Strona główna aplikacji wyświetlająca karty nawigacyjne do modułów (pogoda, ekonomia, wiadomości, kalendarz), podglądy danych (data, imieniny, numeracja dnia roku, święta), kursy walut (EUR, USD, złoto) oraz najnowsze wiadomości. Dla zalogowanych użytkowników dostępne są dodatkowe opcje zarządzania kontem.

**Parametry:** brak  

**Odpowiedź:**  
Renderowany widok HTML (`index.html`).

**Powiązana User Story:** US-HOME-001, US-HOME-002

---

#### 4.1.3 GET `/main/account`

**Moduł:** Home  

**Opis:**  
Strona ustawień konta użytkownika. Wyświetla opcje zarządzania kontem.

**Parametry:** brak  

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
Renderowany widok HTML (`account_settings.html`).

**Powiązana User Story:** US-AUTH-003

---

#### 4.1.4 GET `/main/account/more-options`

**Moduł:** Home  

**Opis:**  
Strona z dodatkowymi opcjami konta, w tym formularz zmiany hasła.

**Parametry:** brak  

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
Renderowany widok HTML (`account_more_options.html`).

**Powiązana User Story:** US-AUTH-003

---

#### 4.1.5 GET/POST `/main/account/change-password`

**Moduł:** Home  

**Opis:**  
Formularz zmiany hasła użytkownika. Po pomyślnej zmianie hasła użytkownik jest automatycznie wylogowywany.

**Parametry (POST):**
- `current_password` (string, wymagany) – obecne hasło
- `new_password` (string, wymagany) – nowe hasło
- `confirm_password` (string, wymagany) – potwierdzenie nowego hasła
- `from` (string, opcjonalny) – parametr wskazujący źródło żądania (`more-options`)

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
- **GET:** Renderowany widok HTML (`change_password.html` lub `account_more_options.html`)
- **POST (sukces):** HTTP 302 redirect do `/auth/login` z komunikatem sukcesu
- **POST (błąd):** Renderowany widok HTML z błędami walidacji

**Powiązana User Story:** US-AUTH-003

---

#### 4.1.6 POST `/main/account/delete`

**Moduł:** Home  

**Opis:**  
Usunięcie konta użytkownika. Po usunięciu użytkownik jest automatycznie wylogowywany.

**Parametry:** brak (używa `current_user` z sesji)

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
- **Sukces:** HTTP 302 redirect do `/auth/login` z komunikatem sukcesu
- **Błąd:** HTTP 302 redirect do `/main/account` z komunikatem błędu

**Powiązana User Story:** US-AUTH-003

---

### 4.2 Moduł: Auth

#### 4.2.1 GET/POST `/auth/login`

**Moduł:** Auth  

**Opis:**  
Formularz logowania użytkownika. Po pomyślnym zalogowaniu ustawia cookie `username` i przekierowuje na stronę główną.

**Parametry (POST):**
- `email` (string, wymagany) – adres e-mail użytkownika
- `password` (string, wymagany) – hasło użytkownika

**Autoryzacja:** Nie wymagane (dostępne dla niezalogowanych)

**Odpowiedź:**  
- **GET:** Renderowany widok HTML (`login.html`)
- **POST (sukces):** HTTP 302 redirect do `/main/` z ustawionym cookie `username`
- **POST (błąd):** Renderowany widok HTML z komunikatem błędu

**Powiązana User Story:** US-AUTH-001

---

#### 4.2.2 GET/POST `/auth/register`

**Moduł:** Auth  

**Opis:**  
Formularz rejestracji nowego użytkownika. Po pomyślnej rejestracji użytkownik jest automatycznie logowany i przekierowywany na stronę główną z flagą pokazania modala powitalnego.

**Parametry (POST):**
- `email` (string, wymagany) – adres e-mail (unikalny)
- `nickname` (string, wymagany) – pseudonim użytkownika (unikalny)
- `password` (string, wymagany) – hasło
- `confirm_password` (string, wymagany) – potwierdzenie hasła

**Autoryzacja:** Nie wymagane (dostępne dla niezalogowanych)

**Odpowiedź:**  
- **GET:** Renderowany widok HTML (`register.html`)
- **POST (sukces):** HTTP 302 redirect do `/main/` z ustawionym cookie `username` i flagą `show_welcome_modal` w sesji
- **POST (błąd):** Renderowany widok HTML z błędami walidacji

**Powiązana User Story:** US-AUTH-002

---

#### 4.2.3 GET `/auth/logout`

**Moduł:** Auth  

**Opis:**  
Wylogowanie użytkownika. Usuwa sesję użytkownika i cookie `username`, następnie przekierowuje na stronę logowania.

**Parametry:** brak

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
HTTP 302 redirect do `/auth/login` z usuniętym cookie `username`.

**Powiązana User Story:** US-AUTH-001

---

### 4.3 Moduł: Calendar

#### 4.3.1 GET `/calendar/horoscope`

**Moduł:** Calendar  

**Opis:**  
Widok horoskopów dla wszystkich znaków zodiaku. Umożliwia wybór znaku i wyświetlenie tygodniowej prognozy astrologicznej.

**Parametry:** brak

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
Renderowany widok HTML (`horoscope.html`).

**Powiązana User Story:** US-CAL-001, US-HOME-003

---

### 4.4 Moduł: Weather

#### 4.4.1 GET `/weather/dashboard` lub `/weather/`

**Moduł:** Weather  

**Opis:**  
Panel pogodowy umożliwiający wyszukiwanie pogody dla różnych miast, wyświetlanie bieżących warunków atmosferycznych, prognozy 3-dniowej oraz interaktywnej mapy z warstwami (temperatura, opady, zachmurzenie, wiatr). Dla zalogowanych użytkowników dostępna jest historia wyszukiwań oraz ostrzeżenia pogodowe.

**Parametry:** brak

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
Renderowany widok HTML (`dashboard.html`).

**Powiązana User Story:** (brak bezpośredniego powiązania w user_stories.md)

---

### 4.5 Moduł: Economy

#### 4.5.1 GET `/main_eco/main_eco`

**Moduł:** Economy  

**Opis:**  
Strona główna modułu ekonomicznego z opcjami zarządzania preferencjami użytkownika.

**Parametry:** brak

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
Renderowany widok HTML (`nav_foot_eco.html`).

**Powiązana User Story:** US-ECO-005, US-ECO-006

---

#### 4.5.2 GET `/currencies/`

**Moduł:** Economy  

**Opis:**  
Strona kursów walut wyświetlająca aktualne kursy wymiany dla różnych walut (USD, EUR, GBP, CHF, JPY, CZK, NOK, SEK, DKK, HUF, CNY, AUD, CAD) względem PLN. Zawiera również formularz konwersji walut.

**Parametry:** brak

**Autoryzacja:** Nie wymagane

**Odpowiedź:**  
Renderowany widok HTML (`currencies.html`).

**Powiązana User Story:** US-ECO-001, US-ECO-004

---

#### 4.5.3 POST `/currencies/convert`

**Moduł:** Economy  

**Opis:**  
Konwersja kwoty między walutami. Przyjmuje dane z formularza i zwraca wynik konwersji.

**Parametry (POST):**
- `amount` (float, wymagany) – kwota do konwersji
- `from_currency` (string, wymagany) – kod waluty źródłowej (np. `USD`, `EUR`)
- `to_currency` (string, wymagany) – kod waluty docelowej (np. `PLN`, `EUR`)

**Autoryzacja:** Nie wymagane

**Odpowiedź:**  
Renderowany widok HTML (`currencies.html`) z wynikiem konwersji w zmiennych `amount`, `from_currency`, `to_currency`, `converted`.

**Powiązana User Story:** US-ECO-004

---

#### 4.5.4 GET `/stockmarket/`

**Moduł:** Economy  

**Opis:**  
Strona indeksów giełdowych i akcji umożliwiająca przeglądanie danych dla różnych instrumentów finansowych (polskie, amerykańskie, europejskie, azjatyckie akcje, indeksy, surowce). Wyświetla wykresy historyczne, dane intraday oraz status otwarcia rynków.

**Parametry (query):**
- `category` (string, opcjonalny) – kategoria instrumentów (np. `Akcje - Polskie`)
- `symbols` (string, opcjonalny) – lista symboli oddzielonych przecinkami (np. `AAPL,MSFT,GOOGL`)
- `range` (string, opcjonalny) – zakres czasowy danych (`1d`, `5d`, `1mo`, `1y`), domyślnie `1mo`

**Autoryzacja:** Nie wymagane

**Odpowiedź:**  
Renderowany widok HTML (`stockmarket.html`).

**Powiązana User Story:** US-ECO-002, US-ECO-004

---

#### 4.5.5 GET `/journey/`

**Moduł:** Economy  

**Opis:**  
Strona wyszukiwania lotów i hoteli. Umożliwia wprowadzenie parametrów podróży (miasto wylotu/przylotu, daty, liczba pasażerów, klasa kabiny) i wyświetla dostępne loty oraz hotele wraz z estymacją całkowitej ceny podróży.

**Parametry (query):**
- `origin` (string, opcjonalny) – miasto/port lotniczy wylotu
- `destination` (string, opcjonalny) – miasto/port lotniczy przylotu
- `date_from` (string, opcjonalny) – data wylotu (format: `YYYY-MM-DD`)
- `date_to` (string, opcjonalny) – data powrotu (format: `YYYY-MM-DD`)
- `people` (integer, opcjonalny) – liczba pasażerów, domyślnie `1`
- `cabin` (string, opcjonalny) – klasa kabiny (`ECO`, `BUSINESS`, `FIRST`), domyślnie `ECO`

**Autoryzacja:** Nie wymagane

**Odpowiedź:**  
Renderowany widok HTML (`journey.html`) z listą lotów, hoteli oraz estymacją kosztów.

**Powiązana User Story:** US-ECO-003

---

### 4.6 Moduł: News

#### 4.6.1 GET `/news/`

**Moduł:** News  

**Opis:**  
Strona główna modułu wiadomości wyświetlająca dwa kafelki (kryminalne i sportowe) oraz 5 ostatnich wiadomości z każdej kategorii.

**Parametry:** brak

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
Renderowany widok HTML (`nav_footnews.html`).

**Powiązana User Story:** (brak bezpośredniego powiązania w user_stories.md)

---

#### 4.6.2 GET `/news/crime`

**Moduł:** News  

**Opis:**  
Lista wiadomości kryminalnych z Krakowa (napady, zatrzymania, komunikaty policji). Dla zalogowanych użytkowników wyświetla informację o zakładkach.

**Parametry:** brak

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
Renderowany widok HTML (`crime_news.html`) z listą artykułów i zestawem `bookmarked_ids`.

**Powiązana User Story:** (brak bezpośredniego powiązania w user_stories.md)

---

#### 4.6.3 GET `/news/sport`

**Moduł:** News  

**Opis:**  
Lista wiadomości sportowych z Polski (Ekstraklasa, reprezentacja, żużel). Dla zalogowanych użytkowników wyświetla informację o zakładkach.

**Parametry:** brak

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
Renderowany widok HTML (`sport_news.html`) z listą artykułów i zestawem `bookmarked_ids`.

**Powiązana User Story:** (brak bezpośredniego powiązania w user_stories.md)

---

#### 4.6.4 GET `/news/detail/<news_id>`

**Moduł:** News  

**Opis:**  
Szczegóły pojedynczego artykułu. Automatycznie zapisuje artykuł w historii przeglądania użytkownika.

**Parametry (path):**
- `news_id` (string, wymagany) – identyfikator artykułu

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
- **Sukces:** Renderowany widok HTML (`detail.html`) z danymi artykułu i flagą `is_bookmarked`
- **Błąd:** HTTP 404 (artykuł nie znaleziony) lub HTTP 500 (błąd serwera)

**Powiązana User Story:** (brak bezpośredniego powiązania w user_stories.md)

---

#### 4.6.5 GET `/news/search`

**Moduł:** News  

**Opis:**  
Formularz wyszukiwania wiadomości z opcjami filtrowania (kategoria, zakres dat, słowa kluczowe). Wyświetla również historię przeglądania użytkownika.

**Parametry:** brak

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
Renderowany widok HTML (`news_search.html`) z pustymi wynikami i historią przeglądania.

**Powiązana User Story:** (brak bezpośredniego powiązania w user_stories.md)

---

#### 4.6.6 GET `/news/search/results`

**Moduł:** News  

**Opis:**  
Wyniki wyszukiwania wiadomości z zastosowaniem filtrów (kategoria, zakres dat, słowa kluczowe w tytule).

**Parametry (query):**
- `q` (string, opcjonalny) – słowa kluczowe do wyszukania w tytule
- `scope` (string, opcjonalny) – zakres wyszukiwania (`all`, `sport`, `crime`), domyślnie `all`
- `from_date` (string, opcjonalny) – data początkowa (format: `YYYY-MM-DD`)
- `to_date` (string, opcjonalny) – data końcowa (format: `YYYY-MM-DD`)

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
Renderowany widok HTML (`news_search.html`) z wynikami wyszukiwania, historią przeglądania oraz parametrami wyszukiwania.

**Powiązana User Story:** (brak bezpośredniego powiązania w user_stories.md)

---

#### 4.6.7 GET `/news/sport/scraped`

**Moduł:** News  

**Opis:**  
Strona ze scrapowanymi wiadomościami sportowymi (przykładowe dane z pliku JSON).

**Parametry:** brak

**Autoryzacja:** Nie wymagane

**Odpowiedź:**  
Renderowany widok HTML (`sport_scraped.html`) z listą scrapowanych artykułów.

**Powiązana User Story:** (brak bezpośredniego powiązania w user_stories.md)

---

#### 4.6.8 GET `/news/bookmarks`

**Moduł:** News  

**Opis:**  
Strona z zakładkami (bookmarks) zalogowanego użytkownika. Wyświetla wszystkie zapisane artykuły.

**Parametry:** brak

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Odpowiedź:**  
Renderowany widok HTML (`bookmarks.html`) z listą zakładek użytkownika.

**Powiązana User Story:** (brak bezpośredniego powiązania w user_stories.md)

---

## 5. Endpointy API (JSON)

Każdy endpoint API jest opisany w sposób umożliwiający przygotowanie testów integracyjnych, klienta API oraz weryfikację zgodności implementacji z dokumentacją.

---

### 5.1 Moduł: Home

#### 5.1.1 GET `/main/api/calendar`

**Moduł:** Home  

**Opis:**  
Zwraca dane kalendarzowe: aktualną datę, imieniny, numerację dnia roku oraz informację o świętach.

**Parametry:** brak

**Autoryzacja:** Nie wymagane

**Przykład zapytania:**
```bash
curl "http://localhost:5000/main/api/calendar"
```

**Przykład odpowiedzi:**
```json
{
  "date": "2024-01-15",
  "day_of_year": 15,
  "name_day": "Paweł",
  "is_holiday": false
}
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** US-HOME-002

---

#### 5.1.2 GET `/main/api/exchange`

**Moduł:** Home  

**Opis:**  
Zwraca dane ekonomiczne dla strony głównej: kursy walut (EUR/PLN, USD/PLN), cenę złota oraz historie cenowe (ostatnie 30 dni dla USD/PLN i EUR/PLN, ostatnie 90 dni dla złota).

**Parametry:** brak

**Autoryzacja:** Nie wymagane

**Przykład zapytania:**
```bash
curl "http://localhost:5000/main/api/exchange"
```

**Przykład odpowiedzi:**
```json
{
  "eur_pln": 4.32,
  "usd_pln": 3.98,
  "gold_price": 2850.50,
  "gold_history": [
    {"date": "2024-01-01", "price": 2840.00},
    {"date": "2024-01-02", "price": 2845.00}
  ],
  "usd_history": [
    {"date": "2024-01-01", "rate": 3.95},
    {"date": "2024-01-02", "rate": 3.96}
  ],
  "eur_history": [
    {"date": "2024-01-01", "rate": 4.30},
    {"date": "2024-01-02", "rate": 4.31}
  ]
}
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** US-ECO-005

---

### 5.2 Moduł: Calendar

#### 5.2.1 GET `/calendar/api/horoscope/<zodiac_sign>`

**Moduł:** Calendar  

**Opis:**  
Zwraca tygodniowy horoskop dla wybranego znaku zodiaku. Horoskop jest tłumaczony na język polski za pomocą Google Translate API.

**Parametry (path):**
- `zodiac_sign` (string, wymagany) – kod znaku zodiaku (np. `aries`, `taurus`, `gemini`, `cancer`, `leo`, `virgo`, `libra`, `scorpio`, `sagittarius`, `capricorn`, `aquarius`, `pisces`)

**Autoryzacja:** Nie wymagane

**Przykład zapytania:**
```bash
curl "http://localhost:5000/calendar/api/horoscope/aries"
```

**Przykład odpowiedzi:**
```json
{
  "zodiac_sign": "aries",
  "horoscope": "Ten tydzień przyniesie Ci wiele możliwości...",
  "date_range": "2024-01-15 - 2024-01-21"
}
```

**Kody odpowiedzi:**
- `200` – OK
- `400` – niepoprawny znak zodiaku (zwraca `{"error": "Invalid zodiac sign"}`)

**Powiązana User Story:** US-CAL-001, US-HOME-003

---

#### 5.2.2 GET `/calendar/api/horoscope`

**Moduł:** Calendar  

**Opis:**  
Zwraca listę wszystkich dostępnych znaków zodiaku.

**Parametry:** brak

**Autoryzacja:** Nie wymagane

**Przykład zapytania:**
```bash
curl "http://localhost:5000/calendar/api/horoscope"
```

**Przykład odpowiedzi:**
```json
{
  "zodiac_signs": [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
  ]
}
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** US-CAL-001

---

### 5.3 Moduł: Weather

#### 5.3.1 GET `/api/config`

**Moduł:** Weather  

**Opis:**  
Zwraca konfigurację API pogodowego (klucz API i URL). Używane przez frontend do bezpośrednich zapytań do OpenWeatherMap API.

**Parametry:** brak  

**Autoryzacja:** Nie wymagane

**Przykład zapytania:**
```bash
curl "http://localhost:5000/api/config"
```

**Przykład odpowiedzi:**
```json
{
  "API_KEY": "your_openweather_api_key",
  "API_URL": "https://api.openweathermap.org/data/2.5/weather?q="
}
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** (brak bezpośredniego powiązania)

---

#### 5.3.2 GET `/api/simple_weather`

**Moduł:** Weather  

**Opis:**  
Zwraca proste dane pogodowe dla Warszawy: temperatura, opis warunków oraz ikona.

**Parametry:** brak

**Autoryzacja:** Nie wymagane

**Przykład zapytania:**
```bash
curl "http://localhost:5000/api/simple_weather"
```

**Przykład odpowiedzi:**
```json
{
  "temp": 12,
  "desc": "Pochmurnie",
  "icon": "04d"
}
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** (brak bezpośredniego powiązania)

---

#### 5.3.3 GET `/api/forecast`

**Moduł:** Weather  

**Opis:**  
Zwraca 3-dniową prognozę pogody dla Warszawy z uśrednionymi wartościami temperatury, wiatru i wilgotności oraz dominującą ikoną i opisem dla każdego dnia.

**Parametry:** brak

**Autoryzacja:** Nie wymagane

**Przykład zapytania:**
```bash
curl "http://localhost:5000/api/forecast"
```

**Przykład odpowiedzi:**
```json
[
  {
    "date": "2024-01-15",
    "temp": 10,
    "wind": 5.2,
    "humidity": 75,
    "icon": "04d",
    "desc": "Pochmurnie"
  },
  {
    "date": "2024-01-16",
    "temp": 8,
    "wind": 4.5,
    "humidity": 80,
    "icon": "10d",
    "desc": "Deszcz"
  },
  {
    "date": "2024-01-17",
    "temp": 12,
    "wind": 6.0,
    "humidity": 70,
    "icon": "01d",
    "desc": "Słonecznie"
  }
]
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** (brak bezpośredniego powiązania)

---

#### 5.3.4 GET `/api/history/<username>`

**Moduł:** Weather  

**Opis:**  
Zwraca pełną historię wyszukiwań pogody dla użytkownika.

**Parametry (path):**
- `username` (string, wymagany) – nazwa użytkownika (nickname)

**Autoryzacja:** Wymagane logowanie (użytkownik może pobrać tylko swoją historię)

**Przykład zapytania:**
```bash
curl "http://localhost:5000/api/history/john_doe"
```

**Przykład odpowiedzi:**
```json
[
  {"city": "Warsaw", "timestamp": "2024-01-15T10:30:00"},
  {"city": "Krakow", "timestamp": "2024-01-14T15:20:00"},
  {"city": "Gdansk", "timestamp": "2024-01-13T09:15:00"}
]
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** (brak bezpośredniego powiązania)

---

#### 5.3.5 GET `/api/history_last3/<username>`

**Moduł:** Weather  

**Opis:**  
Zwraca ostatnie 3 wyszukiwania pogody dla użytkownika.

**Parametry (path):**
- `username` (string, wymagany) – nazwa użytkownika (nickname)

**Autoryzacja:** Wymagane logowanie

**Przykład zapytania:**
```bash
curl "http://localhost:5000/api/history_last3/john_doe"
```

**Przykład odpowiedzi:**
```json
[
  {"city": "Warsaw", "timestamp": "2024-01-15T10:30:00"},
  {"city": "Krakow", "timestamp": "2024-01-14T15:20:00"},
  {"city": "Gdansk", "timestamp": "2024-01-13T09:15:00"}
]
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** (brak bezpośredniego powiązania)

---

#### 5.3.6 POST `/api/history/<username>`

**Moduł:** Weather  

**Opis:**  
Dodaje miasto do historii wyszukiwań użytkownika.

**Parametry (path):**
- `username` (string, wymagany) – nazwa użytkownika (nickname)

**Body (JSON):**
```json
{
  "city": "Warsaw"
}
```

**Autoryzacja:** Wymagane logowanie

**Przykład zapytania:**
```bash
curl -X POST "http://localhost:5000/api/history/john_doe" \
  -H "Content-Type: application/json" \
  -d '{"city": "Warsaw"}'
```

**Przykład odpowiedzi:**
```json
{
  "status": "ok"
}
```

**Kody odpowiedzi:**
- `200` – OK  
- `400` – brak parametru `city` w body (zwraca `{"error": "city not provided"}`)

**Powiązana User Story:** (brak bezpośredniego powiązania)

---

#### 5.3.7 DELETE `/api/history/<username>`

**Moduł:** Weather  

**Opis:**  
Usuwa całą historię wyszukiwań pogody dla użytkownika.

**Parametry (path):**
- `username` (string, wymagany) – nazwa użytkownika (nickname)

**Autoryzacja:** Wymagane logowanie

**Przykład zapytania:**
```bash
curl -X DELETE "http://localhost:5000/api/history/john_doe"
```

**Przykład odpowiedzi:**
```json
{
  "status": "ok"
}
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** (brak bezpośredniego powiązania)

---

### 5.4 Moduł: Economy

#### 5.4.1 GET `/main_eco/get-preferences`

**Moduł:** Economy  

**Opis:**  
Zwraca preferencje ekonomiczne zalogowanego użytkownika: ulubione akcje, waluty oraz historię wyszukiwań.

**Parametry:** brak

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Przykład zapytania:**
```bash
curl "http://localhost:5000/main_eco/get-preferences" \
  -H "Cookie: session=..."
```

**Przykład odpowiedzi:**
```json
{
  "favorite_actions": ["AAPL", "MSFT", "GOOGL"],
  "currencies": ["USD", "EUR", "GBP"],
  "search_history": [
    {"symbol": "AAPL", "timestamp": "2024-01-15T10:30:00"}
  ]
}
```

**Kody odpowiedzi:**
- `200` – OK
- `500` – błąd serwera (zwraca `{"error": "..."}`)

**Powiązana User Story:** US-ECO-004, US-ECO-006

---

#### 5.4.2 PUT `/main_eco/update-preferences`

**Moduł:** Economy  

**Opis:**  
Aktualizuje preferencje ekonomiczne zalogowanego użytkownika.

**Parametry:** brak

**Body (JSON):**
```json
{
  "favorite_actions": ["AAPL", "MSFT", "GOOGL"],
  "currencies": ["USD", "EUR", "GBP"],
  "search_history": [
    {"symbol": "AAPL", "timestamp": "2024-01-15T10:30:00"}
  ]
}
```

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Przykład zapytania:**
```bash
curl -X PUT "http://localhost:5000/main_eco/update-preferences" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=..." \
  -d '{
    "favorite_actions": ["AAPL", "MSFT"],
    "currencies": ["USD", "EUR"],
    "search_history": []
  }'
```

**Przykład odpowiedzi:**
```json
{
  "favorite_actions": ["AAPL", "MSFT"],
  "currencies": ["USD", "EUR"],
  "search_history": []
}
```

**Kody odpowiedzi:**  
- `200` – OK
- `500` – błąd serwera (zwraca `{"error": "..."}`)

**Powiązana User Story:** US-ECO-006

---

#### 5.4.3 GET `/main_eco/api/price/<symbol>`

**Moduł:** Economy  

**Opis:**  
Zwraca aktualną cenę i zmianę procentową dla instrumentu finansowego (akcji, indeksu, surowca).

**Parametry (path):**
- `symbol` (string, wymagany) – symbol instrumentu finansowego (np. `AAPL`, `MSFT`, `GC=F`). Może zawierać nawiasy z symbolem wewnątrz, które są automatycznie usuwane.

**Autoryzacja:** Nie wymagane

**Przykład zapytania:**
```bash
curl "http://localhost:5000/main_eco/api/price/AAPL"
```

**Przykład odpowiedzi:**
```json
{
  "price": 225.50,
  "change": 1.25,
  "currency": "USD"
}
```

**Kody odpowiedzi:**
- `200` – OK
- `404` – symbol nie znaleziony (zwraca `{"error": "Nie znaleziono symbolu"}`)
- `500` – błąd serwera (zwraca `{"error": "..."}`)

**Powiązana User Story:** US-ECO-004, US-ECO-005

---

#### 5.4.4 GET `/currencies/api/latest`

**Moduł:** Economy  

**Opis:**  
Zwraca aktualne kursy walut względem PLN dla wybranych walut (USD, EUR, GBP, CHF, JPY, CZK, NOK, SEK, DKK, HUF, CNY, AUD, CAD).

**Parametry:** brak

**Autoryzacja:** Nie wymagane

**Przykład zapytania:**
```bash
curl "http://localhost:5000/currencies/api/latest"
```

**Przykład odpowiedzi:**
```json
{
  "USD": 3.98,
  "EUR": 4.32,
  "GBP": 5.02,
  "CHF": 4.45,
  "JPY": 0.0271,
  "CZK": 0.1756,
  "NOK": 0.3756,
  "SEK": 0.3821,
  "DKK": 0.5798,
  "HUF": 0.0112,
  "CNY": 0.5523,
  "AUD": 2.6543,
  "CAD": 2.9456
}
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** US-ECO-001, US-ECO-004

---

#### 5.4.5 GET `/stockmarket/data`

**Moduł:** Economy  

**Opis:**  
Zwraca dane historyczne dla wybranych symboli instrumentów finansowych w określonym zakresie czasowym.

**Parametry (query):**
- `symbols` (string, wymagany) – lista symboli oddzielonych przecinkami (np. `AAPL,MSFT,GOOGL`)
- `range` (string, opcjonalny) – zakres czasowy (`1d`, `5d`, `1mo`, `1y`), domyślnie `1mo`

**Autoryzacja:** Nie wymagane

**Przykład zapytania:**
```bash
curl "http://localhost:5000/stockmarket/data?symbols=AAPL,MSFT&range=1mo"
```

**Przykład odpowiedzi:**
```json
{
  "range": "1mo",
  "historical": {
    "AAPL": {
      "data": [
        {"date": "2024-01-01", "close": 185.50, "high": 186.00, "low": 184.50},
        {"date": "2024-01-02", "close": 186.20, "high": 187.00, "low": 185.80}
      ],
      "min": 180.00,
      "max": 190.00
    },
    "MSFT": {
      "data": [
        {"date": "2024-01-01", "close": 375.50, "high": 376.00, "low": 374.50},
        {"date": "2024-01-02", "close": 376.20, "high": 377.00, "low": 375.80}
      ],
      "min": 370.00,
      "max": 380.00
    }
  }
}
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** US-ECO-002, US-ECO-004

---

#### 5.4.6 GET `/stockmarket/ticker`

**Moduł:** Economy  

**Opis:**  
Zwraca aktualne ceny i zmiany procentowe dla top instrumentów finansowych (S&P 500, DAX, FTSE 100, Bitcoin, Gold).

**Parametry:** brak

**Autoryzacja:** Nie wymagane

**Przykład zapytania:**
```bash
curl "http://localhost:5000/stockmarket/ticker"
```

**Przykład odpowiedzi:**
```json
[
  {
    "symbol": "^GSPC",
    "name": "S&P 500",
    "price": 4750.50,
    "rate": "+0.25%",
    "is_open": true
  },
  {
    "symbol": "^GDAXI",
    "name": "DAX",
    "price": 16500.00,
    "rate": "-0.15%",
    "is_open": true
  },
  {
    "symbol": "^FTSE",
    "name": "FTSE 100",
    "price": 7500.00,
    "rate": "+0.10%",
    "is_open": true
  },
  {
    "symbol": "BTC-USD",
    "name": "Bitcoin",
    "price": 42000.00,
    "rate": "+1.50%",
    "is_open": true
  },
  {
    "symbol": "GC=F",
    "name": "Gold",
    "price": 2050.00,
    "rate": "+0.30%",
    "is_open": true
  }
]
```

**Kody odpowiedzi:**
- `200` – OK

**Powiązana User Story:** US-ECO-002, US-ECO-004

---

### 5.5 Moduł: News

#### 5.5.1 POST `/news/api/bookmark/add`

**Moduł:** News  

**Opis:**  
Dodaje artykuł do zakładek zalogowanego użytkownika.

**Parametry:** brak

**Body (JSON):**
```json
{
  "article_id": "123",
  "article_title": "Tytuł artykułu",
  "article_category": "sport",
  "article_summary": "Podsumowanie artykułu",
  "article_source": "Źródło",
  "article_url": "https://example.com/article"
}
```

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Przykład zapytania:**
```bash
curl -X POST "http://localhost:5000/news/api/bookmark/add" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=..." \
  -d '{
    "article_id": "123",
    "article_title": "Tytuł artykułu",
    "article_category": "sport",
    "article_summary": "Podsumowanie",
    "article_source": "Źródło",
    "article_url": "https://example.com/article"
  }'
```

**Przykład odpowiedzi:**
```json
{
  "success": true
}
```

**Kody odpowiedzi:**
- `200` – OK (zwraca `{"success": true}`)
- `400` – brak `article_id` w body (zwraca `{"success": false, "error": "Brak article_id"}`)
- `500` – błąd serwera (zwraca `{"success": false, "error": "DB error"}` lub `{"success": false, "error": "Internal error"}`)

**Powiązana User Story:** (brak bezpośredniego powiązania)

---

#### 5.5.2 POST `/news/api/bookmark/remove`

**Moduł:** News  

**Opis:**  
Usuwa artykuł z zakładek zalogowanego użytkownika.

**Parametry:** brak

**Body (JSON):**
```json
{
  "article_id": "123"
}
```

**Autoryzacja:** Wymagane logowanie (`@login_required`)

**Przykład zapytania:**
```bash
curl -X POST "http://localhost:5000/news/api/bookmark/remove" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=..." \
  -d '{"article_id": "123"}'
```

**Przykład odpowiedzi:**
```json
{
  "success": true
}
```

**Kody odpowiedzi:**
- `200` – OK (zwraca `{"success": true}`)
- `400` – brak `article_id` w body (zwraca `{"success": false, "error": "Brak article_id"}`)
- `500` – błąd serwera (zwraca `{"success": false, "error": "DB error"}` lub `{"success": false, "error": "Internal error"}`)

**Powiązana User Story:** (brak bezpośredniego powiązania)

---

## 6. Uwierzytelnianie i autoryzacja

Aplikacja wykorzystuje **Flask-Login** do zarządzania sesjami użytkowników. Autoryzacja opiera się na sesjach HTTP (cookies).

### 6.1 Mechanizm autoryzacji

- **Sesje:** Użytkownik jest identyfikowany przez sesję Flask-Login przechowywaną w cookie `session`
- **Dekorator `@login_required`:** Endpointy oznaczone tym dekoratorem wymagają zalogowanego użytkownika
- **Przekierowanie:** Niezalogowani użytkownicy próbujący uzyskać dostęp do chronionych endpointów są automatycznie przekierowywani do `/auth/login`
- **Cookie `username`:** Po zalogowaniu ustawiane jest dodatkowe cookie `username` z pseudonimem użytkownika (ważność: 7 dni)

### 6.2 Endpointy wymagające autoryzacji

Następujące endpointy wymagają logowania (oznaczone `+` w tabeli w sekcji 3):

**Moduł Home:**
- `/main/account` (GET)
- `/main/account/more-options` (GET)
- `/main/account/change-password` (GET, POST)
- `/main/account/delete` (POST)

**Moduł Auth:**
- `/auth/logout` (GET)

**Moduł Calendar:**
- `/calendar/horoscope` (GET)

**Moduł Weather:**
- `/weather/dashboard` (GET)
- `/weather/` (GET)
- `/api/history/<username>` (GET, POST, DELETE)
- `/api/history_last3/<username>` (GET)

**Moduł Economy:**
- `/main_eco/main_eco` (GET)
- `/main_eco/get-preferences` (GET)
- `/main_eco/update-preferences` (PUT)

**Moduł News:**
- `/news/` (GET)
- `/news/crime` (GET)
- `/news/sport` (GET)
- `/news/detail/<news_id>` (GET)
- `/news/search` (GET)
- `/news/search/results` (GET)
- `/news/bookmarks` (GET)
- `/news/api/bookmark/add` (POST)
- `/news/api/bookmark/remove` (POST)

### 6.3 Endpointy dostępne bez autoryzacji

Wszystkie pozostałe endpointy (oznaczone `-` w tabeli w sekcji 3) są dostępne bez logowania, w tym:
- Strona główna (`/`, `/main/`)
- Rejestracja i logowanie (`/auth/login`, `/auth/register`)
- API kalendarza (`/main/api/calendar`)
- API ekonomiczne (`/main/api/exchange`, `/currencies/*`, `/stockmarket/*`, `/journey/`)
- API horoskopów (`/calendar/api/horoscope/*`)
- API pogodowe (niektóre endpointy)

---

## 7. Wymagania testowe (integracyjne)

Każdy endpoint opisany w tym pliku powinien mieć **co najmniej jeden test integracyjny** w katalogu `tests/integration/`. Testy powinny być jednoznacznie testowalne na podstawie tej dokumentacji bez konieczności zaglądania do kodu źródłowego.

### 7.1 Mapowanie endpoint → test integracyjny

**Moduł Home:**
- `/main/` → `tests/integration/main_page/test_main_endpoints.py`
- `/main/api/calendar` → `tests/integration/main_page/test_calendar_api.py`
- `/main/api/exchange` → `tests/integration/main_page/test_main_endpoints.py`

**Moduł Auth:**
- `/auth/login`, `/auth/register`, `/auth/logout` → `tests/integration/main_page/test_login.py` (lub osobny plik)

**Moduł Calendar:**
- `/calendar/api/horoscope/*` → `tests/integration/main_page/test_horoscope_endpoints.py`

**Moduł Weather:**
- `/api/config`, `/api/simple_weather`, `/api/forecast` → `tests/integration/weather/test_weather_routes.py`
- `/api/history/*` → `tests/integration/weather/test_history_routes.py`

**Moduł Economy:**
- `/currencies/*`, `/stockmarket/*`, `/journey/` → `tests/integration/exchange/test_*.py`
- `/main_eco/*` → `tests/integration/exchange/test_eco_preferences.py`

**Moduł News:**
- `/news/*` → `tests/integration/news/test_news_routes.py`

### 7.2 Mockowanie zewnętrznych API

Testy integracyjne powinny mockować następujące zewnętrzne API:

- **OpenWeatherMap API** (moduł Weather) – mockowanie odpowiedzi JSON z danymi pogodowymi
- **FreeCurrencyAPI** (moduł Economy) – mockowanie odpowiedzi z kursami walut
- **yfinance** (moduł Economy) – mockowanie danych giełdowych
- **Priceline API** (moduł Economy) – mockowanie odpowiedzi z lotami
- **Booking.com API** (moduł Economy) – mockowanie odpowiedzi z hotelami
- **Google Translate API** (moduł Calendar, Economy) – mockowanie tłumaczeń
- **Horoscope APIs** (moduł Calendar) – mockowanie odpowiedzi z horoskopami

Przykład mockowania w pytest:
```python
import pytest
from unittest.mock import patch, Mock

@patch('requests.get')
def test_weather_api(mock_get):
    mock_get.return_value.json.return_value = {
        "main": {"temp": 12.5},
        "weather": [{"description": "Cloudy", "icon": "04d"}]
    }
    # test endpointu
```

---

## 8. Uwagi końcowe

- `api_reference.md` jest **jedynym miejscem**, gdzie opisuje się szczegóły requestów i response'ów.
- Dokumentacja modułów (`docs/architecture/<module>.md`) zawiera wyłącznie:
  - kontekst,
  - rolę endpointów,
  - powiązanie z User Stories.
- Zmiana w API **wymaga aktualizacji tego pliku**.
- Wszystkie przykłady odpowiedzi w tym dokumencie są przykładowe i mogą różnić się od rzeczywistych odpowiedzi API w zależności od danych.
- Endpointy mogą zwracać dodatkowe pola w odpowiedziach JSON, które nie są wymienione w dokumentacji (np. pola debugowe).

---
