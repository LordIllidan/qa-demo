# Testy

Testy automatyczne resetu hasła w pytest. Rozmawiają z aplikacją demonstracyjną przez HTTP i nie zależą od tego, co zostało po poprzednim przebiegu: każdy test zakłada własne konto.

## Pliki

| Plik | Zawartość |
| --- | --- |
| `testy/test_reset_hasla.py` | pięć testów resetu hasła; domyślny zestaw skryptu `przebieg.py` |
| `testy/test_wiadomosc_resetu.py` | jeden test wiadomości z linkiem; ma zmienny wynik (zagadnienie P3) |
| `testy/conftest.py` | klient aplikacji, opcje `--port` i `--wynik-json`, zapis przebiegu |
| `pytest.ini` | wskazuje katalog `testy` |

## Dwa testy z pokazu

| Test | Co sprawdza | Build 8765 | Build 8766 |
| --- | --- | --- | --- |
| `test_link_dziala_jeden_raz` („link działa jeden raz”) | pierwsze użycie linku daje 200, drugie 410, po drugim użyciu obowiązuje hasło z pierwszego | zielony | czerwony |
| `test_wystarczy_kod_200` („wystarczy kod 200”) | ustawienie hasła przez link daje 200 | zielony | zielony |

Pierwszy test odróżnia build zgodny z wymaganiem od builda z defektem. Drugi przechodzi na obu, więc defektu nie wykrywa. Na tej różnicy stoi zagadnienie 3.

Pozostałe testy z pliku `test_reset_hasla.py`: `test_nowe_haslo_loguje_stare_nie`, `test_nieznany_token_jest_odrzucany`, `test_stan_zwraca_numer_builda`. Zestaw celowo nie pokrywa wszystkich zdań wymagania i zawiera test bez zdania w wymaganiu. To materiał dla zagadnienia P4.

## Test o zmiennym wyniku

`test_wiadomosc_z_linkiem_jest_w_skrzynce` prosi o reset, czeka stałe 60 ms i raz czyta skrzynkę. Aplikacja dostarcza wiadomość z losowym opóźnieniem do 120 ms, więc na tym samym buildzie test raz przechodzi, a raz nie. Leży w osobnym pliku, żeby domyślny przebieg na porcie 8765 był zawsze zielony. Do historii przebiegów służy skrypt `historia.py`.

Nazwa pliku i treść testu nie zdradzają, że wynik jest zmienny. Wskazać to ma model na podstawie historii.

## Uruchamianie

Zalecana droga to skrypty z katalogu `narzedzia`, bo zapisują wynik w stałym formacie:

```powershell
python narzedzia/przebieg.py --port 8765
python narzedzia/przebieg.py --port 8766
```

Bezpośrednio przez pytest, z katalogu głównego repozytorium:

```powershell
python -m pytest testy/test_reset_hasla.py --port 8766
python -m pytest testy/test_reset_hasla.py --port 8766 --wynik-json wyniki/reczny.json
```

Polecenie `python -m pytest` bez wskazania pliku uruchamia cały katalog `testy`, razem z testem o zmiennym wyniku.

## Zapis przebiegu

Opcja `--wynik-json` zapisuje dla każdego testu: nazwę, plik, opis (docstring), wynik, czas, komunikat, miejsce zatrzymania oraz wymianę żądań i odpowiedzi z aplikacją. Odczyt skrzynki ponawiany w oczekiwaniu na wiadomość trafia do zapisu jako jeden wpis z liczbą odczytów. Opis formatu: `docs/format-wejscia.md`.
