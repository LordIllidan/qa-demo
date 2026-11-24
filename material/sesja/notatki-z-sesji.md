# Notatki z sesji eksploracyjnej

- Build: 1.5.0 (port 8766)
- Data: 24.11.2026, 10:00–10:30
- Tester: Ola
- Karta: zbadać reset hasła pod kątem ponownego użycia linków i stanu konta po resecie
- Konto: ola@example.com, założone na czas sesji, hasło startowe StareHaslo-1

## Zapis

10:01 zalogowałam się starym hasłem w pierwszym oknie, /konto odpowiada 200. Zostawiam tę sesję na później.

10:03 poprosiłam o reset i odczytałam link ze skrzynki. Poprosiłam drugi raz, w skrzynce jest nowy, inny link. Mam dwa linki.

10:06 nowszy link, hasło NoweHaslo-1 -> 200 „Hasło zostało zmienione.”

10:07 pierwsze okno, /konto -> 401. Sesja sprzed resetu już nie działa.

10:09 ten sam nowszy link drugi raz, hasło InneHaslo-2 -> znowu 200 „Hasło zostało zmienione.”!
Logowanie InneHaslo-2 -> 200. Logowanie NoweHaslo-1 -> 401. Czyli hasło zmieniło się drugi raz.

10:13 starszy z dwóch linków (ten z pierwszej prośby), hasło „a” -> 200. Logowanie hasłem „a” -> 200.
Nie wiem, czy starszy link ma działać po użyciu nowszego. Hasło z jednego znaku przeszło.

10:17 starszy link, puste hasło -> 400 „Brak nowego hasła.”

10:19 pusty token -> 400.

10:21 prośba o reset dla nikt@example.com (nie ma konta) -> 202, ten sam komunikat co dla konta. Czasu odpowiedzi nie mierzyłam.

10:24 prośba o reset dla OLA@example.com (wielkie litery) -> 202. Skrzynki nie sprawdziłam, bo skończył się czas.

## Nie zdążyłam

- link użyty po dłuższym czasie, na przykład następnego dnia
- wiele próśb o reset w krótkim czasie
- porównanie z buildem 1.4.0
