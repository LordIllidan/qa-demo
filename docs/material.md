# Materiał pokazu

Wspólny materiał wejściowy dla wszystkich zagadnień. Leży w katalogu `material`. Wszystkie dane są syntetyczne: adresy w domenie example.com, hasła wymyślone na potrzeby pokazu.

## Zestawienie

| Plik albo katalog | Co zawiera | Zagadnienia | Podaje go |
| --- | --- | --- | --- |
| `material/wymagania/reset-hasla.md` | wymaganie resetu hasła, zdania R1–R7 i interfejs | 1, 2, 3, 4, 7, 8, P4, P5, P6, R1, R2, R4, R5, R6, R7 | `wymaganie.py reset-hasla` |
| `material/wymagania/filtr-zamowien.md` | historyjka z filtrem listy zamówień, zdania F1–F8 i role | 8, R1, R5, R8 | `wymaganie.py filtr-zamowien` |
| `material/zakres/lista-sprawdzen.json` | zdanie „zmiana w resecie, 40 minut” i lista sprawdzeń z czasami | 4, R3 | `lista_sprawdzen.py` |
| `material/liczby/build-8765.json`, `material/liczby/build-8766.json` | liczby dwóch buildów: profil, progi, ścieżki orders i search | 5, 6 | `liczby.py`, `zbierz_wyniki.py` |
| `material/dane/dane-resetu.json` | przykładowy plik danych dla przebiegu w formacie `qa-demo/dane/1`: lista wejść, każde z oczekiwanym wynikiem i jego źródłem | 7 | `przebieg_danych.py` |
| `material/zgloszenia/ZGL-101.md` | zgłoszenie defektu resetu hasła | P2 | plik czyta model albo człowiek |
| `material/zgloszenia/otwarte.json` | lista otwartych zgłoszeń | 6, R2, R8 | `zbierz_wyniki.py`, `plan_iteracji.py`; w zagadnieniu R2 plik czyta model albo człowiek |
| `material/zakres/zakres-wydania.json` | zakres planowany i wykonany | 6 | `zbierz_wyniki.py` |
| `material/przebieg-nocny/` | zapis nocnego przebiegu z kilkoma awariami, przebieg referencyjny i log | P1 | `przebieg_nocny.py` |
| `material/sesja/ryzyka.md` | lista ryzyk resetu hasła z poziomami ustalonymi przez zespół | P5, R8 | plik czyta model albo człowiek |
| `material/sesja/notatki-z-sesji.md` | notatki testera z sesji eksploracyjnej na buildzie 1.5.0 | P5, R2 | plik czyta model albo człowiek |
| `material/zmiana-w-testach/` | wersja pliku z testami po zmianie i opis zmiany od autora | P6 | `zmiana_w_testach.py` |
| `material/zmiana-wymagania/` | wymaganie resetu hasła w wersji 2 i opis zmiany od autorki | R6, R8 | `zmiana_wymagania.py`, `plan_iteracji.py` |
| `material/interfejs/reset-hasla.json` | opis interfejsu resetu hasła w formacie OpenAPI 3.0, przygotowany przez zespół programistów | R7 | `opis_interfejsu.py` |
| `material/plan/iteracja.json` | dane iteracji: historie, zespół z godzinami, środowisko, ustalenia | R8 | `plan_iteracji.py` |

Materiałem są też dwa buildy aplikacji (`docs/aplikacja.md`) i testy (`docs/testy.md`).

## Wymagania

Oba wymagania są napisane tak, jak pisze się zwykłe historyjki: mówią o głównej drodze użytkownika i nie mówią wszystkiego. Czego w nich brakuje, ma wskazać model, dlatego dokumentacja tego nie wylicza.

Historyjka z filtrem zamówień istnieje tylko jako tekst. Aplikacja demonstracyjna jej nie realizuje, bo zagadnienia 8, R1 i R5 pracują na samym wymaganiu.

## Lista sprawdzeń (zagadnienie 4)

Dziesięć sprawdzeń z czasem wykonania w minutach i zdanie o zmianie z oknem 40 minut. Lista nie ma poziomów ryzyka ani kolejności: ułożenie jej i policzenie, co mieści się w oknie, jest zadaniem modelu.

## Liczby dwóch buildów (zagadnienie 5)

Dwa gotowe pliki wyników, po jednym na build. Każdy zawiera profil obciążenia, progi i metryki ścieżek `orders` oraz `search`. Zestawienie liczb, porównanie profilu i odniesienie do progów jest zadaniem modelu, dlatego ten dokument liczb nie powtarza.

Liczby są przygotowane na potrzeby pokazu. Narzędzia niczego nie mierzą, a aplikacja demonstracyjna nie ma ścieżek `orders` i `search`. Przyjęte założenie: liczby dotyczą tych samych dwóch buildów co porty 8765 i 8766.

## Nocny przebieg (zagadnienie P1)

Trzy pliki w `material/przebieg-nocny`:

- `wynik-8766.json`: dziesięć testów na buildzie 1.5.0, część z wynikiem innym niż zaliczony,
- `wynik-8765.json`: ten sam zestaw na buildzie 1.4.0 jako przebieg referencyjny,
- `log-8766.txt`: log przebiegu z wpisami przebiegu, aplikacji i środowiska.

Pliki wyników mają ten sam format co wynik skryptu `przebieg.py`. Są zapisem przygotowanym ręcznie, a nie wynikiem uruchomienia: pole `pochodzenie` mówi to wprost. Zestaw nocny jest szerszy niż katalog `testy`; testów z pliku `testy_nocne/test_reset_regresja.py` w repozytorium nie ma.

## Sesja eksploracyjna (zagadnienie P5)

Lista ryzyk służy do karty sesji przed sesją. Notatki służą do raportu po sesji. Notatki opisują faktyczne zachowanie builda 1.5.0 i zawierają rzeczy niedokończone oraz wątpliwości testera.

## Zmiana w testach (zagadnienie P6)

`material/zmiana-w-testach/test_reset_hasla.py` to wersja pliku `testy/test_reset_hasla.py` po zmianie zaproponowanej przez autora. `opis-zmiany.md` to opis, który autor dołączył do zmiany. Różnicę wersji i wyniki obu wersji na obu buildach podaje skrypt `zmiana_w_testach.py`.

## Zmiana wymagania (zagadnienia R6 i R8)

`material/zmiana-wymagania/reset-hasla.md` to wymaganie resetu hasła w wersji 2, przyjęte do realizacji w wydaniu 1.6.0. Aplikacja demonstracyjna realizuje wersję 1 z katalogu `material/wymagania`. Skrypt `wymaganie.py` wersji 2 nie podaje; podaje ją `zmiana_wymagania.py` razem z wersją 1. `opis-zmiany.md` to opis, który autorka dołączyła do zmiany.

## Opis interfejsu (zagadnienie R7)

`material/interfejs/reset-hasla.json` to opis czterech operacji resetu hasła w formacie OpenAPI 3.0. Opis przygotował zespół programistów, niezależnie od wymagania. Operacje `/test/...` aplikacji demonstracyjnej nie są w nim opisane, bo służą tylko testom.

## Dane iteracji (zagadnienie R8)

`material/plan/iteracja.json` opisuje iterację przed wydaniem 1.6.0: dwie historie, dwie osoby z godzinami na testy, terminy środowiska i ustalenia zespołu. Format `qa-demo/iteracja/1`. Skrypt `plan_iteracji.py` podaje te dane razem z listą ryzyk, otwartymi zgłoszeniami i treścią historii.

## Zgłoszenia i zakres (zagadnienia 6 i P2)

`ZGL-101.md` to zgłoszenie, od którego zaczyna się ponowny test w zagadnieniu P2. Dotkliwość i priorytet w zgłoszeniach oraz stany w zakresie wydania są wpisane jako decyzje ludzi.

## Odpowiedzi dla prowadzącego

To, co model ma w pokazie ustalić z materiału, jest opisane w pliku `prowadzacy/odpowiedzi-pokazu.md`. Modele pracujące w repozytorium tego pliku nie czytają, patrz `docs/plik-prowadzacego.md`.
