# Architektura modułu: Moduł `weather`

> **Cel dokumentu:**  
> Ten dokument odpowiada na pytanie: **„Jak moduł pogodowy działa i na jakich danych operuje?”**

 
> Architektura wspólna całej aplikacji: [`doc/architecture.md`](../architecture.md)

---

## 1. Cel modułu

Moduł pogodowy odpowiada za pobieranie, prezentowanie i archiwizowanie informacji pogodowych dla użytkowników serwisu. Udostępnia dane o aktualnej pogodzie, prognozie godzinowej i 3-dniowej oraz ostrzeżenia pogodowe. Moduł zarządza również historią wyszukiwań użytkowników i integruje dane z zewnętrznego API OpenWeatherMap.

---

## 2. Zakres funkcjonalny (powiązanie z User Stories)

**TU UZUPEŁNIĆ:** wstaw listę User Stories (ID z Jiry + krótki opis).

- **US2** Jako użytkownik zalogowany chcę zobaczyć informacje dla wybranej przeze mnie lokalizacji dotyczące temperatury, ciśnienia, opadów, wiatru, wilgotności powietrza, jakości powietrza
- **US1** Jako użytkownik niezalogowany chcę zobaczyć pogodę dla Warszawy / mojej domyślnej lokalizacji. 
- **US3** Jako użytkownik chcę zobaczyć graficzną prezentację informacji pogodowych na mapie dla lokalizacji.
- **US4** Jako użytkownik chcę otrzymać powiadomienie, gdy pogoda gwałtownie się zmienia
Alerty o:
opadach śniegu,
opadach deszczu,
temperaturze poniżej 0 oraz powyżej 30 stopni Celsjusza,
burzach.
- **US6**
 Jako użytkownik chcę zobaczyć moje poprzednie lokalizacje po ponownym zalogowaniu
 -**US5**
Jako użytkownik, chcę zobaczyć prognozę pogody na kilka dni, aby zaplanować swoje aktywności.
---


## 3. Granice modułu (co wchodzi / co nie wchodzi)

### 3.1 Moduł odpowiada za
Pobieranie danych pogodowych z OpenWeatherMap.

Przechowywanie i odczyt historii wyszukiwań użytkowników w lokalnej bazie SQLite.

Generowanie ostrzeżeń pogodowych na podstawie pobranych danych.

Obsługę widoku panelu pogodowego i warstw mapy w UI.

### 3.2 Moduł nie odpowiada za
Autoryzację i zarządzanie użytkownikami (realizuje moduł auth).

Ogólną nawigację i wygląd strony (realizuje moduł dashboard/navbar).

Globalne ustawienia serwisu informacyjnego, np. newsy czy inne moduły.

---

## 4. Struktura kodu modułu
serwis_info/modules/weather/
│
├─ db/                       #przechowywanie historii wyszukiwań i uzytkowników
│  ├─ connection.py          # Połączenie z bazą SQLite (users.db)
│  ├─ history_repository.py  # Operacje CRUD na historii wyszukiwań
│  └─ user_repository.py     # Operacje na użytkownikach modułu (np. użytkownik demo)
│
├─ routes/                   #API Flaskowe dla pogody i historii
│  ├─ __init__.py            # Rejestracja blueprintów modułu
│  ├─ weather_routes.py      # Endpointy API pogodowego i konfiguracji
│  ├─ history_routes.py      # Endpointy API historii wyszukiwań
│  └─ dashboard_routes.py    # Routing widoku dashboardu pogodowego
│
├─ services/                 #logika, pośredniczy miedzy db a routes
│  └─ history_service.py     # Logika biznesowa historii wyszukiwań
│
├─ static/                   #frontend
│  ├─ style.css              # Style CSS specyficzne dla modułu pogodowego
│  └─ js/                    #interakcje uzytkownika, mapy, alerty
│     ├─ app.js              # Główna inicjalizacja modułu w UI
│     ├─ config.js           # Pobieranie konfiguracji (API_KEY, API_URL)
│     ├─ forecast.js         # Prognoza wielodniowa i godzinowa + wykresy
│     ├─ alerts.js           # Generowanie ostrzeżeń pogodowych
│     ├─ history.js          # Obsługa historii wyszukiwań w UI
│     ├─ mapControls.js      # Obsługa mapy i warstw pogodowych
│     ├─ mapLayers.js        # Definicje warstw OpenWeatherMap
│     ├─ panel.js            # Logika panelu bocznego użytkownika
│     ├─ search.js           # Wyszukiwanie miast i karty pogodowe
│     ├─ user.js             # Obsługa użytkownika (cookie, display name)
│     └─ weather.js          # Mini-widget bieżącej pogody i prognozy 3-dniowej
│
├─ templates/
│  └─ dashboard.html         # Widok dashboardu pogodowego
│
└─ users.db                  # Lokalna baza danych SQLite modułu pogodowego


- **routes/** – endpointy HTTP (API + HTML)
- **services/** – logika biznesowa
- **db/** – dostęp do SQLite
- **static/** – frontend JS
- **templates/** – widoki HTML

---

## 5. Interfejs modułu

>**Instrukcja:**
>Nie powielaj szczegółów request/response – pełna specyfikacja znajduje się w api_reference.md.

Poniżej przedstawiono endpointy udostępniane przez ten moduł.
Szczegółowa specyfikacja każdego endpointu (parametry, odpowiedzi, błędy)
znajduje się w pliku [`doc/api_reference.md`](../api_reference.md).


| Metoda | Endpoint                         | Typ  | Opis                               | User Stories        | Dokumentacja |
|:------:|----------------------------------|:----:|------------------------------------|---------------------|--------------|
| GET    | /weather/dashboard               | HTML | Dashboard pogodowy                 | US1–US6             | api_reference.md#weather-dashboard |
| GET    | /weather/api/config              | JSON | Konfiguracja (API_KEY, API_URL)    | US1–US3             | api_reference.md#weather-config |
| GET    | /weather/api/simple_weather      | JSON | Bieżąca pogoda (domyślna lokalizacja) | US1              | api_reference.md#weather-simple |
| GET    | /weather/api/forecast            | JSON | Prognoza dzienna i godzinowa       | US5                 | api_reference.md#weather-forecast |
| GET    | /weather/api/history/{username}  | JSON | Historia wyszukiwań użytkownika    | US6                 | api_reference.md#weather-history |
| POST   | /weather/api/history/{username}  | JSON | Dodanie miasta do historii         | US2, US6            | api_reference.md#weather-history-add |
| DELETE | /weather/api/history/{username}  | JSON | Usunięcie historii użytkownika     | US6                 | api_reference.md#weather-history-delete |

US1 – domyślna pogoda (Warszawa) → dashboard + simple_weather
US2 – szczegóły dla wybranego miasta → dashboard + zapis historii
US3 – wizualizacja (mapa) → dashboard + config
US4 – alerty → dashboard
US5 – prognoza → forecast
US6 – zapamiętywanie lokalizacji → history GET/POST/DELETE

---

## 6. Zewnętrzne API wykorzystywane przez moduł

Moduł korzysta z API OpenWeatherMap (https://openweathermap.org/
):

Current Weather Data — bieżąca pogoda (/weather)

5 day / 3 hour forecast — prognoza godzinowa i 3-dniowa (/forecast)

Air Pollution API — jakość powietrza (/air_pollution)

Weather Map Layers — warstwy mapy (/tile/{layer}/{z}/{x}/{y}.png)

Autoryzacja: klucz API (API_KEY) w .env.
Mapowanie danych: odpowiedzi JSON → obiekty JS (np. main.temp, weather[0].description).

### 6.1 Konfiguracja (zmienne `.env`)

Wpisz zmienne używane do konfiguracji API:

| Zmienna                 | Przykład | Opis                    | Wymagana |
| ----------------------- | -------- | ----------------------- | -------- |
| **OPENWEATHER_API_KEY** | `123abc` | Klucz do OpenWeatherMap | TAK      |


### 6.2 Przykład zapytania do API (opcjonalnie)

```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=Warsaw&units=metric&lang=pl&appid=$OPENWEATHER_API_KEY"
```

### 6.3 Obsługa błędów i fallback
Jeśli API nie odpowiada, frontend wyświetla komunikat błędu lub brak danych.

Cache w forecast.js redukuje liczbę powtórnych wywołań dla tej samej lokalizacji.

Ostrzeżenia (alerts.js) zwracają pustą tablicę, jeśli brak danych.

---

## 7. Model danych modułu

> **Cel tej sekcji:**  
> Opisać **wszystkie dane**, na których operuje moduł.  
> Obejmuje to zarówno **encje bazodanowe**, jak i **obiekty domenowe bez własnych tabel**.

> **Ważne:**  
> Nie powtarzaj tutaj pełnego opisu encji wspólnych całej aplikacji  
> (np. `User`). Możesz się do nich odwołać.

---

### 7.1 Encje bazodanowe (tabele)

users — informacje o użytkownikach modułu (wspólna tabela, minimalny rekord dla historii).

pola: id, username

history — zapis wyszukiwanych miast przez użytkowników

pola: id, username, query (nazwa miasta), timestamp

relacja: username → users.username (referencja logiczna)

---

### 7.2 Obiekty domenowe (bez tabel w bazie)

WeatherData — dane pobierane z OpenWeatherMap (main, weather, wind, coord)

ForecastData — lista prognoz godzinowych (list[])

AlertData — ostrzeżenia generowane na podstawie prognozy (temp, wind, code, desc)

---

### 7.3 Relacje i przepływ danych

Użytkownik → wpisuje miasto w wyszukiwarce → search.js → wywołanie API OpenWeatherMap.

Dane pogodowe → wyświetlane w kartach i mapie → dodawane do historii (history_service.py).

Prognoza godzinowa/dniowa → generowanie wykresów i szczegółów godzinowych.

Ostrzeżenia → przetwarzane na alerty tekstowe w JS → wyświetlane w panelu.

---

## 8. Przepływ danych w module

Scenariusz: Wyszukanie pogody dla miasta

Użytkownik wpisuje nazwę miasta w polu wyszukiwania i klika „Szukaj”.

search.js wykonuje fetch /api/weather?city=<miasto> i /api/air_pollution.

Otrzymane dane wyświetlane są w karcie pogodowej, dodawane do mapy i historii (/api/history/<username>).

forecast.js umożliwia wybór dnia i godziny → generuje wykres temperatury.

alerts.js pobiera prognozę i generuje ostrzeżenia → wyświetlane w panelu bocznym.

---

## 9. Diagramy modułu (wymagane)

### 9.1 Diagram sekwencji (dla 1 user story)

**Opcja: Mermaid**

```mermaid
sequenceDiagram
  participant U as User/Browser
  participant F as Flask
  participant DB as Database
  participant API as OpenWeatherMap

  U->>F: POST /api/history/<username> + city
  F->>API: GET /weather?q=city
  API-->>F: JSON z pogodą
  F->>DB: INSERT INTO history (username, city, timestamp)
  DB-->>F: potwierdzenie zapisu
  F-->>U: JSON z pogodą, ostrzeżeniami i AQI

  ```

### 9.2 Diagram komponentów modułu (opcjonalnie)

**TU UZUPEŁNIĆ:** moduł, serwisy, modele, zależności.

---

## 10. Testowanie modułu

Szczegóły: [`doc/testing.md`](../testing.md)

### 10.1 Unit tests (pytest)
**TU UZUPEŁNIĆ:** 
Testy jednostkowe koncentrują się na logice biznesowej modułu oraz funkcjach pomocniczych, niezależnych od frameworka Flask i zewnętrznych API.

Zakres testów jednostkowych:
logika generowania ostrzeżeń pogodowych (temperatura, wiatr),
agregacja i przetwarzanie danych prognozy (średnie wartości, wybór ikony/opisu)

logika serwisów (warstwa services):
dodawanie miasta do historii,
pobieranie historii,
czyszczenie historii,
funkcje pomocnicze (np. budowanie URL warstw mapowych).

Przykładowe pliki:
tests/unit/weather/test_alerts_logic.py
tests/unit/weather/test_forecast_processing.py
tests/unit/weather/test_history_service.py
tests/unit/weather/test_weather_utils.py

### 10.2 Integration tests (HTML/API)
**TU UZUPEŁNIĆ:** 
Testy integracyjne sprawdzają poprawne działanie endpointów Flask oraz ich integrację z:
warstwą routingu,
serwisami,
bazą danych SQLite,
zewnętrznym API (mockowane).

Zakres testów integracyjnych:
konfiguracja API (/weather/api/config),
bieżąca pogoda (/weather/api/simple_weather) – z mockiem OpenWeatherMap,
prognoza 3-dniowa (/weather/api/forecast) – z mockiem danych,

API historii wyszukiwań:
GET /weather/api/history/<username>,
POST /weather/api/history/<username>,
DELETE /weather/api/history/<username>,
renderowanie HTML dashboardu pogodowego (/weather/dashboard).

Przykładowe pliki:
tests/integration/weather/test_weather_api.py
tests/integration/weather/test_weather_history_api.py
tests/integration/weather/test_weather_html.py

### 10.3 Acceptance tests (Playwright)
Wymaganie: **min. 1 test Playwright na każde User Story modułu**.
Testy akceptacyjne (E2E) realizowane są przy użyciu Playwright i symulują rzeczywiste zachowanie użytkownika w przeglądarce.
Każda User Story modułu pogodowego ma co najmniej jeden test akceptacyjny.

| User Story | Test          | Opis                                                    |
| ---------- | ------------- | ------------------------------------------------------- |
| **US1** | `test_US1.py` | Wyświetlenie bieżącej pogody dla Warszawy lub fallback  |
| **US2** | `test_US2.py` | Wyszukiwanie miasta i wyświetlenie szczegółów pogody    |
| **US5** | `test_US5.py` | Prognoza wielodniowa, kalendarz i widok godzinowy       |
| **US4** | `test_US4.py` | Wyświetlanie ostrzeżeń pogodowych                       |
| **US6** | `test_US6.py` | Odtworzenie ostatnio wyszukiwanych miast po odświeżeniu |
| **US3** | `test_US3.py` | Obsługa warstw mapy i legend                            |


---

## 11. Ograniczenia, ryzyka, dalszy rozwój

1. Ograniczenia
Moduł zależy od zewnętrznego API OpenWeatherMap (limity zapytań, dostępność).
Brak trwałego cache po stronie backendu (cache istnieje tylko w JS).
Historia wyszukiwań oparta o prostą bazę SQLite (ograniczona skalowalność).

2. Ryzyka
Przekroczenie limitów API przy dużej liczbie użytkowników.
Zmiany struktury odpowiedzi OpenWeatherMap mogą wymagać aktualizacji parserów.
Testy E2E zależne od działania JavaScript i czasu odpowiedzi API.

3. Dalszy rozwój
Rozszerzenie ostrzeżeń o więcej zjawisk.
Rozbudowa historii wyszukiwań (statystyki, ulubione miasta).
Mockowanie API OpenWeatherMap również w testach E2E.
