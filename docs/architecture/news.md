# Architektura modułu: Moduł `news`

> **Cel dokumentu:**  
> Ten plik opisuje budowę **modułu news**, który wyświetla najnowsze wiadomości które są zbierane na bazie scraperów

---

## 1. Cel modułu

Moduł **news** (z wiadomościami) dostarcza funkcje związane z przeglądaniem wiadomości.
- Wyświetla najnowsze zescrapowane wiadomości kryminalne i sportowe
- Zezwala na wyszukiwanie wiadomości po kategoriach, frazie lub dacie
- Zezwala na zapisywanie wiadomości w zakładkach
- Zapisuje historię przeglądanych wiadomości 

---

## 2. Zakres funkcjonalny (powiązanie z User Stories)

- **US-13** - Jako użytkownik chcę na stronie serwisu mieć dostęp do najnowszych wiadomości sportowych i kryminalnych z Krakowa 
- **US-32** - Jako użytkownik na stronie serwisu wiadomości chce mieć osobny widok na wiadomości kryminalne i sportowe
- **US-34** - Jako użytkownik chcę na stronie serwisu widzieć przed wybraniem zakładki widzieć około 10 najnowszych wiadomości.
- **US-49** - Jako użytkownik chcę mieć z widoku strony głównej możliwość przejścia na stronę serwisu wiadomości 
- **US-36** - Jako użytkownik na stronie serwisu chcę mieć możliwość wyszukania danych wiadomości po nazwie, kategoriach lub dacie.
- **US-35** - Jako zalogowany użytkownik na stronie serwisu, chcę widzieć historie swoich poprzednich haseł wpisanych w wyszukiwarkę. 
- **US-41** - Jako zalogowany użytkownik na stronie serwisu chcę mieć możliwość dodawania wiadomości do "zakładki" do której mam dostęp z poziomu strony serwisu (zapisywanie wiadomości do przeczytania na później) 

---

## 3. Granice modułu (co wchodzi / co nie wchodzi)

### 3.1 Moduł odpowiada za
- Pobieranie treści z zdefiniowanych źródeł (scrapery/RSS) i normalizację artykułów do wspólnego modelu.
- Przechowywanie artykułów w lokalnej bazie (cache), serwowanie widoków HTML oraz API (listy, szczegóły, wyszukiwanie).
- Funkcjonalności użytkownika związane z zakładkami i historią wyszukiwań/przeglądania.
- Walidację i paginację wyników oraz prostą filtrację po kategoriach i dacie.

### 3.2 Moduł nie odpowiada za
- Autoryzację globalną użytkowników
- Złożone operacje analityczne / rekomendacje (poza prostą listą najnowszych).

---

## 4. Struktura kodu modułu

Aktualna struktura katalogu modułu `news` w repozytorium (odwzorowuje rzeczywiste pliki):

- serwis_info/modules/news/
  - db/                       -- katalog pomocniczy z danymi/DB modułu
  - news.db                   -- lokalna baza modułu (sqlite)
  - routes/                   -- routy/endpointy modułu
    - news_page.py            -- blueprint / widoki strony wiadomości
  - services/                 -- logika biznesowa i scraper'y
    - articles_data_builder.py
    - articles_data_giver.py
    - articles_saver.py
    - bookmarks_service.py
    - history_service.py
    - scheduler.py
    - scraper_cowkrak.py
    - scraper_onet.py
    - scraper_test.py
    - articles.json            
    - articles_sport.json
    - articles_crime.json             
  - templates/                -- szablony HTML używane przez widoki modułu
    - news_search.html
    - crime_news.html
    - sport_news.html
    - sport_scraped.html
    - bookmarks.html
    - detail.html
    - nav_footnews.html
    - _init_.py
  - static/                   -- zasoby statyczne modułu (JS/CSS/dane)
    - bookmarks.js
    - test_news.css
    - sport_data.json
    - sport_news_data.json

Uwagi:
- W repozytorium moduł nie używa plików o nazwach `views.py` czy `api.py` - zamiast nich znajdują się konkretne skrypty w `routes/` i `services/`.
- Scrapery są zaimplementowane jako osobne pliki (`scraper_cowkrak.py`, `scraper_onet.py`, `scraper_test.py`) i korzystają z lokalnych JSON-ów jako przykładowych źródeł.
- Pliki `articles_*.json` służą jako fixture/cache i mogą być wykorzystywane przez testy lub jako fallback.

---

## 5. Interfejs modułu

Poniżej przedstawiono endpointy udostępniane przez ten moduł.
Szczegółowa specyfikacja każdego endpointu (parametry, odpowiedzi, błędy)
znajduje się w pliku [`docs/api_reference.md`](../api_reference.md).

| Metoda | Ścieżka | Typ | Rola w module | Powiązane User Stories | Szczegóły |
|---:|---|---|---|---|---|
| GET | /news/ | HTML | Widok główny modułu (kafelki + lista najnowszych) | US-13, US-34, US-49 | [api_reference.md#news-html](../api_reference.md#news-html) |
| GET | /news/crime | HTML | Lista wiadomości kryminalnych | US-32 | [api_reference.md#news-category-crime](../api_reference.md#news-category-crime) |
| GET | /news/sport | HTML | Lista wiadomości sportowych | US-32 | [api_reference.md#news-category-sport](../api_reference.md#news-category-sport) |
| GET | /news/detail/<news_id> | HTML | Szczegóły artykułu (zapis historii, sprawdzenie bookmarka) | US-13 | [api_reference.md#news-detail](../api_reference.md#news-detail) |
| GET | /news/search | HTML | Formularz wyszukiwania + panel historii użytkownika | US-36, US-35 | [api_reference.md#news-search-form](../api_reference.md#news-search-form) |
| GET | /news/search/results | HTML | Wyniki wyszukiwania (q, scope, from_date, to_date) | US-36 | [api_reference.md#news-search-results](../api_reference.md#news-search-results) |
| GET | /news/bookmarks | HTML | Widok zakładek zalogowanego użytkownika | US-41, US-35 | [api_reference.md#news-bookmarks](../api_reference.md#news-bookmarks) |
| POST | /news/api/bookmark/add | JSON | Dodaj artykuł do zakładek (wymaga auth) | US-41 | [api_reference.md#api-news-bookmark-add](../api_reference.md#api-news-bookmark-add) |
| POST | /news/api/bookmark/remove | JSON | Usuń artykuł z zakładek (wymaga auth) | US-41 | [api_reference.md#api-news-bookmark-remove](../api_reference.md#api-news-bookmark-remove) |

---

## 6. Zewnętrzne API / źródła wykorzystywane przez moduł (scrapery)

Moduł opiera się głównie na własnych scraperach (brak centralnego zewnętrznego provider-a z jednym API). Obecne implementacje pokazują:

- scraper_onet.py - scraper dla sekcji sportowych serwisu `przegladsportowy.onet.pl` (Selenium + BeautifulSoup). Zbiera tytuł, datę (meta tag), treść (p), nagłówki (h2) i obrazy. Funkcja: onet_scraper_function(size_of_scrap) → lista artykułów.

- scraper_cowkrak.py - scraper dla sekcji kryminalnych serwisu `cowkrakowie.pl/category/kryminalne` (Selenium + BeautifulSoup).

- articles_saver.py - agreguje wyniki ze scraperów (onet + cowkrak), porównuje po URL, dopisuje nowe artykuły do plików `articles_sport.json` i `articles_crime.json`. Można uruchomić ręcznie lub z poziomu scheduler-a.

Zasady autoryzacji i limity
- Scrapery działają jako klient HTTP/automatyzowany (Selenium). Należy respektować polityki źródeł. W kodzie nie ma centralnego rate-limitingu poza prostymi opóźnieniami i mechanizmami unikania duplikatów.

Mapowanie pola artykułu (format używany wewnętrznie):
- id / id_number (unikalny identyfikator w pliku),
- title, summary (opcjonalne), content (lista bloków tekstu), url/link, published_at (ISO / datetime), category (sport|crime), images (lista url), author_name, subcategory, source_name

### 6.1 Konfiguracja (zmienne środowiskowe)

- NEWS_DB_PATH - opcjonalna ścieżka do pliku SQLite używanego przez moduł (`serwis_info/modules/news/db/connection.py` domyślnie wskazuje `.../news.db`).

(Uwaga: w repo nie znaleziono innych globalnych zmiennych konfiguracyjnych typu API_KEY dla scrapers; scrapery konfiguruje się parametrem `size_of_scrap` lub przez uruchamianie `articles_saver()` / `scheduler`.)

### 6.2 Wywołanie API zakładek

- Dodanie zakładki (skrót): JSON -> POST /news/api/bookmark/add
  - body: { "article_id": "os12345", "article_title": "Tytuł", "article_category": "sport" }
  - sukces: { "success": true }

- Usunięcie zakładki: POST /news/api/bookmark/remove
  - body: { "article_id": "os12345" }

---

## 7. Model danych modułu

Sekcja opisuje tabele i obiekty używane przez implementację (pliki w `serwis_info/modules/news/db/`).

### 7.1 Encje bazodanowe (tabele SQLite)

- users
  - id (INTEGER PK AUTOINCREMENT)
  - username (TEXT UNIQUE)
  - Rola: identyfikacja właściciela zakładek i historii; tabela minimalna (tylko id i username).

- bookmarks
  - id (INTEGER PK AUTOINCREMENT)
  - user_id (INTEGER NOT NULL) - FK → users.id
  - article_id (TEXT NOT NULL) - identyfikator artykułu (z scrappera / pliku JSON)
  - article_title (TEXT NOT NULL)
  - article_category (TEXT)
  - article_summary (TEXT)
  - article_source (TEXT)
  - article_url (TEXT)
  - timestamp (TEXT NOT NULL) - zapis daty dodania w formacie '%Y-%m-%d %H:%M:%S'
  - UNIQUE(user_id, article_id)
  - Rola: przechowywanie zakładek użytkownika; używane przez `bookmarks_service`.

- articles_history (articles_history)
  - id (INTEGER PK AUTOINCREMENT)
  - user_id (INTEGER NOT NULL) - FK → users.id
  - article_id (TEXT NOT NULL)
  - article_title (TEXT NOT NULL)
  - viewed_at (TEXT NOT NULL) - data ostatniego wyświetlenia
  - UNIQUE(user_id, article_id)
  - Rola: przechowywanie ostatnio oglądanych artykułów (użytkownik → artykuły)

### 7.2 Obiekty domenowe (DTO / struktury w pamięci)

- Artykuł (dict) - format zwracany z scraperów / plików JSON: { id / id_number, title, summary, content, url, published_at, category, images, author_name }
- HistoryEntry (dict) - { article_id, article_title, viewed_at }
- BookmarkEntry (dict) - { bookmark_id, article_id, article_title, article_category, article_summary, article_source, article_url, timestamp }

### 7.3 Relacje i ograniczenia

- Użytkownik (users) 1:N → bookmarks
- Użytkownik (users) 1:N → articles_history
- Zakładki/history odnoszą się do artykułu przez `article_id` (nie ma relacyjnego FK do tabeli artykułów - artykuły są przechowywane w plikach JSON lub zewnętrznie)

---

## 8. Przepływ danych w module

### Scenariusz: Zalogowany użytkownik wyszukuje wiadomości, przegląda szczegóły, dodaje do zakładek i sprawdza historię

1. **Użytkownik przechodzi na stronę News** (`GET /news/`)
   - Flask renderuje `nav_footnews.html` (szablon w `templates/`).
   - Widok wywołuje `articles_data_giver.load_articles('crime')` i `articles_data_giver.load_articles('sport')`, sortuje wyniki i wybiera najnowsze (kafelki).
   - Interfejs pokazuje kafelki z `crime_latest` i `sport_latest` oraz linki do list i szczegółów.

2. **Użytkownik wybiera kategorię (np. kryminalne)** (`GET /news/crime`)
   - Backend: `articles = articles_data_giver.load_articles('crime')` → sortowanie przez `_sort_articles` w `routes/news_page.py`.
   - Backend pobiera zakładki użytkownika: `bookmarks_service.fetch_user_bookmarks(current_user.id)` i tworzy zbiór `bookmarked_ids` do oznaczania elementów w szablonie.
   - Render: `crime_news.html` otrzymuje `articles` i `bookmarked_ids`.

3. **Użytkownik otwiera szczegóły artykułu** (`GET /news/detail/<news_id>`)
   - Backend ładuje wszystkie artykuły (`load_articles('all')`) i znajduje artykuł po `id_number` lub `id`.
   - Sprawdza, czy artykuł jest w zakładkach: `bookmarks_service.is_bookmarked(current_user.id, news_id)`.
   - Rejestruje wejście w historii: `history_service.record_view(current_user.id, article)` (zapis do `articles_history`).
   - Render: `detail.html` z danymi artykułu i flagą `is_bookmarked`.

4. **Użytkownik dodaje artykuł do zakładek** (akcja JS/Front → `POST /news/api/bookmark/add`)
   - Frontend wysyła JSON: { "article_id": ..., "article_title": ..., "article_category": ..., "article_summary": ..., "article_url": ..., "article_source": ... }.
   - Endpoint `api_bookmark_add` parsuje JSON i waliduje `article_id`.
   - Wywołanie serwisu: `bookmarks_service.add_article_to_bookmarks(current_user.id, ...)` → `db/bookmarks_repository.add_bookmark(...)` zapisuje rekord w tabeli `bookmarks` (unikatowe ograniczenie `UNIQUE(user_id, article_id)`).
   - Odpowiedź: JSON { "success": true } lub { "success": false, "error": "..." }.
   - Uwaga: w przypadku konfliktu (duplikat) repozytorium zwraca False i endpoint odpowiada błędem 500/odpowiednim komunikatem.

5. **Użytkownik usuwa artykuł z zakładek** (`POST /news/api/bookmark/remove`)
   - Frontend wysyła JSON: { "article_id": ... }.
   - Endpoint `api_bookmark_remove` wywołuje `bookmarks_service.remove_article_from_bookmarks(current_user.id, article_id)` → `db/bookmarks_repository.remove_bookmark` usuwa rekord.
   - Odpowiedź: JSON z polem `success`.

6. **Użytkownik wyszukuje artykuły** (formularz na `GET /news/search`, wyniki `GET /news/search/results`)
   - `GET /news/search` renderuje `news_search.html` z ostatnią historią: `history_service.get_view_history(current_user.id, limit=10)`.
   - Po wypełnieniu danych, frontend wywołuje `GET /news/search/results?q=fraza&scope=all|sport|crime&from_date=YYYY-MM-DD&to_date=YYYY-MM-DD`.
   - Backend:
     - ładuje odpowiedni zbiór artykułów: `load_articles(scope)`;
     - filtruje po tytule (q) i po dacie (parsowanie ISO / YYYY-MM-DD);
     - sortuje wyniki malejąco po `published_at` i zwraca render `news_search.html` z parametrami i historią.
   - Jeśli użytkownik kliknie wynik, to przebiega krok 3 (szczegóły) i wpis do historii jest zarejestrowany.

7. **Aktualizacja cache / scrapowanie (zadanie okresowe lub manualne)**
   - `articles_saver.py` wywołuje scrapers: `onet_scraper_function(...)` i `cowkrak_scraper_function(...)`, agreguje wyniki i porównuje po `url`.
   - Nowe artykuły są dopisywane do plików `services/articles_sport.json` i `services/articles_crime.json`.
   - Można uruchomić `articles_saver()` ręcznie lub uruchomić `scheduler.start_scheduler()` (jeśli skonfigurowany).
   - Endpointy modułu (np. `GET /news/`, `GET /news/crime`) zawsze czytają z `articles_*.json` przez `articles_data_giver.load_file_data`; w ten sposób nowe dane stają się widoczne po zapisaniu JSON.

8. **Wyświetlanie zescrapowanych artykułów** (`GET /news/sport/scraped`)
   - Widok ładuje `sport_news_data.json` (jeśli istnieje) albo używa `_sample_articles()` z `articles_data_giver`.
   - Render: `sport_scraped.html`.

---

Powyższy scenariusz odzwierciedla rzeczywiste wywołania i przepływy w `serwis_info/modules/news/`: szablony w `templates/`, logika w `routes/news_page.py`, operacje biznesowe w `services/*`, oraz trwałe zapisy zakładek i historii w `db/*.py` (SQLite). 

---

## 9. Diagramy modułu (skrót)

9.1 Sekwencja (wyświetlenie listy najnowszych):
- User -> Flask(view/news_home) -> articles_data_giver.load_articles -> services/*.json -> render_template -> User

9.2 Komponenty:
- routes/news_page.py (widoki + prosty API dla zakładek)
- services/* (scrapery, saver, bookmarks_service, history_service)
- db/* (connection + repositories dla bookmarks i history)
- static/, templates/

---

## 10. Testowanie modułu

Istnieją testy e2e/integracyjne w repo (Playwright + pytest). Rekomendacje i punktacja:

10.1 Unit tests (pytest)
test_news_bookmark_remove.py - kompleksowy test sprawdzający działanie zapisu zakladki jak i jego usuwanie
test_news_detail.py - test sprawdza czy uzytkownik jest w stanie przegladać artykułu 
test_news_history.py - test sprawdza poprawność działania historii wyszukiwania
test_news_list.py - test sprawdza działanie listy artykułów
test_news_search.py - test sprawdza wyszukiawrke artykułów 

10.2 Integration tests (Flask)
- Widoki: /news/, /news/crime, /news/sport, /news/detail/<id> - testy wymagają kontekstu zalogowanego użytkownika (Flask-Login fixture).
- API zakładek: POST /news/api/bookmark/add i /remove - testy tworzenia/usuwania i sprawdzenia stanu bazy (testowy plik news.db w `serwis_info/modules/news/` lub tymczasowy `NEWS_DB_PATH`).

10.3 Acceptance / E2E (Playwright)
- Scenariusze mapujące US-13, US-34, US-35, US-41: sprawdzenie widoczności list, dodania do zakładek, historii wyszukań.

Szybkie testy do dodania (pytest):
- test_load_articles_returns_list
- test_add_and_remove_bookmark_updates_db
- test_search_filters_by_title_and_date

---

## 11. Ograniczenia, ryzyka, dalszy rozwój

- Scrapowanie: techniczne ryzyka - sprawdzać polityki źródeł; rozważyć użycie oficjalnych API dostawców tam, gdzie to możliwe. Konieczność modyfikowania scraperów pod każdą stronę
- Skalowalność: aktualnie artykuły przechowywane w lokalnych plikach JSON (cache) i lokalnym SQLite; dla większego ruchu warto przenieść do centralnego DB i workerów (np. Celery/Redis), oraz serwisu cachującego.
- Atomowość / duplikaty: obecna deduplikacja odbywa się po URL przy zapisie do JSON; rozważyć dodatkowe mechanizmy deduplikacji i normalizacji (hash treści).
- Rate-limit i retry: scrapery używają prostych opóźnień; dodać bardziej solidny limiter i backoff.
- Bezpieczeństwo: endpointy zakładek wymagają zalogowania, ale wejścia z frontendu powinny być dodatkowo walidowane (np. długości pól, typy).

Dalsze kroki (propozycje):
- Dodać kolejne scrapery dla większej liczby lokalnych portali i kategorii (łatwy adapter dla nowych źródeł).
- Dodać automatyczne tagowanie artykułów (słownik + lekka NLP) oraz interfejs do ręcznej korekty tagów.
- Rozszezenie segmentu histori wyszukiwania o statystyki (najczęściej wyszukiwane frazy itp.).