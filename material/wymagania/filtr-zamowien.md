# Filtr listy zamówień

- Identyfikator: REQ-FILTR
- Autor: właścicielka produktu
- Stan: przyjęte do realizacji

## Historyjka

Jako zalogowany klient chcę filtrować listę swoich zamówień po statusie i dacie złożenia, żeby szybko znaleźć zamówienie, o które pytam.

## Kryteria akceptacji

- F1. Lista zamówień pokazuje zamówienia zalogowanego klienta, od najnowszego.
- F2. Klient zawęża listę statusem: nowe, opłacone, wysłane, anulowane. Może wybrać kilka statusów naraz.
- F3. Klient zawęża listę zakresem dat złożenia zamówienia: od i do, obie daty włącznie.
- F4. Filtry statusu i daty działają łącznie. Lista pokazuje zamówienia, które spełniają oba warunki.
- F5. Gdy żadne zamówienie nie spełnia filtrów, lista jest pusta i widać komunikat „Brak zamówień dla wybranych filtrów”.
- F6. Klient widzi wyłącznie własne zamówienia.
- F7. Konsultant biura obsługi otwiera listę zamówień wskazanego klienta i używa tych samych filtrów.
- F8. Przefiltrowaną listę można pobrać jako plik CSV.

## Role

| Rola | Opis |
| --- | --- |
| Klient | zalogowany użytkownik sklepu; składa i przegląda zamówienia |
| Konsultant | pracownik biura obsługi; rola tylko do odczytu |

## Interfejs

| Operacja | Żądanie | Odpowiedź |
| --- | --- | --- |
| Lista zamówień | `GET /zamowienia`, parametry `status`, `od`, `do`, `klient`; nagłówek `Authorization: Bearer <sesja>` | 200 i lista zamówień |
| Pobranie pliku CSV | `GET /zamowienia.csv` z tymi samymi parametrami i nagłówkiem | 200 i plik CSV |
