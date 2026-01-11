# Testy E2E z Playwright

Testy end-to-end używające Playwright (nowocześniejsza alternatywa dla Selenium).

## Instalacja

### 1. Zainstaluj Playwright:
```bash
python -m pip install playwright pytest-playwright
```

### 2. Zainstaluj przeglądarki Playwright:
```bash
python -m playwright install chromium
```

## Uruchamianie testów

### 1. Uruchom aplikację Flask:
```bash
python app.py
```

### 2. W drugim terminalu uruchom testy:
```bash
# Wszystkie testy e2e
python -m pytest tests/e2e/ -v

# Tylko konkretny plik
python -m pytest tests/e2e/test_homepage.py -v
python -m pytest tests/e2e/test_login.py -v
python -m pytest tests/e2e/test_horoscope.py -v
python -m pytest tests/e2e/test_weather.py -v
python -m pytest tests/e2e/test_load_modules.py -v
```

## Struktura testów

- `test_homepage.py` - testy strony głównej
- `test_login.py` - testy logowania
- `test_horoscope.py` - testy horoskopu
- `test_weather.py` - testy modułu pogody (w tym dla niezalogowanych użytkowników)
- `test_load_modules.py` - testy ładowania różnych modułów i przepływu użytkownika

## Zalety Playwright vs Selenium

- **Prostsza składnia**: `page.get_by_role()` zamiast `driver.find_element(By.NAME, "email")`
- **Lepsze oczekiwania**: Automatyczne czekanie na elementy
- **Szybsze**: Lepsza wydajność
- **Więcej funkcji**: Screenshoty, nagrywanie, trace

## Uwagi

- Testy wymagają uruchomionej aplikacji Flask na `http://localhost:5000`
- Testy horoskopu wymagają zalogowanego użytkownika
- Testy pogody sprawdzają zarówno zalogowanych jak i niezalogowanych użytkowników

