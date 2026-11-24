# Reset hasła

- Identyfikator: REQ-RESET
- Wersja: 2
- Autor: właścicielka produktu
- Stan: przyjęte do realizacji w wydaniu 1.6.0

## Historyjka

Jako użytkownik, który nie pamięta hasła, chcę ustawić nowe hasło przez link wysłany na mój adres e-mail, żeby odzyskać dostęp do konta.

## Kryteria akceptacji

- R1. Użytkownik podaje adres e-mail i prosi o reset hasła. Jeśli istnieje konto z tym adresem, system wysyła na ten adres wiadomość z linkiem resetu.
- R2. Odpowiedź systemu na prośbę o reset jest taka sama, gdy konto istnieje i gdy nie istnieje.
- R3. Link resetu zawiera token. Użytkownik, który otworzy link, ustawia nowe hasło.
- R4. Link resetu działa jeden raz i przez 30 minut od wysłania wiadomości. Link użyty ponownie albo po tym czasie jest odrzucany, a hasło się nie zmienia.
- R5. Żądanie ustawienia hasła bez tokenu albo z tokenem, którego system nie wydał, jest odrzucane.
- R6. Po ustawieniu nowego hasła użytkownik loguje się nowym hasłem. Stare hasło przestaje działać.
- R7. Po ustawieniu nowego hasła wszystkie wcześniej otwarte sesje użytkownika przestają działać.
- R8. Nowa prośba o reset unieważnia linki wysłane wcześniej na ten sam adres.
- R9. Nowe hasło ma co najmniej 12 znaków. Krótsze hasło jest odrzucane, a hasło się nie zmienia.

## Interfejs

| Operacja | Żądanie | Odpowiedź |
| --- | --- | --- |
| Prośba o reset | `POST /reset/zamow`, pole `email` | 202 |
| Ustawienie hasła | `POST /reset/potwierdz`, pola `token` i `haslo` | 200 po ustawieniu hasła; 410, gdy link był już użyty albo minął jego czas (R4); 400, gdy tokenu brak albo system go nie wydał (R5); 422, gdy nowe hasło jest krótsze niż 12 znaków (R9) |
| Logowanie | `POST /logowanie`, pola `email` i `haslo` | 200 i identyfikator sesji; 401 przy błędnych danych |
| Dane konta | `GET /konto`, nagłówek `Authorization: Bearer <sesja>` | 200; 401 bez działającej sesji |
