# Aplikacja demonstracyjna

Prosta aplikacja HTTP z jedną funkcją: resetem hasła. Działa w trzech buildach, a port wyznacza build. Kod: `app/serwer.py`, sama biblioteka standardowa Pythona.

## Buildy

| Port | Numer builda | Rola w pokazie |
| --- | --- | --- |
| 8765 | 1.4.0 | wcześniejszy build, używany jako odniesienie |
| 8766 | 1.5.0 | nowszy build |
| 8767 | 1.5.1 | build dostarczony do ponownego testu po zgłoszeniu `material/zgloszenia/ZGL-101.md` (zagadnienie P2) |

Każdy build ma własne konta, tokeny i sesje. Dane żyją w pamięci i znikają po zatrzymaniu aplikacji.

Wszystkie buildy to ta sama aplikacja z resetem hasła opisanym w wymaganiu `material/wymagania/reset-hasla.md`. Czym się od siebie różnią, ma w pokazie ustalić model na podstawie wejścia, dlatego ten dokument tego nie opisuje. Opis różnic dla prowadzącego leży w pliku `prowadzacy/odpowiedzi-pokazu.md`.

## Uruchomienie

Wszystkie buildy w jednym oknie PowerShell:

```powershell
python app/serwer.py
```

Jeden build:

```powershell
python app/serwer.py --port 8766
```

Aplikacja zajmuje okno do zatrzymania przez Ctrl+C, więc skrypty z katalogu `narzedzia` uruchamia się w drugim oknie. Każde żądanie zostawia w oknie aplikacji jeden wiersz z portem i numerem builda.

## Adresy

Adresy z wymagania:

| Adres | Pola | Odpowiedź |
| --- | --- | --- |
| `POST /reset/zamow` | `email` | 202, zawsze ten sam komunikat |
| `POST /reset/potwierdz` | `token`, `haslo` | 200 po ustawieniu hasła; 410, gdy link był już użyty; 400, gdy tokenu brak albo system go nie wydał |
| `POST /logowanie` | `email`, `haslo` | 200 i pole `sesja`; 401 przy błędnych danych |
| `GET /konto` | nagłówek `Authorization: Bearer <sesja>` | 200 i adres e-mail; 401 bez działającej sesji |

Adresy pomocnicze środowiska testowego (nie są częścią wymagania):

| Adres | Do czego służy |
| --- | --- |
| `GET /stan` | podaje numer builda i port |
| `POST /test/konto` z polami `email` i `haslo` | zakłada konto; odpowiedź 201 |
| `GET /test/skrzynka?email=<adres>` | podaje ostatnią dostarczoną wiadomość: nadawca, odbiorca, temat, treść, link i token; 404, gdy wiadomości jeszcze nie ma |
| `GET /` | strona „Nie pamiętam hasła”; formularz woła `POST /reset/zamow` |
| `GET /reset?token=<token>` | strona „Ustaw nowe hasło”; formularz woła `POST /reset/potwierdz` |
| `GET /test/potwierdzenie.pdf` | prosty PDF z potwierdzeniem zmiany hasła; tekst wyciąga `narzedzia/pdf.py` |

Po starcie w każdym buildzie istnieje konto `anna@example.com` z hasłem `StareHaslo-1`.

Wiadomość z linkiem trafia do skrzynki z opóźnieniem, tak jak w systemie, w którym pocztę wysyła osobna usługa. Dopóki wiadomość jest w drodze, skrzynka odpowiada 404 z polem `w_drodze`.

## Czego aplikacja nie robi

- Nie ma historyjki z filtrem zamówień. Ta historyjka istnieje tylko jako tekst wymagania.
- Nie ma ścieżek `orders` i `search`. Liczby dla nich leżą w gotowych plikach, patrz `docs/material.md`.
- Zachowania, o których wymaganie milczy, nie są w aplikacji wzorcem. To, co build robi w takim miejscu, nie jest oczekiwanym wynikiem.
