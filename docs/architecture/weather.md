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

- **US-WEATHER-01** Jako użytkownik zalogowany chcę zobaczyć informacje dla wybranej przeze mnie lokalizacji dotyczące temperatury, ciśnienia, opadów, wiatru, wilgotności powietrza, jakości powietrza
- **US-WEATHER-02** Jako użytkownik niezalogowany chcę zobaczyć pogodę dla Warszawy / mojej domyślnej lokalizacji. 
- **US-WEATHER-03** Jako użytkownik chcę otrzymać informację o braku danych gdy są one niedostępne.
- **US-WEATHER-04** Jako użytkownik chcę zobaczyć graficzną prezentację informacji pogodowych na mapie dla lokalizacji.
- **US-WEATHER-05** Jako użytkownik chcę otrzymać powiadomienie, gdy pogoda gwałtownie się zmienia

Alerty o:
opadach śniegu,
opadach deszczu,
temperaturze poniżej 0 oraz powyżej 30 stopni Celsjusza,

burzach.
- 
**US-WEATHER-06**
 Jako użytkownik chcę zobaczyć moje poprzednie lokalizacje po ponownym zalogowaniu
 - 
**US-WEATHER-07**
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
weather/
│
├─ db/
│  ├─ connection.py          # Połączenie z bazą SQLite
│  └─ history_repository.py  # CRUD historii wyszukiwań
│
├─ routes/
│  ├─ __init__.py            # Rejestracja blueprintów
│  ├─ weather_routes.py      # Endpointy pogodowe
│  └─ history_routes.py      # Endpointy historii
│
├─ services/
│  └─ history_service.py     # Logika historii wyszukiwań
│
├─ static/js/
│  ├─ app.js                 # Inicjalizacja panelu, mapy i wyszukiwania
│  ├─ config.js              # Pobranie API_KEY i URL
│  ├─ forecast.js            # Obsługa prognozy godzinowej/dniowej
│  ├─ alerts.js              # Obsługa ostrzeżeń pogodowych
│  ├─ history.js             # Ładowanie historii użytkownika
│  ├─ mapControls.js         # Sterowanie mapą i warstwami
│  ├─ mapLayers.js           # Definicje warstw OpenWeatherMap
│  ├─ panel.js               # Logika panelu bocznego
│  └─ search.js              # Wyszukiwanie miast i obsługa kart pogodowych
│
├─ templates/
│  └─ dashboard.html         # Widok modułu pogodowego

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

>**PRZYKŁAD TABELI:** dostosuj do swojego modułu.
| Metoda | Ścieżka                 | Typ  | Rola w module                        | Powiązane User Stories | Szczegóły                               |
| -----: | ----------------------- | ---- | ------------------------------------ | ---------------------- | --------------------------------------- |
|    GET | /dashboard              | HTML | Widok dashboardu pogodowego          | US-201, US-202         | api_reference.md#weather-dashboard      |
|    GET | /api/config             | JSON | Pobranie konfiguracji (API_KEY, URL) | US-201                 | api_reference.md#weather-config         |
|    GET | /api/simple_weather     | JSON | Bieżąca pogoda dla Warszawy          | US-201                 | api_reference.md#weather-simple         |
|    GET | /api/forecast           | JSON | 3-dniowa prognoza                    | US-202                 | api_reference.md#weather-forecast       |
|    GET | /api/history/<username> | JSON | Historia wyszukiwań                  | US-204                 | api_reference.md#weather-history        |
|   POST | /api/history/<username> | JSON | Dodanie miasta do historii           | US-201, US-204         | api_reference.md#weather-history-add    |
| DELETE | /api/history/<username> | JSON | Usunięcie historii użytkownika       | US-205                 | api_reference.md#weather-history-delete |


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
**TU UZUPEŁNIĆ:** co testujecie jednostkowo (np. funkcje services, walidacja).

### 10.2 Integration tests (HTML/API)
**TU UZUPEŁNIĆ:** które endpointy są testowane integracyjnie.

### 10.3 Acceptance tests (Playwright)
Wymaganie: **min. 1 test Playwright na każde User Story modułu**.

**TU UZUPEŁNIĆ:** lista testów akceptacyjnych + mapowanie do US.

---

## 11. Ograniczenia, ryzyka, dalszy rozwój

zależność od zewnętrznego API,

brak cache po stronie backendu,

możliwość rozbudowy o alerty push i zapisy ulubionych miast.
