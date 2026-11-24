# Testy

Testy automatyczne resetu hasła w pytest. Rozmawiają z aplikacją demonstracyjną przez HTTP i nie zależą od tego, co zostało po poprzednim przebiegu: każdy test zakłada własne konto.

## Pliki

| Plik | Zawartość |
| --- | --- |
| `testy/test_reset_hasla.py` | pięć testów resetu hasła; domyślny zestaw skryptu `przebieg.py` |
| `testy/test_wiadomosc_resetu.py` | jeden test wiadomości z linkiem; poza domyślnym zestawem skryptu `przebieg.py` |
| `testy/conftest.py` | klient aplikacji, opcje `--port` i `--wynik-json`, zapis przebiegu |
| `pytest.ini` | wskazuje katalog `testy` |

## Dwa testy z pokazu

| Test | Nazwa w pokazie |
| --- | --- |
| `test_link_dziala_jeden_raz` | „link działa jeden raz” |
| `test_wystarczy_kod_200` | „wystarczy kod 200” |

Na tych dwóch testach pracują zagadnienia 3 i P6. Kod obu testów i ich wyniki na dwóch buildach podaje skrypt `tabela_asercji.py`. Co każdy z nich sprawdza i jak wypada na buildach, ma w pokazie ustalić model, dlatego ten dokument tego nie opisuje.

Pozostałe testy z pliku `test_reset_hasla.py`: `test_nowe_haslo_loguje_stare_nie`, `test_nieznany_token_jest_odrzucany`, `test_stan_zwraca_numer_builda`. Powiązanie testów ze zdaniami wymagania jest zadaniem modelu w zagadnieniu P4.

## Test wiadomości z linkiem

`test_wiadomosc_z_linkiem_jest_w_skrzynce` leży w osobnym pliku `testy/test_wiadomosc_resetu.py`. Nie wchodzi do domyślnego zestawu skryptu `przebieg.py`. Wchodzi do domyślnego zestawu skryptu `historia.py`, który uruchamia cały katalog `testy`.

## Odpowiedzi dla prowadzącego

Wyniki testów na buildach i opis tego, co z nich wynika, leżą w pliku `prowadzacy/odpowiedzi-pokazu.md`. Modele pracujące w repozytorium tego pliku nie czytają, patrz `docs/plik-prowadzacego.md`.

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

Polecenie `python -m pytest` bez wskazania pliku uruchamia cały katalog `testy`, czyli oba pliki z testami.

## Zapis przebiegu

Opcja `--wynik-json` zapisuje dla każdego testu: nazwę, plik, opis (docstring), wynik, czas, komunikat, miejsce zatrzymania oraz wymianę żądań i odpowiedzi z aplikacją. Odczyt skrzynki ponawiany w oczekiwaniu na wiadomość trafia do zapisu jako jeden wpis z liczbą odczytów. Opis formatu: `docs/format-wejscia.md`.
