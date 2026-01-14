# Instrukcja przygotowania dokumentacji projektu (na podstawie template’ów)


> **OD LINIJKI 250 SĄ WYPISANE W JAKO LISTA RZECZY DO UZUPEŁNIENIA**  

> **Cel dokumentu**  
> Ten plik wyjaśnia **jak korzystać z dostarczonych template’ów**, aby przygotować **docelową dokumentację projektu** aplikacji webowej (Flask).  
> Dokumentacja ma być na tyle kompletna, aby umożliwić: uruchomienie projektu, zrozumienie architektury, weryfikację API oraz wykonanie testów **bez wglądu w kod**.

---

## 1. Co dostarczamy (pliki startowe / template’y)

W ZIP'ie otrzymujecie zestaw plików dokumentacji:

### 1.1 Pliki, które będą w repo docelowo (po uzupełnieniu)
- `README.md` – główny opis projektu (w repo głównym) - jest 
- `doc/architecture.md` – architektura wspólna aplikacji
- `doc/api_reference.md` – **pełna** referencja endpointów (HTML + JSON) – jedno źródło prawdy
- `doc/setup.md` – konfiguracja środowiska i `.env`
- `doc/testing.md` – plan testów + tabele testów + raport
- `doc/project_management.md` – opis prowadzenia projektu (Scrum/Jira/sprinty/zespoły) - jest
- `doc/contribution.md` – zasady pracy i kontrybucji (workflow Git, PR, DoD, code review)
- `doc/architecture/<module>.md` – dokumentacja architektury modułów (po jednym pliku na moduł)
- `doc/assets/…` – zasoby do dokumentacji (screeny, diagramy, raporty)

### 1.2 Pliki pomocnicze
- `doc/module_template.md` – **wzorzec** do tworzenia `doc/architecture/<module>.md`  
  (może zostać w repo jako wzorzec, ale nie jest wymagany w wersji końcowej).


---

## 2. Docelowa struktura katalogów (wymagana)

Docelowo w repozytorium powinna istnieć poniższa struktura:

```text
.
├── README.md
└── doc/
    ├── architecture.md
    ├── api_reference.md
    ├── setup.md
    ├── testing.md
    ├── project_management.md
    ├── contribution.md
    ├── specification/
    │   ├── user_stories.md
    ├── architecture/
    │   ├── <module_1>.md
    │   ├── <module_2>.md
    │   └── ...
    └── assets/
        ├── screenshots/
        ├── diagrams/
        └── reports/
```

### 2.1 Zasoby w `doc/assets/`
- `doc/assets/screenshots/` – screenshoty głównych widoków aplikacji (używane w `README.md`)
- `doc/assets/diagrams/` – pliki diagramów (jeśli nie używacie Mermaid)
- `doc/assets/reports/` – raporty z testów (np. `report.html` z pytest)

---

## 3. Jak korzystać z template’ów (co uzupełnić, co usunąć)

### 3.1 Ogólne zasady edycji template’ów
1. **Wypełnij wszystkie miejsca oznaczone**: `TU UZUPEŁNIĆ`.
2. Wszystkie fragmenty oznaczone jako **PRZYKŁAD**:
   - potraktuj jako inspirację,
   - dostosuj do własnego projektu,
   - albo usuń, jeśli nie pasują.
3. Po zakończeniu prac:
   - w repo **nie powinno zostać** żadne `TU UZUPEŁNIĆ`,
   - usuń instrukcje, które nie są już potrzebne (np. „Instrukcja: …”).
4. Nie duplikuj treści:
   - szczegóły API tylko w `doc/api_reference.md`,
   - szczegóły modułu tylko w `doc/architecture/<module>.md`,
   - część wspólna tylko w `doc/architecture.md`.

---

## 4. Jak wypełnić poszczególne pliki

### 4.1 `README.md` (w repo głównym)
**Rola:** „Mapa projektu” + szybkie uruchomienie + skrót linków do dokumentacji.

**Uzupełnij przede wszystkim:**
- opis projektu (cel, najważniejsze funkcje),
- **Szybki start** (lokalnie),
- **Widoki aplikacji** (screenshoty w `doc/assets/screenshots/`),
- linki do dokumentacji w `doc/`,
- krótki opis modułów.

**Nie wklejaj do README:**
- szczegółowych opisów endpointów (to jest w `doc/api_reference.md`),
- szczegółowych opisów architektury modułów (to jest w `doc/architecture/<module>.md`).

---

### 4.2 `doc/architecture.md` (architektura wspólna)
**Rola:** opis wspólnych elementów całej aplikacji, niezależnie od modułów.

**Uzupełnij:**
- widok systemu jako całości,
- technologie wspólne,
- konwencje w repozytorium,
- przepływ danych (ogólny),
- **model danych wspólny** (tylko encje przekrojowe),
- cross-cutting concerns (config/logging/security),
- decyzje architektoniczne,
- linki do dokumentacji modułów.

**Nie opisuj tu:**
- szczegółów implementacji konkretnego modułu,
- tabel stricte modułowych,
- szczegółów endpointów (to jest w `doc/api_reference.md`).

---

### 4.3 `doc/architecture/<module>.md` (architektura modułu)
**Rola:** opis działania konkretnego modułu.

**Jak utworzyć plik modułu:**
1. Skopiuj `doc/module_template.md` do `doc/architecture/<nazwa_modulu>.md`.
2. Zmień tytuł oraz dostosuj treść do swojego modułu.
3. Wypełnij wszystkie `TU UZUPEŁNIĆ`.

**Kluczowe zasady:**
- **Sekcja 5 (Interfejs modułu)**: tylko tabela skrótowa + linki do `api_reference.md` (bez duplikacji request/response).
- **Sekcja 7 (Model danych modułu)**: opisz dane modułu:
  - encje bazodanowe (tabele modułu),
  - obiekty domenowe bez tabel (obiekty z API itp.),
  - relacje i przepływ danych.

---

### 4.4 `doc/api_reference.md` (pełna specyfikacja API)
**Rola:** „kontrakt API” + podstawa do testów integracyjnych (HTML + JSON).

**Wymaganie:** Dokument ma pozwolić na przygotowanie testów integracyjnych **bez czytania kodu**.

**Uzupełnij dla każdego endpointu:**
- metoda, ścieżka, typ (HTML/JSON), opis,
- parametry (query/path/body),
- przykłady requestów (np. curl),
- przykłady odpowiedzi (HTML/JSON),
- kody odpowiedzi i błędy,
- powiązanie z User Story (jeśli dotyczy),
- informacja o auth (jeśli dotyczy).

**Nie opisuj tu:**
- architektury modułów (to jest w `doc/architecture/<module>.md`).

---

### 4.5 `doc/setup.md` (konfiguracja i środowisko)
**Rola:** instrukcja uruchomienia środowiska + opis `.env`.

**Uzupełnij:**
- wymagania systemowe (Python/Node/OS),
- instalacja lokalna,
- pełna tabela zmiennych `.env` (opis + czy wymagane),
- `.env.example` (bez sekretów),
- różnice środowisk (dev/test/prod),
- typowe problemy.

---

### 4.6 `doc/testing.md` (plan testów + raport)
**Rola:** standard testowania w projekcie + minimalne wymagania + tabele testów.

**Wymagane:**
- testy Unit / Integration / E2E,
- **oddzielna tabela testów dla każdego modułu**,
- mapowanie E2E ↔ User Stories,
- instrukcja generowania raportu HTML:
  ```bash
  pytest --html=report.html --self-contained-html
  ```
- umieszczenie raportu w:
  - `doc/assets/reports/report.html`

---

### 4.7 `doc/project_management.md` (prowadzenie projektu)
**Rola:** opis procesu wytwórczego: Scrum, Jira, sprinty, podział zespołu.

**Uzupełnij minimalnie:**
- link do Jiry,
- link do repozytorium,
- ewentualne różnice między planem a realizacją (jeśli wystąpiły).

---

### 4.8 `doc/contribution.md` (zasady pracy)
**Rola:** zasady współpracy w repo: workflow, commity, PR, DoD, review.

**Uzupełnij:**
- przyjęty workflow (branching),
- zasady commitów (np. z ID z Jiry),
- zasady PR i code review,
- Definition of Done.

---

## 5. Zalecana kolejność uzupełniania dokumentacji

1. `README.md` – szkic (opis + szybki start + linki) 
2. `doc/project_management.md` – uzupełnienie linków (Jira/GitHub)
3. `doc/architecture.md` – część wspólna (bez modułów)
4. `doc/architecture/<module>.md` – moduły (na bazie template’u)
5. `doc/api_reference.md` – pełny kontrakt endpointów (HTML + JSON)
6. `doc/setup.md` – środowisko + `.env`
7. `doc/testing.md` – plan testów + tabele + raport
8. `README.md` – finalizacja (screeny, porządki, aktualizacja linków)

---

## 6. Checklista „dokumentacja gotowa” (wymagane)

- [ ] W repo nie ma fragmentów `TU UZUPEŁNIĆ`
- [ ] Wszystkie moduły mają swój plik: `doc/architecture/<module>.md`
- [ ] `doc/api_reference.md` zawiera **wszystkie** endpointy HTML + JSON
- [ ] `doc/testing.md` zawiera tabele testów dla każdego modułu i opis raportu HTML
- [ ] `doc/assets/screenshots/` zawiera aktualne screenshoty i README je wyświetla
- [ ] `doc/assets/reports/report.html` istnieje (lub wskazano, jak go wygenerować)
- [ ] Linki w README i dokumentacji działają (ścieżki względne)
- [ ] W `setup.md` istnieje kompletna tabela `.env` + `.env.example` bez sekretów

---

## 7. Najczęstsze błędy (czego unikać)

- Duplikowanie szczegółowych opisów endpointów w plikach modułów (powinny być tylko w `doc/api_reference.md`).
- Opisywanie danych modułowych w `architecture.md` (powinny być w `doc/architecture/<module>.md`).
- Brak powiązania testów E2E z User Stories.
- Brak raportu HTML z testów lub brak informacji, jak go wygenerować.
- Brak aktualnych screenshotów w README.

---





**do uzupełnienia**

---

## Lista rzeczy do uzupełnienia

---

## Checklista zgodności z instrukcją (sekcja 6)

### Wymagane pliki i ich status:
- [x] `README.md` – główny opis projektu - **GOTOWE**
- [x] `docs/architecture.md` – architektura wspólna aplikacji - **GOTOWE**
- [x] `docs/api_reference.md` – pełna referencja endpointów - **GOTOWE**
- [x] `docs/setup.md` – konfiguracja środowiska i `.env` - **GOTOWE**
- [ ] `docs/testing.md` – plan testów + tabele testów + raport - **BRAK**
- [x] `docs/project_management.md` – opis prowadzenia projektu - **GOTOWE**
- [ ] `docs/contribution.md` – zasady pracy i kontrybucji - **BRAK**
- [x] `docs/architecture/auth.md` – dokumentacja modułu auth - **GOTOWE**
- [x] `docs/architecture/calendar.md` – dokumentacja modułu calendar - **GOTOWE**
- [x] `docs/architecture/economy.md` – dokumentacja modułu economy - **GOTOWE**
- [ ] `docs/architecture/weather.md` – dokumentacja modułu weather - **DO UZUPEŁNIENIA** (5x `TU UZUPEŁNIĆ`)
- [x] `docs/architecture/news.md` – dokumentacja modułu news - **GOTOWE**

### Checklista "dokumentacja gotowa" (z instrukcji):
- [ ] W repo nie ma fragmentów `TU UZUPEŁNIĆ` - **NIE** (weather.md ma 5 miejsc)
- [ ] Wszystkie moduły mają swój plik: `docs/architecture/<module>.md` - **TAK** (ale weather.md i news.md nie są uzupełnione)
- [x] `docs/api_reference.md` zawiera **wszystkie** endpointy HTML + JSON - **TAK**
- [ ] `docs/testing.md` zawiera tabele testów dla każdego modułu i opis raportu HTML - **BRAK PLIKU**
- [x] `docs/assets/screenshots/` zawiera aktualne screenshoty i README je wyświetla - **TAK**
- [ ] `docs/assets/reports/report.html` istnieje (lub wskazano, jak go wygenerować) - **BRAK**
- [x] Linki w README i dokumentacji działają (ścieżki względne) - **TAK**
- [x] W `setup.md` istnieje kompletna tabela `.env` + `.env.example` bez sekretów - **TAK**

---

## Lista rzeczy do uzupełnienia (szczegółowa)

### Pliki do utworzenia (PRIORYTET 1):
- [x] `docs/setup.md` - konfiguracja środowiska i `.env` - **GOTOWE**
  - [x] Wymagania systemowe (Python/Node/OS)
  - [x] Instalacja lokalna
  - [x] Pełna tabela zmiennych `.env` (opis + czy wymagane)
  - [x] `.env.example` (bez sekretów)
  - [x] Różnice środowisk (dev/test/prod)
  - [x] Typowe problemy

- [ ] `docs/testing.md` - plan testów + tabele testów + raport
  - Testy Unit / Integration / E2E
  - Oddzielna tabela testów dla każdego modułu
  - Mapowanie E2E ↔ User Stories
  - Instrukcja generowania raportu HTML
  - Umieszczenie raportu w `docs/assets/reports/report.html`

- [ ] `docs/contribution.md` - zasady pracy i kontrybucji
  - Przyjęty workflow (branching)
  - Zasady commitów (np. z ID z Jiry)
  - Zasady PR i code review
  - Definition of Done

### Pliki do uzupełnienia (PRIORYTET 1):
- [ ] `docs/architecture/weather.md` - usunąć wszystkie `TU UZUPEŁNIĆ`:
  - [ ] Linia 22: lista User Stories
  - [ ] Linia 254: moduł, serwisy, modele, zależności
  - [ ] Linia 263: testy jednostkowe
  - [ ] Linia 266: testy integracyjne
  - [ ] Linia 271: testy akceptacyjne

- [x] `docs/architecture/news.md` - dokumentacja modułu news - **GOTOWE**

### Zasoby (assets):
- [ ] Sprawdzić czy screenshoty są aktualne i odpowiadają aktualnemu wyglądowi aplikacji
- [ ] Wygenerować raport HTML z testów (gdy będą testy):
  ```bash
  pytest --html=docs/assets/reports/report.html --self-contained-html
  ```
- [ ] Dodać diagramy do `docs/assets/diagrams/` (jeśli nie używamy tylko Mermaid) - **OPCJONALNE: jeśli używamy Mermaid w dokumentacji, nie jest wymagane**

### Ogólne sprawdzenie i finalizacja:
- [x] Sprawdzić czy wszystkie linki w dokumentacji działają (ścieżki względne) - **TAK**
- [ ] Upewnić się, że nie ma żadnych `TU UZUPEŁNIĆ` w całym repo (sprawdzić wszystkie pliki .md) - **NIE** (weather.md)
- [x] Usunąć wszystkie instrukcje pomocnicze (np. "Instrukcja: ...", "PRZYKŁAD:") - **TAK**
- [ ] Sprawdzić spójność numeracji User Stories w całej dokumentacji
- [ ] Sprawdzić czy wszystkie moduły mają linki w `docs/architecture.md` (sekcja 10)
- [ ] Sprawdzić czy `README.md` ma poprawne linki do wszystkich dokumentów
- [ ] Sprawdzić czy `docs/architecture.md` ma poprawne linki do modułów (auth, calendar, economy, weather, news)

---

## Podsumowanie statusu:

**Zgodność z instrukcją: ~80%**

**Uzupełnione w 100% (poza weather.md):**
- README.md
- docs/architecture.md
- docs/api_reference.md
- docs/setup.md
- docs/project_management.md
- docs/architecture/auth.md
- docs/architecture/calendar.md
- docs/architecture/economy.md

**Gotowe (100% uzupełnione):**
- README.md
- docs/architecture.md
- docs/api_reference.md (wszystkie endpointy)
- docs/setup.md
- docs/project_management.md
- docs/architecture/auth.md
- docs/architecture/calendar.md
- docs/architecture/economy.md
- docs/architecture/news.md
- Screenshoty w docs/assets/screenshots/

**Brakuje:**
- docs/testing.md
- docs/contribution.md
- Raport HTML z testów

**Wymaga uzupełnienia:**
- docs/architecture/weather.md (5x `TU UZUPEŁNIĆ`)