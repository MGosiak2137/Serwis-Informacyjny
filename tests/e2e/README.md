# Testy E2E (End-to-End)

Testy end-to-end używające Selenium do testowania aplikacji w przeglądarce.

## Wymagania

1. **Selenium** - już w `requirements.txt`
2. **ChromeDriver** - należy zainstalować zgodnie z wersją Chrome
3. **Uruchomiona aplikacja Flask** - przed uruchomieniem testów

## Instalacja

### 1. Zainstaluj zależności:
```bash
python -m pip install -r requirements.txt
```

### 2. Zainstaluj ChromeDriver:
- Pobierz ChromeDriver z https://chromedriver.chromium.org/
- Dodaj do PATH lub umieść w folderze projektu

## Uruchamianie testów

### 1. Uruchom aplikację Flask w jednym terminalu:
```bash
python app.py
```
Aplikacja powinna działać na `http://localhost:5000`

### 2. W drugim terminalu uruchom testy e2e:

**WAŻNE:** Na Windows używaj `python -m pytest` zamiast `pytest`:

```bash
# Wszystkie testy e2e
python -m pytest tests/e2e/

# Tylko testy strony głównej
python -m pytest tests/e2e/test_homepage.py

# Tylko testy logowania
python -m pytest tests/e2e/test_login.py

# Tylko testy horoskopu
python -m pytest tests/e2e/test_horoscope.py

# Z wizualizacją (bez headless) - zmień w plikach testowych
python -m pytest tests/e2e/ -v
```

## Tryb headless vs. wizualny

Domyślnie testy uruchamiają się w trybie headless (bez okna przeglądarki).
Aby zobaczyć przeglądarkę podczas testów, zmień w plikach testowych:

```python
chrome_options.add_argument("--headless")  # Usuń tę linię
```

## Struktura testów

- `test_homepage.py` - testy strony głównej
- `test_login.py` - testy logowania
- `test_horoscope.py` - testy horoskopu (wymaga zalogowania)

## Uwagi

- Testy e2e są wolniejsze niż testy jednostkowe/integracyjne
- Wymagają uruchomionej aplikacji
- Mogą być niestabilne w zależności od szybkości sieci/komputera
- Używają rzeczywistej bazy danych (jeśli nie używasz testowej konfiguracji)

