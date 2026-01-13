# Konfiguracja projektu i środowiska (`setup.md`)

Ten dokument opisuje wymagania systemowe, proces instalacji oraz konfigurację zmiennych środowiskowych dla aplikacji Serwis Informacyjny.

---

## 1. Wymagania systemowe

- **Python:** 3.9 lub nowszy
- **Node.js:** 18.0 lub nowszy (wymagane dla Playwright w testach E2E)
- **System operacyjny:** Windows 10+, Linux, macOS
- **Git:** do klonowania repozytorium

---

## 2. Instalacja lokalna

### 2.1 Klonowanie repozytorium

```bash
git clone https://github.com/MGosiak2137/Serwis-Informacyjny.git
cd Serwis-Informacyjny
```

### 2.2 Tworzenie środowiska wirtualnego

```bash
python -m venv .venv
```

**Aktywacja środowiska:**
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
- **Linux/macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 2.3 Instalacja zależności Python

```bash
pip install -r requirements.txt
```

### 2.4 Instalacja zależności Node.js (dla testów E2E)

```bash
npm install
```

Następnie zainstaluj przeglądarki dla Playwright:

```bash
npx playwright install
```

### 2.5 Konfiguracja zmiennych środowiskowych

Utwórz plik `.env` w katalogu `env/` na podstawie przykładu poniżej (sekcja 3.2).

### 2.6 Utworzenie bazy danych

```bash
python create_db.py
```

### 2.7 Uruchomienie aplikacji

```bash
python app.py
```

lub

```bash
flask --app app run
```

Aplikacja będzie dostępna pod adresem: `http://127.0.0.1:5000/`

---

## 3. Plik `.env`

Plik `.env` zawiera **sekrety i konfigurację środowiskową** i **nie może być commitowany do repozytorium**. Plik powinien znajdować się w katalogu `env/.env`.

### 3.1 Wymagane zmienne środowiskowe

| Zmienna | Przykład | Opis | Wymagana |
|---|---|---|---|
| `SECRET_KEY` | `your-secret-key-here` | Klucz sesji Flask używany do szyfrowania cookies i sesji. Powinien być długim, losowym stringiem. | TAK |
| `OPENWEATHER_API_KEY` | `abc123def456...` | Klucz API do OpenWeatherMap API (moduł Weather). Można uzyskać na: https://openweathermap.org/api | TAK |
| `CURRENCY_API_KEY` | `abc123def456...` | Klucz API do FreeCurrencyAPI (moduł Economy). Można uzyskać na: https://freecurrencyapi.com/ | TAK |
| `RAPIDAPI_KEY` | `abc123def456...` | Klucz API do RapidAPI używany dla Priceline i Booking.com (moduł Economy - wyszukiwanie lotów i hoteli). Można uzyskać na: https://rapidapi.com/ | TAK |
| `RAPIDAPI_HOST_PRICELINE` | `priceline-com2.p.rapidapi.com` | Host RapidAPI dla Priceline API (wyszukiwanie lotów). | TAK |
| `RAPIDAPI_HOST_BOOKING` | `booking-com.p.rapidapi.com` | Host RapidAPI dla Booking.com API (wyszukiwanie hoteli). | TAK |

### 3.2 Opcjonalne zmienne środowiskowe

| Zmienna | Przykład | Opis | Wymagana |
|---|---|---|---|
| `NEWS_DB_PATH` | `serwis_info/modules/news/news.db` | Ścieżka do bazy danych SQLite dla modułu News. Jeśli nie podano, używa domyślnej ścieżki: `serwis_info/modules/news/news.db` | NIE |

### 3.3 Przykładowy plik `.env`

Utwórz plik `env/.env` z następującą zawartością:

```env
# Sekrety aplikacji
SECRET_KEY=your-secret-key-here-generate-a-long-random-string

# API Keys - OpenWeatherMap
OPENWEATHER_API_KEY=your_openweather_api_key_here

# API Keys - FreeCurrencyAPI
CURRENCY_API_KEY=your_freecurrency_api_key_here

# API Keys - RapidAPI (Priceline i Booking.com)
RAPIDAPI_KEY=your_rapidapi_key_here
RAPIDAPI_HOST_PRICELINE=priceline-com2.p.rapidapi.com
RAPIDAPI_HOST_BOOKING=booking-com.p.rapidapi.com

# Opcjonalne - ścieżka do bazy danych News
# NEWS_DB_PATH=serwis_info/modules/news/news.db
```

### 3.4 Generowanie SECRET_KEY

Możesz wygenerować bezpieczny `SECRET_KEY` używając Pythona:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

lub

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 4. `.env.example`

Projekt powinien zawierać plik `env/.env.example` jako wzorzec konfiguracji **bez sekretów**.

**Przykładowy plik `.env.example`:**

```env
# Sekrety aplikacji
SECRET_KEY=your-secret-key-here-generate-a-long-random-string

# API Keys - OpenWeatherMap
OPENWEATHER_API_KEY=your_openweather_api_key_here

# API Keys - FreeCurrencyAPI
CURRENCY_API_KEY=your_freecurrency_api_key_here

# API Keys - RapidAPI (Priceline i Booking.com)
RAPIDAPI_KEY=your_rapidapi_key_here
RAPIDAPI_HOST_PRICELINE=priceline-com2.p.rapidapi.com
RAPIDAPI_HOST_BOOKING=booking-com.p.rapidapi.com

# Opcjonalne - ścieżka do bazy danych News
# NEWS_DB_PATH=serwis_info/modules/news/news.db
```

**Wymagania:**
- Plik `.env.example` **nie zawiera sekretów** (tylko przykładowe wartości)
- Wszystkie wymagane zmienne są opisane
- Plik może być bezpiecznie commitowany do repozytorium

---

## 5. Konfiguracja środowisk (dev / test / prod)

### 5.1 Środowisko deweloperskie (dev)

- **Plik `.env`:** `env/.env` (lokalny)
- **Baza danych:** SQLite (`database.db`, `news.db`, `users.db`)
- **Debug mode:** `True` (w `app.py`)
- **Logowanie:** Wyświetlane w konsoli

### 5.2 Środowisko testowe (test)

- **Plik `.env`:** `env/.env.test` (lub zmienne środowiskowe w CI/CD)
- **Baza danych:** SQLite w pamięci (`:memory:`) dla testów
- **Debug mode:** `False`
- **Konfiguracja:** `TestingConfig` z `config.py`
- **CSRF:** Wyłączony dla testów (`WTF_CSRF_ENABLED = False`)

### 5.3 Środowisko produkcyjne (prod)

- **Plik `.env`:** Zmienne środowiskowe ustawione na serwerze (Amazon EC2)
- **Baza danych:** PostgreSQL (planowane) lub SQLite
- **Debug mode:** `False`
- **URL:** `https://serwisinformacyjny.eu/`
- **Hosting:** Amazon EC2

**Różnice:**
- W produkcji wszystkie klucze API muszą być ustawione
- `SECRET_KEY` musi być silnym, losowym stringiem
- Debug mode musi być wyłączony
- Logi powinny być przekierowane do pliku lub systemu zarządzania logami

---

## 6. Typowe problemy

### 6.1 Brak zmiennych `.env`

**Problem:** Aplikacja nie uruchamia się lub wyświetla błędy związane z brakującymi zmiennymi.

**Rozwiązanie:**
- Upewnij się, że plik `env/.env` istnieje
- Sprawdź, czy wszystkie wymagane zmienne są ustawione
- Zweryfikuj, czy ścieżka do pliku `.env` jest poprawna (powinien być w `env/.env`)

### 6.2 Zajęty port 5000

**Problem:** Błąd `Address already in use` przy uruchomieniu aplikacji.

**Rozwiązanie:**
- Zmień port w `app.py`: `app.run(debug=True, port=5001)`
- Lub zatrzymaj proces używający portu 5000

### 6.3 Brak kluczy API

**Problem:** Moduły (Weather, Economy) nie działają lub wyświetlają błędy.

**Rozwiązanie:**
- Uzyskaj klucze API z odpowiednich serwisów:
  - OpenWeatherMap: https://openweathermap.org/api
  - FreeCurrencyAPI: https://freecurrencyapi.com/
  - RapidAPI: https://rapidapi.com/
- Dodaj klucze do pliku `env/.env`
- Uruchom ponownie aplikację

### 6.4 Błąd importu modułów

**Problem:** `ModuleNotFoundError` lub `ImportError` przy uruchomieniu.

**Rozwiązanie:**
- Upewnij się, że środowisko wirtualne jest aktywne
- Zainstaluj wszystkie zależności: `pip install -r requirements.txt`
- Sprawdź, czy jesteś w katalogu głównym projektu

### 6.5 Błąd bazy danych

**Problem:** Błędy związane z bazą danych przy uruchomieniu.

**Rozwiązanie:**
- Uruchom `python create_db.py` aby utworzyć bazę danych
- Sprawdź uprawnienia do zapisu w katalogu projektu
- Dla modułu News: sprawdź, czy ścieżka `NEWS_DB_PATH` jest poprawna

### 6.6 Playwright nie działa (testy E2E)

**Problem:** Testy E2E nie uruchamiają się lub przeglądarki nie są zainstalowane.

**Rozwiązanie:**
- Zainstaluj Node.js: `npm install`
- Zainstaluj przeglądarki: `npx playwright install`
- Upewnij się, że Node.js jest w wersji 18.0 lub nowszej

---

## 7. Struktura katalogów związana z konfiguracją

```
.
├── env/
│   └── .env                    # Plik z sekretami 
├── config.py                   # Konfiguracja Flask
├── app.py                      # Punkt wejścia aplikacji
├── create_db.py                # Skrypt tworzący bazę danych
├── requirements.txt            # Zależności Python
├── package.json                # Zależności Node.js
└── database.db                 # Główna baza danych SQLite (tworzona automatycznie)
```

---

## 8. Bezpieczeństwo

**Ważne zasady:**
- **NIGDY nie commituj** pliku `env/.env` do repozytorium
- Plik `.env` powinien być dodany do `.gitignore`
- Używaj silnych, losowych wartości dla `SECRET_KEY`
- Nie udostępniaj kluczy API publicznie
- W produkcji używaj zmiennych środowiskowych ustawionych na serwerze zamiast pliku `.env`

---
