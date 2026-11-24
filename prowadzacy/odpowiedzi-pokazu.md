# Odpowiedzi pokazu

Plik dla osoby, która prowadzi pokaz. Zbiera w jednym miejscu to, co model ma w pokazie ustalić sam: który build zachowuje się inaczej i jak, który test tego nie wykrywa, który test ma zmienny wynik.

Modele pracujące w repozytorium tego katalogu nie czytają. Zakaz stoi w zasadach wspólnych każdego skilla. Opis: `docs/plik-prowadzacego.md`.

## Buildy

| Port | Numer builda | Zachowanie |
| --- | --- | --- |
| 8765 | 1.4.0 | zgodne z wymaganiem `material/wymagania/reset-hasla.md` |
| 8766 | 1.5.0 | defekt: link resetu działa drugi raz |
| 8767 | 1.5.1 | build z poprawką: link resetu znowu działa jeden raz |

### Build z poprawką (zagadnienie P2)

Wybrany wariant: trzeci build na porcie 8767. To ten sam kod aplikacji z numerem builda 1.5.1 i z włączonym jednorazowym użyciem linku. Wariant jest najprostszy, bo nie wymaga drugiej kopii kodu, a ponowny test dostaje build o innym numerze niż build ze zgłoszenia. Odrzucony wariant to ponowne użycie portu 8765: model porównywałby wtedy zgłoszenie z buildem odniesienia, a nie z buildem po poprawce.

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

## Wynik domyślnego zestawu na buildach (zagadnienia 2 i P2)

Polecenie `python narzedzia/przebieg.py --port <port>`:

| Build | Wynik domyślnego zestawu |
| --- | --- |
| 8765 (1.4.0) | pięć testów zaliczonych |
| 8766 (1.5.0) | `test_link_dziala_jeden_raz` niezaliczony, pozostałe cztery zaliczone, w tym `test_wystarczy_kod_200` |
| 8767 (1.5.1) | pięć testów zaliczonych |

## Dwa testy z pokazu (zagadnienie 3)

| Test | Co sprawdza | Build 8765 | Build 8766 |
| --- | --- | --- | --- |
| `test_link_dziala_jeden_raz` („link działa jeden raz”) | pierwsze użycie linku daje 200, drugie 410, po drugim użyciu obowiązuje hasło z pierwszego | zielony | czerwony |
| `test_wystarczy_kod_200` („wystarczy kod 200”) | ustawienie hasła przez link daje 200 | zielony | zielony |

Pierwszy test odróżnia build zgodny z wymaganiem od builda z defektem. Drugi przechodzi na obu, więc defektu nie wykrywa. Na tej różnicy stoi zagadnienie 3.

Tabela, którą skrypt `tabela_asercji.py` podaje dla ustawień domyślnych:

| test | build 1.4.0 (port 8765) | build 1.5.0 (port 8766) |
| --- | --- | --- |
| test_link_dziala_jeden_raz | zaliczony | niezaliczony |
| test_wystarczy_kod_200 | zaliczony | zaliczony |

## Zestaw testów a wymaganie (zagadnienie P4)

Zestaw w pliku `testy/test_reset_hasla.py` celowo nie pokrywa wszystkich zdań wymagania i zawiera test bez zdania w wymaganiu. To materiał dla zagadnienia P4.

## Test o zmiennym wyniku (zagadnienie P3)

Test o zmiennym wyniku leży w pliku `testy/test_wiadomosc_resetu.py`.

`test_wiadomosc_z_linkiem_jest_w_skrzynce` prosi o reset, czeka stałe 60 ms i raz czyta skrzynkę. Aplikacja dostarcza wiadomość z losowym opóźnieniem do 120 ms, więc na tym samym buildzie test raz przechodzi, a raz nie. Leży w osobnym pliku, żeby domyślny przebieg na porcie 8765 był zawsze zielony. Do historii przebiegów służy skrypt `historia.py`.

Nazwa pliku i treść testu nie zdradzają, że wynik jest zmienny. Wskazać to ma model na podstawie historii. Wynik tego testu jest losowy, więc dwie historie różnią się od siebie.

## Dane pod regułę (zagadnienie 7)

`material/dane/dane-resetu.json` to przykładowy plik danych dla przebiegu: pierwszy link, ten sam link drugi raz, pusty token.

## Lista sprawdzeń (zagadnienie 4)

Suma czasów dziesięciu sprawdzeń przekracza okno 40 minut.

## Liczby dwóch buildów (zagadnienie 5)

| Ścieżka | p95 na buildzie 1.4.0 | p95 na buildzie 1.5.0 | Próg p95 |
| --- | --- | --- | --- |
| orders | 42,1 ms | 702,3 ms | poniżej 500 ms |
| search | 118,4 ms | 118,9 ms | poniżej 300 ms |

Profil w obu plikach jest ten sam: 20 użytkowników, narastanie 30 s, czas trwania 300 s, przerwa między żądaniami 1 s.

## Nocny przebieg (zagadnienie P1)

W pliku `material/przebieg-nocny/wynik-8766.json` jest dziesięć testów na buildzie 1.5.0, w tym sześć z wynikiem innym niż zaliczony.

## Zgłoszenie ZGL-101 (zagadnienia 2 i P2)

`material/zgloszenia/ZGL-101.md` to zgłoszenie defektu „link resetu działa drugi raz” w kształcie, jaki powstaje w zagadnieniu 2 po decyzji człowieka.

## Zagadnienia rozszerzające (R1–R5)

Odpowiedzi wyprowadzone z materiału ręcznie. Skilli i agentów dla tych zagadnień nie uruchomiono w GitHub Copilot, więc to, co odda model, może się różnić układem.

### R1. Przypadki testowe techniką

Czego się spodziewać dla wymagania `reset-hasla`:

- R4 nadaje się do przejść stanów. Wymaganie podaje dwa stany linku: wydany i użyty. Przejście „wydany → użyty” daje 200, a ponowne użycie daje 410 i hasło się nie zmienia. Wymaganie nie opisuje linku, którego czas minął, ani starszego linku po użyciu nowszego. W tych miejscach powinno stać pytanie do autora, a nie oczekiwany wynik.
- R5 nadaje się do klas równoważności: brak tokenu, token, którego system nie wydał, token wydany. Dla dwóch pierwszych wymaganie podaje 400.
- R2 daje dwie klasy adresu: z kontem i bez konta, z tą samą odpowiedzią 202. O adresie niepoprawnym składniowo i o wielkości liter wymaganie milczy.
- R6 i R7 to skutki po ustawieniu hasła. Nie mają granic ani kombinacji, więc wystarcza po jednym przypadku.

Dla wymagania `filtr-zamowien`:

- F3 nadaje się do wartości brzegowych: zamówienie z dnia „od”, z dnia „do”, z dnia przed „od” i z dnia po „do”. O sytuacji, w której „od” jest późniejsze niż „do”, i o podaniu tylko jednej daty wymaganie milczy.
- F2 i F4 nadają się do tablicy decyzyjnej: status spełniony albo nie, data spełniona albo nie, cztery kombinacje, lista pokazuje zamówienie tylko w jednej.
- F2: cztery statusy to cztery klasy, do tego wybór kilku naraz. O braku wybranego statusu i o statusie spoza listy wymaganie milczy.

Dobry wynik ma mało przypadków, a przy każdym element modelu. Zły wynik to kilkadziesiąt przypadków z tej samej klasy albo oczekiwany wynik wpisany tam, gdzie wymaganie milczy.

### R2. Zgłoszenie z obserwacji ręcznej

Notatki z sesji mają kilka obserwacji o różnym charakterze:

| Zapis | Co z niego wynika |
| --- | --- |
| 10:09, ten sam link drugi raz, odpowiedź 200 i zmienione hasło | sprzeczne z R4; to samo zachowanie opisuje otwarte zgłoszenie ZGL-101, na tym samym buildzie, z tymi samymi hasłami |
| 10:13, starszy link działa po użyciu nowszego | wymaganie tego nie określa; pytanie do autora, a nie defekt |
| 10:13, hasło z jednego znaku przyjęte | wymaganie nie ma reguł hasła; pytanie do autora |
| 10:07, sesja sprzed resetu odpowiada 401 | zgodne z R7; to nie jest obserwacja do zgłoszenia |
| 10:21, adres bez konta dostaje 202 i ten sam komunikat | zgodne z R2 |
| 10:24, adres wielkimi literami, skrzynka niesprawdzona | obserwacja niedokończona; brakuje wyniku, żeby cokolwiek zgłaszać |

Dla zapisu z 10:09 model powinien wskazać ZGL-101 jako możliwe powtórzenie i zostawić rozstrzygnięcie człowiekowi. ZGL-097 dotyczy stopki wiadomości i nie ma związku z żadną obserwacją. Kroki zgłoszenia mają pochodzić z zapisów 10:03, 10:06 i 10:09. Notatki nie mówią, czy obserwację powtórzono, ani jak te same kroki kończą się na buildzie 1.4.0; porównanie z tym buildem tester sam wpisał do części „Nie zdążyłam”. Model powinien to podać jako braki, a nie przepisać porównanie z ZGL-101 jako własną obserwację testera.

### R3. Kandydaci do automatyzacji

| Sprawdzenie | Test automatyczny | Stan |
| --- | --- | --- |
| S1 (5 min) | `test_wystarczy_kod_200` sprawdza tylko kod odpowiedzi; skutek, czyli logowanie nowym hasłem, sprawdza `test_nowe_haslo_loguje_stare_nie` | w całości, ale dopiero dwoma testami razem; sam `test_wystarczy_kod_200` to pokrycie częściowe |
| S2 (5 min) | `test_link_dziala_jeden_raz` | w całości |
| S3 (4 min) | `test_nieznany_token_jest_odrzucany` | częściowo: nie ma żądania bez tokenu |
| S4 (4 min) | `test_wiadomosc_z_linkiem_jest_w_skrzynce` | częściowo: nie ma adresu bez konta ani porównania odpowiedzi |
| S5 (5 min) | `test_nowe_haslo_loguje_stare_nie` | w całości |
| S6 (4 min) | brak osobnego testu; logowanie występuje tylko jako krok po resecie | brak |
| S7–S10 (8, 6, 7, 6 min) | brak | brak |

Czas ręczny: sprawdzenia z pełnym testem (S1, S2, S5) to 15 minut, z częściowym (S3, S4) 8 minut, bez testu (S6–S10) 31 minut, razem 54 minuty. `test_stan_zwraca_numer_builda` nie odpowiada żadnemu sprawdzeniu z listy. Wejście nie mówi, jak często wykonuje się listę, jak często zmieniają się obszary ani ile kosztuje napisanie testu, więc model nie ma z czego wyliczyć opłacalności.

### R4. Szkic testu automatycznego

Przykładowy przypadek do potwierdzenia przez prowadzącego: „Odpowiedź na prośbę o reset jest taka sama dla adresu z kontem i dla adresu bez konta: kod 202 i ta sama treść” (R2 i tabela interfejsu). Takiego testu w zestawie nie ma. Wspólne zaplecze ma potrzebny krok, `popros_o_reset`, więc zmiana zaplecza nie jest potrzebna.

Test napisany z tych kroków jest zielony na wszystkich trzech buildach (8765, 8766, 8767): każdy odpowiada kodem 202 i tym samym komunikatem. Sprawdzono to 24.11.2026 plikiem tymczasowym, którego w repozytorium nie ma.

Test nie sprawdza czasu odpowiedzi ani tego, czy dla adresu bez konta nie powstaje wiadomość. Model powinien to napisać w części „Czego ten test nie sprawdza”.

Drugi przykład, na którym widać zakaz: jeśli poprosić o test dla starszego linku po użyciu nowszego, wymaganie nie podaje oczekiwanego wyniku. Model ma zapytać, a nie uruchomić kroki i wpisać do asercji 200, które build zwraca.

### R5. Testy niefunkcjonalne

Wymaganie `reset-hasla`:

- Bezpieczeństwo ma zdania: R2, R4, R5, R7. Milczy o czasie ważności linku, liczbie próśb w krótkim czasie i regułach hasła.
- Wydajność, niezawodność, zgodność: nic. Na przykład nie ma czasu dostarczenia wiadomości ani zachowania, gdy wysyłka się nie powiedzie.
- Użyteczność i dostępność: wymaganie opisuje interfejs programistyczny, bez ekranu. Model powinien napisać, że z tekstu nie da się tego ocenić, i zapytać o ekran ustawienia hasła oraz treść wiadomości.
- Bezpieczeństwo użytkowania: bez zastosowania.

Wymaganie `filtr-zamowien`:

- Użyteczność: F5 podaje treść komunikatu. O obsłudze klawiaturą, czytniku ekranu i kontraście nic.
- Zgodność: F8 mówi o pliku CSV, ale nie o kodowaniu, separatorze ani formacie daty.
- Wydajność: nic o liczbie zamówień, stronicowaniu ani czasie odpowiedzi.
- Bezpieczeństwo: F6 i F7 oraz rola tylko do odczytu; szczegóły należą do zagadnienia 8.

Zły wynik to próg wpisany jak wymaganie, na przykład „odpowiedź poniżej 2 sekund” albo „zgodność z WCAG 2.1 AA”, bez etykiety „reguła własna modelu” i bez pytania do autora.

## Przykład zapisu przebiegu

Zapis w formacie `qa-demo/przebieg/1` z builda 8766, z testem, który zatrzymał się na asercji:

```json
{
  "format": "qa-demo/przebieg/1",
  "pochodzenie": "uruchomienie",
  "build": {"port": 8766, "numer": "1.5.0"},
  "zestaw": "testy/test_reset_hasla.py",
  "start": "2026-11-24T19:40:02+01:00",
  "podsumowanie": {"liczba_testow": 5, "zaliczony": 4, "niezaliczony": 1, "pominięty": 0, "błąd": 0},
  "testy": [
    {
      "nazwa": "test_link_dziala_jeden_raz",
      "plik": "testy/test_reset_hasla.py",
      "opis": "<docstring testu>",
      "wynik": "niezaliczony",
      "czas_ms": 118,
      "komunikat": "AssertionError: assert 200 == 410 ...",
      "miejsce": "testy/test_reset_hasla.py:12",
      "asercja": "assert drugie_uzycie.status == 410",
      "wymiana": [
        {"nr": 1, "zadanie": "POST /test/konto", "dane": {"email": "...", "haslo": "..."}, "status": 201, "odpowiedz": {"email": "..."}}
      ]
    }
  ]
}
```

## Sformułowania z przykładów użytkownika

Skille i `README.md` używają przykładów spoza pokazu, żeby model nie dostał odpowiedzi razem z instrukcją. Oryginalne sformułowania, z których te przykłady powstały:

| Miejsce | Oryginalne sformułowanie |
| --- | --- |
| zasada 6 w zasadach wspólnych skilli i w `README.md` | model opisuje zachowanie systemu: „na tym buildzie link działa drugi raz”, a nie „test padł” |
| skill `zgloszenie-defektu`, tytuł i wynik faktyczny zgłoszenia | „na tym buildzie link działa drugi raz” |
| skill `przeglad-zmiany-w-testach`, skutek zmiany w wynikach | „po tej zmianie test jest zielony na buildzie 8766” |
| skill `ocena-asercji`, dwa buildy | build zgodny z wymaganiem to 8765, build wadliwy to 8766 |
| skill `przeglad-zmiany-w-testach`, dwa buildy | build zgodny z wymaganiem to 8765, build wadliwy to 8766 |
| skill `test-potwierdzajacy`, build do ponownego testu | build z poprawką działa na porcie 8767 |

Polecenie zagadnienia P2 z portem i nazwą testu:

```powershell
python narzedzia/przebieg.py --port 8767 --test test_link_dziala_jeden_raz
```

## Gdzie jeszcze widać odpowiedzi

Zakaz czytania dotyczy tylko katalogu `prowadzacy`. Odpowiedzi widać także w miejscach, których zmienić się nie da bez zmiany pokazu:

- `app/serwer.py`: kod aplikacji, w tym ustawienia każdego builda,
- `material/zgloszenia/ZGL-101.md`: gotowe zgłoszenie, wejście zagadnienia P2,
- `testy`: kod testów.
