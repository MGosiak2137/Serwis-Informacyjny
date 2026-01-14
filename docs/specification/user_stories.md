# User Stories

> **Cel dokumentu:**  
> Ten dokument zawiera listę User Stories dla projektu Serwis Informacyjny NEWC.  
> User Stories zostały pogrupowane według modułów aplikacji.

---

## Moduł: Strona główna (Home)

### US-HOME-001
**Jako** użytkownik  
**Chcę** zobaczyć stronę główną aplikacji, która umożliwia wybór modułu i przejście do podstrony modułu  
**Aby** móc łatwo nawigować po aplikacji i uzyskać dostęp do różnych funkcjonalności

### US-HOME-002
**Jako** użytkownik  
**Chcę** na stronie głównej zobaczyć w formie graficznej aktualną datę, imieniny, numerację dnia roku oraz informację, czy ten dzień jest wolny od pracy, czy nie  
**Aby** mieć szybki dostęp do podstawowych informacji kalendarzowych

---

## Moduł: Kalendarz (Calendar)

### US-CAL-001
**Jako** zalogowany użytkownik  
**Chcę** po kliknięciu w kartkę z kalendarza na stronie głównej móc zobaczyć tygodniowy horoskop  
**Aby** poznać prognozę astrologiczną na najbliższy tydzień

---

## Moduł: Logowanie (Authentication)

### US-AUTH-001
**Jako** użytkownik niezalogowany  
**Chcę** móc zalogować się na istniejące już konto  
**Aby** uzyskać dostęp do funkcjonalności wymagających autoryzacji

### US-AUTH-002
**Jako** użytkownik nieposiadający konta w aplikacji  
**Chcę** móc założyć konto
**Aby** móc korzystać z aplikacji

**Uwaga:** Funkcjonalność wysyłania e-maila z potwierdzeniem jest obecnie niezaimplementowana.

### US-AUTH-003
**Jako** zalogowany użytkownik  
**Chcę** móc zachować swoje preferencje  
**Aby** aplikacja zapamiętywała moje ustawienia i wybory

---

## Moduł: Ekonomia (Economy)

### US-ECO-001
**Jako** użytkownik niezalogowany  
**Chcę** dowiedzieć się kursu euro, dolara i franka szwajcarskiego  
**Aby** mieć dostęp do podstawowych informacji o kursach walut bez konieczności rejestracji

### US-ECO-002
**Jako** zalogowany użytkownik  
**Chcę** sprawdzić historyczne dane cenowe dotyczące walut, indeksów akcyjnych oraz surowców naturalnych  
**Aby** analizować trendy i zmiany cen w czasie

### US-ECO-003
**Jako** zalogowany użytkownik  
**Chcę** sprawdzić, jaka jest prawdopodobna cena mojej podróży do wybranego miejsca wyjazdu (koszty dojazdu oraz miejsca zamieszkania)  
**Aby** zaplanować budżet podróży

### US-ECO-004
**Jako** zalogowany użytkownik  
**Chcę** sprawdzić kursy różnych walut oraz możliwość przeliczania walut  
**Aby** móc konwertować kwoty między różnymi walutami

### US-ECO-005
**Jako** zalogowany użytkownik  
**Chcę** na stronie głównej w okienku ekonomicznym widzieć 3 wybrane przeze mnie kursy waluty, ceny akcji lub surowców  
**Aby** mieć szybki dostęp do najważniejszych dla mnie informacji ekonomicznych

### US-ECO-006
**Jako** zalogowany użytkownik  
**Chcę** po przejściu do modułu ekonomicznego mieć możliwość grupowania w zakładki wybrane przeze mnie pozycje walutowe, akcyjne i surowcowe  
**Aby** lepiej organizować i szybciej znajdować interesujące mnie dane ekonomiczne

---

## Moduł: Backend i infrastruktura

### US-DEV-001
**Jako** deweloper  
**Chcę** stworzyć logiczne zaplecze strony poprzez utworzenie podstawowego backendu we Flasku oraz ścieżek dla podstron  
**Aby** zapewnić spójną strukturę aplikacji i umożliwić routing między różnymi modułami

### US-DEV-002
**Jako** deweloper  
**Chcę** mieć bazę danych, umożliwiającą dodawanie nowych tabel dla poszczególnych modułów oraz połączenie jej z istniejącym backendem  
**Aby** móc elastycznie rozszerzać funkcjonalność aplikacji bez konieczności przebudowy struktury danych

---

## Uwagi

- User Stories zostały pogrupowane według modułów aplikacji
- Każda User Story jest opatrzona unikalnym identyfikatorem (format: `US-MODULE-XXX`)
- User Stories techniczne (dla deweloperów) zostały wyodrębnione do osobnej sekcji
- Niektóre funkcjonalności wymienione w User Stories mogą być częściowo lub w pełni niezaimplementowane (zaznaczono w uwagach)

---

## Powiązanie z testami

Każda User Story powinna mieć co najmniej jeden test akceptacyjny (E2E) przypisany do niej.
Szczegóły dotyczące testowania znajdują się w dokumentacji: [`docs/testing.md`](../testing.md)
