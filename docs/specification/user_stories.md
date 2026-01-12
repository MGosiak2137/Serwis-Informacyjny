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

### US-HOME-003
**Jako** zalogowany użytkownik  
**Chcę** po kliknięciu w kartkę z kalendarza na stronie głównej móc zobaczyć tygodniowy horoskop  
**Aby** poznać prognozę astrologiczną na najbliższy tydzień

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
**Chcę** móc założyć konto oraz otrzymać e-mail z potwierdzeniem jego utworzenia  
**Aby** móc korzystać z aplikacji i otrzymać potwierdzenie rejestracji

**Uwaga:** Funkcjonalność wysyłania e-maila z potwierdzeniem jest obecnie niezaimplementowana.

### US-AUTH-003
**Jako** zalogowany użytkownik  
**Chcę** móc zachować swoje preferencje  
**Aby** aplikacja zapamiętywała moje ustawienia i wybory

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
