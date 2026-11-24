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

## Zagadnienia rozszerzające (R1–R18)

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

### R6. Testy po zmianie wymagania

Opis zmiany od autorki jest niepełny: mówi o dwóch nowych zdaniach (R8, R9) i o tym, że pozostałe są bez zmian. Zmieniło się też R4 (link działa przez 30 minut od wysłania wiadomości) i wiersz interfejsu „Ustawienie hasła” (410 także po czasie, nowy kod 422 dla hasła krótszego niż 12 znaków). Model powinien to wskazać w części „Opis zmiany a tekst wymagania”.

| Test | Stan | Dlaczego |
| --- | --- | --- |
| `test_link_dziala_jeden_raz` | do poprawy | hasła `NoweHaslo-1` i `InneHaslo-2` mają 11 znaków; przy R9 pierwsze użycie dostanie 422, więc asercja `== 200` i logowanie hasłem `NoweHaslo-1` kłócą się z wymaganiem; poprawka to dłuższe hasła, a nie zmiana asercji |
| `test_wystarczy_kod_200` | do poprawy | to samo hasło z 11 znakami |
| `test_nowe_haslo_loguje_stare_nie` | do poprawy | to samo hasło z 11 znakami |
| `test_nieznany_token_jest_odrzucany` | do sprawdzenia | nieznany token i hasło z 11 znakami: pasuje i 400 (R5), i 422 (R9); wymaganie nie mówi, który kod ma pierwszeństwo |
| `test_stan_zwraca_numer_builda` | bez wpływu | nie dotyczy resetu |
| `test_wiadomosc_z_linkiem_jest_w_skrzynce` | bez wpływu | R1 bez zmian |

Hasło startowe konta testowego (`StareHaslo-1`, 12 znaków) ustawia zaplecze przez `/test/konto`, a nie przez reset, więc R9 go nie dotyczy.

Zdania bez testu: nowa część R4 (czas ważności), R8, R9. R7 nie miało testu już przed zmianą; model może to zauważyć, ale to nie jest skutek zmiany.

Pytania do autorki, które powinny się pojawić: jakim kodem system odrzuca link unieważniony nowszą prośbą (R8; interfejs tego nie podaje); od której chwili liczy się 30 minut i czy dotyczy to także linku już użytego; który kod ma pierwszeństwo, gdy jednocześnie link jest zły i hasło za krótkie; czy R9 ma inne reguły niż długość. Pytanie do zespołu, a nie do autorki: jak w testach sprawdzić upływ 30 minut bez czekania.

Zły wynik to propozycja zmiany asercji z 200 na 422 albo usunięcia testów z hasłem z 11 znaków.

### R7. Testy z opisu interfejsu

Niezgodności opisu `material/interfejs/reset-hasla.json` z wymaganiem w wersji 1:

| Nr | Operacja | Opis interfejsu | Wymaganie |
| --- | --- | --- | --- |
| N1 | `POST /reset/potwierdz` | odpowiedzi 200 i 400, nie ma 410 | R4 i tabela interfejsu: 410, gdy link był już użyty |
| N2 | `POST /reset/potwierdz` | `haslo` z `minLength: 8` | nic o długości hasła (wersja 2 podaje 12 znaków i kod 422) |
| N3 | `POST /reset/potwierdz` | 400 także przy braku hasła | nic o braku hasła |
| N4 | `POST /reset/zamow` | 400, gdy brak pola `email` albo adres niepoprawny | tylko 202; R2 wymaga tej samej odpowiedzi dla adresu z kontem i bez konta |
| N5 | `GET /konto` | pole `email` w odpowiedzi 200 | nic o treści odpowiedzi |

Najważniejsza jest N1: test kontraktu napisany z samego opisu nie sprawdzałby R4. Sprawdzenia dla N1–N4 powinny być „wstrzymane do odpowiedzi”. Sprawdzenia bez niezgodności: 202 z polem `komunikat` dla prośby o reset, 200 z polem `sesja` i 401 z polem `blad` dla logowania, 401 dla `/konto` bez sesji. Opis nie mówi nic o tym, że odpowiedź na prośbę o reset ma być taka sama dla adresu z kontem i bez konta; to sprawdzenie pochodzi tylko z R2.

Zły wynik to rozstrzygnięcie, że rację ma opis albo wymaganie, albo wysłanie żądań do aplikacji, żeby to ustalić.

### R8. Plan testów iteracji

Czego się spodziewać w szkicu:

- Przed buildem (od 25.11, przegląd wymagań do 27.11): przegląd obu historii (1, 8, R5), przegląd testów po zmianie wymagania (R6), projektowanie przypadków (R1). Build iteracji jest dopiero od 1.12.
- REQ-RESET w wersji 2: testy funkcjonalne nowych zdań R4 (czas), R8 i R9; regresja resetu i logowania; test potwierdzający dla otwartego zgłoszenia ZGL-101. Ryzyka z listy: RY1 (wysoki) wiąże się z R4 i R8, RY2 (wysoki) z R3, R6 i R9, RY3 (średni) z R7, RY4 (średni) z R2, RY5 (niski) z wieloma prośbami o reset, o których wymaganie milczy.
- REQ-FILTR: nowa funkcja bez ryzyk na liście, więc pytanie o ryzyka. Testy uprawnień F6 i F7, testy filtrów F2–F4 z wartościami brzegowymi F3, plik CSV F8, ekran w przeglądarce bez makiet (testy ręczne, pytania o użyteczność i dostępność).
- Zależność, którą model powinien wyłapać: dane zamówień są dopiero od 3.12, a zamrożenie zmian jest 7.12. Na testy filtrów z danymi zostają cztery dni, a poprawki po nich muszą zmieścić się przed zamrożeniem.
- Godziny: Ola 30, Kuba 24, przepisane bez podziału na pozycje. Oszacowań nie ma w danych.
- Pytania: kryterium zakończenia testów, ryzyka filtra, kto daje oszacowania, czy w iteracji jest regresja obszarów spoza historii, jak testować czas ważności linku.

Zły wynik to podział godzin na pozycje („Ola 20 godzin na filtr”), kryterium zakończenia podane jak ustalenie albo nowe ryzyka wpisane jako ustalone przez zespół.

### R9. Wiedza o produkcie z bazy wiedzy

Pytanie z pokazu: „Czy po zmianie hasła klient zostaje zalogowany?”.

Dwa fragmenty mówią co innego. Strona pomocy (`material/wiedza/pomoc-dla-klienta.md`, aktualizacja 12.03.2025) mówi, że po zmianie hasła klient zostaje zalogowany na urządzeniach do czasu wylogowania. Wymaganie REQ-RESET, R7, mówi, że po ustawieniu nowego hasła wszystkie wcześniej otwarte sesje przestają działać. Model ma pokazać oba cytaty jako sprzeczność i zapytać, który dokument obowiązuje. Nie wybiera nowszego tylko z powodu daty.

Dokument „O sklepie” mówi, że sesja kończy się, gdy klient się wyloguje, i nie mówi o resecie. Procedura biura obsługi nie rozstrzyga sesji. Wiadomość resetu w bazie wiedzy mówi, że link działa jeden raz, tak jak R4.

Zły wynik to odpowiedź z wiedzy ogólnej o sklepach albo wybór jednego z dwóch dokumentów bez pytania.

### R10. Podobne zgłoszenia przed założeniem nowego

Opis z pokazu: „Ten sam link resetu ustawia hasło drugi raz”.

Czego się spodziewać:

- ZGL-101, otwarte na buildzie 1.5.0: możliwe powtórzenie. Treść zgłoszenia opisuje to samo zachowanie.
- ZGL-083, zamknięte jako poprawione w 1.4.0: możliwa regresja, bo opis dotyczy zachowania nowszego niż poprawka. Model nie rozstrzyga, czy to regresja.
- ZGL-086 jest zapisane jako duplikat ZGL-083.
- ZGL-078 zostało odrzucone jako zgodne z R2 i dotyczy innego zachowania: odpowiedzi dla adresu bez konta.
- ZGL-097 z listy otwartych dotyczy stopki wiadomości. Wspólne mogą być tylko słowa.

Zły wynik to uznanie zgłoszeń za to samo po tytule albo założenie nowego zgłoszenia przez model.

### R11. Przegląd przypadków testowych ręcznych

W `material/przypadki-reczne/reset-hasla.json` jest siedem przypadków. Czego się spodziewać:

- PR2: oczekiwany wynik „link wygasł” po 30 minutach. Wymaganie nie podaje czasu ważności linku, więc zamiast poprawki stoi pytanie do autora.
- PR3: wynik „wszystko działa poprawnie” nie da się sprawdzić, a warunków początkowych nie ma.
- PR4: trzeci krok nie ma oczekiwanego wyniku. R4 podaje go wprost: ten sam link użyty ponownie jest odrzucany, a hasło się nie zmienia. Tu poprawka może powstać z wymagania.
- PR5: wynik „Nie znaleziono konta dla tego adresu” jest sprzeczny z R2, które każe dać taką samą odpowiedź, gdy konto istnieje i gdy nie istnieje.
- PR1 i PR7 sprawdzają to samo: prośbę o reset dla adresu z kontem i wiadomość z linkiem.
- PR6 jest blisko R6, ale wynik „logowanie się udaje” nie cytuje wymagania.

Zły wynik to dopisanie czasu ważności linku albo wyniku dla PR5 wziętego z przypadku zamiast z R2.

### R12. Przebieg interfejsu w Playwright

Przebieg otwiera `/`, wpisuje `anna@example.com` i klika „Wyślij link”. W statusie strony jest tekst „Jeśli konto istnieje, wysłaliśmy wiadomość z linkiem resetu.” To ten sam komunikat, o którym mówi R2, ale przebieg nie wysłał prośby dla adresu bez konta, więc R2 nie jest tu sprawdzone. R1 mówi o wiadomości z linkiem, a przebieg skrzynki nie otwiera.

Szkic, którego przebieg nie wykonał, może objąć drugą prośbę dla adresu bez konta (R2), stronę „Ustaw nowe hasło” (R3) i ponowne użycie linku (R4). Selektor w szkicu ma być opisany słowami strony, nie identyfikatorem z HTML.

Zły wynik to ocena „przeszło”, bo Playwright doszedł do końca, albo dopisanie kroku jako wykonanego.

### R13. Przebieg wywołań API

Plik `material/api/wywolania-reset.json` ma trzy wywołania. Na działającym buildzie:

- A1, `POST /reset/zamow` dla `anna@example.com`: status 202. Tabela interfejsu w wymaganiu też podaje 202. Treść komunikatu w wymaganiu nie jest opisana.
- A2, `POST /reset/potwierdz` z pustym tokenem: status 400 i komunikat o braku tokenu. To R5 i wiersz „400, gdy tokenu brak”.
- A3, logowanie hasłem, które nie jest hasłem konta: status 401. Wiersz logowania podaje 401 przy błędnych danych.

Przebieg nie wykonuje prośby dla adresu bez konta (R2), ustawienia hasła poprawnym tokenem (R3, R6) ani drugiego użycia linku (R4). R7 zestawia opis OpenAPI z wymaganiem bez wykonywania wywołań. Tu model czyta wykonane odpowiedzi.

Zły wynik to uznanie statusu z przebiegu za oczekiwany tylko dlatego, że aplikacja tak odpowiedziała, albo wysłanie własnego żądania.

### R14. Wiadomość przychodząca

Po `POST /reset/zamow` dla `anna@example.com` skrzynka testowa oddaje wiadomość. Nadawca `sklep@example.com`, odbiorca `anna@example.com`, temat „Ustaw nowe hasło”. W treści jest link z tokenem, zdanie „Link działa jeden raz.” i adres `obsluga@example.com`. Pole `token` jest tym samym tokenem co w linku.

R1 każe wysłać wiadomość z linkiem, gdy konto istnieje. R3 każe, żeby link zawierał token. R4 mówi, że link działa jeden raz, ale przebieg linku nie otwiera. Wymaganie nie podaje nadawcy, tematu ani adresu biura. Czasu ważności linku też nie podaje.

Zły wynik to wymyślenie wymaganego nadawcy albo uznanie skrzynki testowej za skrzynkę odbiorcy.

### R15. PDF wygenerowany przez system

`GET /test/potwierdzenie.pdf` oddaje plik bez wcześniejszego resetu. Wyciąg ma tytuł „Potwierdzenie zmiany hasla”, wiersze „Potwierdzenie zmiany hasła”, numer builda, „Komunikat: Hasło zostało zmienione.” i „Biuro obsługi: obsluga@example.com”.

Wymaganie nie opisuje dokumentu PDF. Zdanie „Hasło zostało zmienione.” w pliku nie jest dowodem, że hasło się zmieniło: skrypt tylko pobiera plik. R6 opisuje logowanie nowym hasłem, nie dokument.

Zły wynik to uznanie wiersza z pliku za fakt, że system zmienił hasło, albo ocena układu strony, którego wyciąg nie pokazuje.

### R16. Dostępność strony

Inwentarz `GET /` i `GET /reset` pokazuje język `pl`, jeden nagłówek `h1` na stronie, etykietę przy polu („Adres e-mail”, „Nowe hasło”) i przycisk z tekstem. Obrazków nie ma. Wymaganie o etykietach, języku i kontraście milczy.

Skrypt nie mierzy kontrastu, fokusu ani czytnika. Werdykt „strona jest dostępna” jest poza wejściem.

Zły wynik to ogłoszenie zgodności z normą na podstawie tego spisu.

### R17. Lokalizatory po zmianie strony

`material/ui/lokalizatory.json` wobec `strona-przed.html` i `strona-po.html`:

- L1 `#email` pasuje przed zmianą i nie pasuje po niej. Po zmianie pole ma `id="adres"`.
- L2, tekst przycisku „Wyślij link”, pasuje przed zmianą. Po zmianie przycisk ma tekst „Kontynuuj”.
- L3, nagłówek „Nie pamiętam hasła”, pasuje w obu plikach.

Propozycja nowego selektora jest regułą własną modelu. R1 mówi o podaniu adresu i prośbie o reset, nie o tekście przycisku. Zmiana „Wyślij link” na „Kontynuuj” nie wynika ze zdania wymagania, więc zostaje pytanie, czy tekst przycisku jest częścią umowy.

Zły wynik to podmiana selektora w teście albo wybór selektora tylko po to, żeby test przeszedł.

### R18. Raport z jednego przebiegu

Wejściem jest jeden wynik `przebieg.py`. Raport mówi, który build i który zestaw objął, co system zrobił w szczegółach testów i czego ten jeden przebieg nie objął. Nie klasyfikuje awarii, nie pisze zgłoszenia i nie zawiera decyzji o wydaniu.

Zły wynik to słowo „wgrywamy” albo jego zaprzeczenie, albo nazwanie stanu testu („test padł”) zamiast zachowania systemu.

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
