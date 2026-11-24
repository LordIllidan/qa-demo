# O sklepie i słownik pojęć

- Rodzaj: opis produktu dla zespołu
- Właściciel dokumentu: właścicielka produktu
- Aktualizacja: 03.11.2026

## Czym jest sklep

Sklep internetowy, w którym klient zakłada konto, składa zamówienia i przegląda ich historię. Zamówieniami klientów zajmuje się biuro obsługi. Sklep ma interfejs REST, z którego korzystają strona sklepu i aplikacja biura obsługi.

## Konto klienta

Konto klienta jest przypisane do jednego adresu e-mail. Adres e-mail jest loginem. Jeden adres e-mail może mieć tylko jedno konto. Klient loguje się adresem e-mail i hasłem.

## Sesja

Po zalogowaniu klient dostaje identyfikator sesji. Strona sklepu i aplikacja wysyłają go w nagłówku `Authorization: Bearer <sesja>`. Klient może mieć kilka sesji naraz, na przykład w telefonie i w komputerze. Sesja kończy się, gdy klient się wyloguje.

## Słownik

| Pojęcie | Znaczenie |
| --- | --- |
| klient | osoba z kontem w sklepie, która składa i przegląda zamówienia |
| konsultant | pracownik biura obsługi |
| reset hasła | ustawienie nowego hasła przez link wysłany na adres e-mail konta |
| token resetu | ciąg znaków w linku resetu, po którym sklep rozpoznaje prośbę o reset |
| zamówienie | zakup złożony przez klienta, z numerem, datą złożenia i statusem |
| build | wersja aplikacji sklepu oddana do testów |
