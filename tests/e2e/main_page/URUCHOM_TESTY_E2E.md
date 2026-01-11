# Jak uruchomić testy E2E - Krok po kroku

## Krok 1: Zainstaluj zależności (jeśli jeszcze nie)

```bash
python -m pip install -r requirements.txt
```

## Krok 2: Uruchom aplikację Flask

**W pierwszym terminalu (PowerShell):**

```bash
cd C:\Users\gorsz\Desktop\Serwis-Informacyjny\Serwis-Informacyjny
python app.py
```

Poczekaj aż zobaczysz:
```
 * Running on http://127.0.0.1:5000
```

**NIE ZAMYKAJ TEGO TERMINALA!** Aplikacja musi działać podczas testów.

## Krok 3: Uruchom testy

**Otwórz DRUGI terminal (PowerShell) i uruchom:**

```bash
cd C:\Users\gorsz\Desktop\Serwis-Informacyjny\Serwis-Informacyjny
python -m pytest tests/e2e/test_homepage.py -v
```

## Co się stanie?

1. Testy otworzą przeglądarkę Chrome (w trybie headless - niewidoczną)
2. Przejdą na stronę http://localhost:5000/main/
3. Sprawdzą czy strona się załadowała
4. Sprawdzą czy są elementy (navbar, karty, stopka)

## Przykłady komend:

```bash
# Wszystkie testy e2e
python -m pytest tests/e2e/ -v

# Tylko testy strony głównej
python -m pytest tests/e2e/test_homepage.py -v

# Tylko testy logowania
python -m pytest tests/e2e/test_login.py -v

# Tylko testy horoskopu
python -m pytest tests/e2e/test_horoscope.py -v
```

## Ważne!

- **Zawsze używaj `python -m pytest`** zamiast `pytest` (na Windows)
- **Aplikacja Flask MUSI być uruchomiona** w innym terminalu
- Jeśli testy nie działają, sprawdź czy aplikacja działa na http://localhost:5000

## Jeśli coś nie działa:

1. Sprawdź czy aplikacja Flask działa - otwórz http://localhost:5000/main/ w przeglądarce
2. Sprawdź czy masz ChromeDriver - testy wymagają Chrome
3. Sprawdź czy pytest jest zainstalowany: `python -m pytest --version`

