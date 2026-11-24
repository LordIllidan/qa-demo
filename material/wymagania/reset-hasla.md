# Reset hasła

- Identyfikator: REQ-RESET
- Autor: właścicielka produktu
- Stan: przyjęte do realizacji

## Historyjka

Jako użytkownik, który nie pamięta hasła, chcę ustawić nowe hasło przez link wysłany na mój adres e-mail, żeby odzyskać dostęp do konta.

## Kryteria akceptacji

- R1. Użytkownik podaje adres e-mail i prosi o reset hasła. Jeśli istnieje konto z tym adresem, system wysyła na ten adres wiadomość z linkiem resetu.
- R2. Odpowiedź systemu na prośbę o reset jest taka sama, gdy konto istnieje i gdy nie istnieje.
- R3. Link resetu zawiera token. Użytkownik, który otworzy link, ustawia nowe hasło.
- R4. Link resetu działa jeden raz. Ten sam link użyty ponownie jest odrzucany, a hasło się nie zmienia.
- R5. Żądanie ustawienia hasła bez tokenu albo z tokenem, którego system nie wydał, jest odrzucane.
- R6. Po ustawieniu nowego hasła użytkownik loguje się nowym hasłem. Stare hasło przestaje działać.
- R7. Po ustawieniu nowego hasła wszystkie wcześniej otwarte sesje użytkownika przestają działać.

## Interfejs

| Operacja | Żądanie | Odpowiedź |
| --- | --- | --- |
| Prośba o reset | `POST /reset/zamow`, pole `email` | 202 |
| Ustawienie hasła | `POST /reset/potwierdz`, pola `token` i `haslo` | 200 po ustawieniu hasła; 410, gdy link był już użyty (R4); 400, gdy tokenu brak albo system go nie wydał (R5) |
| Logowanie | `POST /logowanie`, pola `email` i `haslo` | 200 i identyfikator sesji; 401 przy błędnych danych |
| Dane konta | `GET /konto`, nagłówek `Authorization: Bearer <sesja>` | 200; 401 bez działającej sesji |
