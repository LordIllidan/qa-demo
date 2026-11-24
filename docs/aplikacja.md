# Aplikacja demonstracyjna

Prosta aplikacja HTTP z jedną funkcją: resetem hasła. Działa w trzech buildach, a port wyznacza build. Kod: `app/serwer.py`, sama biblioteka standardowa Pythona.

## Buildy

| Port | Numer builda | Zachowanie |
| --- | --- | --- |
| 8765 | 1.4.0 | zgodne z wymaganiem `material/wymagania/reset-hasla.md` |
| 8766 | 1.5.0 | defekt: link resetu działa drugi raz |
| 8767 | 1.5.1 | build z poprawką: link resetu znowu działa jeden raz |

Każdy build ma własne konta, tokeny i sesje. Dane żyją w pamięci i znikają po zatrzymaniu aplikacji.

### Build z poprawką (zagadnienie P2)

Wybrany wariant: trzeci build na porcie 8767. To ten sam kod aplikacji z numerem builda 1.5.1 i z włączonym jednorazowym użyciem linku. Wariant jest najprostszy, bo nie wymaga drugiej kopii kodu, a ponowny test dostaje build o innym numerze niż build ze zgłoszenia. Odrzucony wariant to ponowne użycie portu 8765: model porównywałby wtedy zgłoszenie z buildem odniesienia, a nie z buildem po poprawce.

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
| `GET /test/skrzynka?email=<adres>` | podaje ostatnią dostarczoną wiadomość z linkiem resetu i tokenem; 404, gdy wiadomości jeszcze nie ma |

Po starcie w każdym buildzie istnieje konto `anna@example.com` z hasłem `StareHaslo-1`.

Wiadomość z linkiem trafia do skrzynki z losowym opóźnieniem do 120 ms, tak jak w systemie, w którym pocztę wysyła osobna usługa. Dopóki wiadomość jest w drodze, skrzynka odpowiada 404 z polem `w_drodze`.

## Czego aplikacja nie robi

- Nie ma historyjki z filtrem zamówień. Ta historyjka istnieje tylko jako tekst wymagania.
- Nie ma ścieżek `orders` i `search`. Liczby dla nich leżą w gotowych plikach, patrz `docs/material.md`.
- Zachowania, o których wymaganie milczy, nie są w aplikacji wzorcem. To, co build robi w takim miejscu, nie jest oczekiwanym wynikiem.

## Defekt ręcznie, w PowerShell

Przykład pokazuje różnicę między buildami bez uruchamiania testów. Na porcie 8766 ostatnie polecenie zwraca komunikat o zmianie hasła. Na porcie 8765 to samo polecenie kończy się błędem z kodem 410.

```powershell
$adres = "http://127.0.0.1:8766"
$konto = @{ email = "anna@example.com" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$adres/reset/zamow" -ContentType "application/json" -Body $konto
Start-Sleep -Milliseconds 300
$token = (Invoke-RestMethod -Uri "$adres/test/skrzynka?email=anna@example.com").token
$pierwsze = @{ token = $token; haslo = "NoweHaslo-1" } | ConvertTo-Json
$drugie = @{ token = $token; haslo = "InneHaslo-2" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$adres/reset/potwierdz" -ContentType "application/json" -Body $pierwsze
Invoke-RestMethod -Method Post -Uri "$adres/reset/potwierdz" -ContentType "application/json" -Body $drugie
```
