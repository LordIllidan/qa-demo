# Tester manualny i tester automatyzujący: kto czego używa

Zestaw ma trzydzieści dwa zagadnienia: czternaście z pokazu i osiemnaście rozszerzających (R1–R18). Ten plik dzieli je według dwóch ról i dla każdej podaje, w którym momencie pracy sięgnąć po które zagadnienie, co tester wnosi sam, co dostaje i na co ma uważać. Na końcu stoi wykaz rodzajów testów i prac, których zestaw nie obejmuje.

Opis zagadnień jest w `README.md`, opis skilli w [skille.md](skille.md), opis agentów w [agenci-copilot.md](agenci-copilot.md).

## Dwie role

| | Tester manualny | Tester automatyzujący |
| --- | --- | --- |
| Główna praca | analizuje wymagania, projektuje przypadki, wykonuje testy ręcznie, prowadzi sesje eksploracyjne, zgłasza defekty i sprawdza poprawki | wybiera, co automatyzować, pisze i utrzymuje testy oraz ich zaplecze, czyta wyniki przebiegów, oddziela defekt od wady testu i środowiska, pilnuje bramek |
| Wejście, z którym pracuje | wymaganie, własne notatki, lista sprawdzeń, zgłoszenia | wymaganie, kod testów, zapis przebiegu, historia przebiegów, liczby |
| Gdzie model pomaga najwięcej | przy tekście: pytania do autora, przypadki, karta sesji, szkic zgłoszenia | przy zapisie przebiegu i kodzie: klasyfikacja awarii, ocena asercji, szkic testu, przegląd zmiany |
| Gdzie model szkodzi najłatwiej | dopisuje do zgłoszenia krok, którego nie było, albo oczekiwany wynik, którego wymaganie nie podaje | bierze oczekiwany wynik z tego, co build zwraca, albo osłabia asercję, żeby test był zielony |

W wielu zespołach jedna osoba wykonuje obie prace. Podział dotyczy czynności, a nie stanowiska.

## Zagadnienia według ról

„Tak” oznacza pracę codzienną. „Czasem” oznacza pracę, do której trzeba wnieść własne wejście albo która zdarza się rzadziej.

| Nr | Zagadnienie | Tester manualny | Tester automatyzujący | Agent |
| --- | --- | --- | --- | --- |
| 1 | Luki w wymaganiu | tak | tak | Analiza wymagania |
| 2 | Defekt z czerwonego przebiegu | – (patrz R2) | tak | Analiza przebiegu |
| 3 | Ocena asercji | – | tak | Analiza przebiegu |
| 4 | Zakres po zmianie | tak | czasem | Zakres i wydanie |
| 5 | Zdanie o dwóch buildach | czasem | tak | Zakres i wydanie |
| 6 | Karta przed wgraniem | tak | tak | Zakres i wydanie |
| 7 | Dane pod regułę | tak (tabela wejść) | tak (plik dla przebiegu) | Analiza wymagania |
| 8 | Uprawnienia przy zwykłej historyjce | tak | tak | Analiza wymagania |
| P1 | Czerwony przebieg: produkt, test czy środowisko | – | tak | Analiza przebiegu |
| P2 | Ponowny test po poprawce | czasem (własny wynik) | tak | Analiza przebiegu |
| P3 | Test niestabilny | – | tak | Analiza przebiegu |
| P4 | Pokrycie wymagania testami | czasem (lista przypadków ręcznych) | tak | Analiza wymagania |
| P5 | Karta sesji eksploracyjnej | tak | czasem | Analiza wymagania |
| P6 | Przegląd zmiany w testach | – | tak | Analiza przebiegu |
| R1 | Przypadki testowe techniką | tak | tak | Analiza wymagania |
| R2 | Zgłoszenie z obserwacji ręcznej | tak | czasem | Analiza przebiegu |
| R3 | Kandydaci do automatyzacji | czasem (dostarcza listę) | tak | Zakres i wydanie |
| R4 | Szkic testu automatycznego | – | tak | Analiza wymagania |
| R5 | Testy niefunkcjonalne | tak | tak | Analiza wymagania |
| R6 | Testy po zmianie wymagania | czasem (przypadki ręczne) | tak | Analiza wymagania |
| R7 | Testy z opisu interfejsu | czasem (testy API wykonywane ręcznie) | tak | Analiza wymagania |
| R8 | Plan testów iteracji | tak | tak | Zakres i wydanie |
| R9 | Wiedza o produkcie z bazy wiedzy | tak | tak | Analiza wymagania |
| R10 | Podobne zgłoszenia przed założeniem nowego | tak | tak | Analiza przebiegu |
| R11 | Przegląd przypadków testowych ręcznych | tak | – | Analiza wymagania |
| R12 | Przebieg interfejsu w Playwright | czasem | tak | Analiza przebiegu |
| R13 | Przebieg wywołań API | czasem | tak | Analiza przebiegu |
| R14 | Wiadomość przychodząca | tak | tak | Analiza przebiegu |
| R15 | PDF wygenerowany przez system | tak | tak | Analiza przebiegu |
| R16 | Dostępność strony | tak | czasem | Analiza przebiegu |
| R17 | Lokalizatory po zmianie strony | – | tak | Analiza przebiegu |
| R18 | Raport z jednego przebiegu | tak | tak | Analiza przebiegu |

## Ścieżka testera manualnego

| Moment pracy | Zagadnienie | Co wnosisz | Co dostajesz | Na co uważasz |
| --- | --- | --- | --- | --- |
| Przed iteracją | R8 | dane iteracji, ryzyka, godziny | szkic planu: rodzaje testów, role, terminy, pytania | oszacowania i kryterium zakończenia daje zespół, nie model |
| Historyjka trafia do przeglądu | 1, 8, R5, R9 | tekst wymagania i pytanie o produkt | pytania do autora, przypadki uprawnień, pytania o cechy jakości, odpowiedź z fragmentów bazy wiedzy | pytanie nie jest wymaganiem; zdanie bez cytatu fragmentu nie jest regułą produktu |
| Wymaganie się zmieniło | R6 | obie wersje wymagania, własne przypadki ręczne | które przypadki trzeba poprawić i które nowe zdania nie mają przypadku | opis zmiany od autora może nie wymieniać wszystkiego |
| Projektujesz testy | R1, 7 | tekst wymagania | przypadki z techniką i źródłem, tabelę wejść | oczekiwany wynik bez cytatu z wymagania to pytanie, a nie przypadek |
| Przed sesją eksploracyjną | P5 | listę ryzyk, cel sesji | kartę sesji | zakres i czas ustalasz ty |
| Po sesji albo po wykonaniu przypadków | P5, R2, R10, R11 | notatki, opis zachowania, przypadki ręczne | raport z sesji, szkic zgłoszenia, podobne zgłoszenia, problemy w przypadkach | w szkicu nie może być kroku, którego nie ma w notatkach; podobieństwo zgłoszeń rozstrzygasz ty |
| Przychodzi poprawka | P2 | zgłoszenie i własny wynik ponownego testu | zdanie o tym, czy kroki dają wynik oczekiwany, i co zostało niesprawdzone | „naprawione” mówisz ty, po sprawdzeniu |
| Zmiana w ograniczonym oknie czasu | 4 | listę sprawdzeń z czasami | kolejność od najwyższego ryzyka i to, co się nie mieści | model niczego nie usuwa z listy; skrócenie zakresu to decyzja |
| Przed wydaniem | 6 | wyniki, zgłoszenia, zakres | kartę: co sprawdzone, co czerwone, czego nie ruszano | decyzja o wydaniu nie należy do modelu |

### Jak wnieść własne wejście

Część skilli opisuje wejście z automatycznego przebiegu. Zasada wspólna 1 dopuszcza także wejście podane przez człowieka, więc tester manualny wnosi je sam:

- wkleja tekst do rozmowy: wymaganie z własnego projektu, notatki, wynik wykonania przypadku,
- albo zapisuje go w pliku w katalogu `wyniki` i wskazuje plik w prośbie. Katalog `wyniki` nie trafia do repozytorium.

```powershell
New-Item -ItemType Directory -Force wyniki | Out-Null
Copy-Item material/sesja/notatki-z-sesji.md wyniki/moje-notatki.md
copilot --agent analiza-przebiegu --prompt "Przygotuj zgłoszenie z obserwacji zapisanej w wyniki/moje-notatki.md o godzinie 10:13."
```

Szkic jest tak dobry jak notatki. Notatka, z której da się zrobić zgłoszenie, ma: build, dane, czynności w kolejności, dosłowną odpowiedź systemu i godzinę.

## Ścieżka testera automatyzującego

| Moment pracy | Zagadnienie | Co wnosisz | Co dostajesz | Na co uważasz |
| --- | --- | --- | --- | --- |
| Przed iteracją | R8 | dane iteracji, ryzyka, godziny | szkic planu z podziałem na role | to samo co tester manualny |
| Historyjka trafia do przeglądu | 1, 8, R5 | tekst wymagania | pytania do autora, przypadki uprawnień, pytania o cechy jakości | to samo co tester manualny |
| Zespół oddał opis interfejsu | R7 | opis OpenAPI, wymaganie | sprawdzenia kontraktu ze źródłem i niezgodności opisu z wymaganiem | test kontraktu z samego opisu utrwala implementację |
| Wymaganie się zmieniło | R6 | obie wersje wymagania, kod testów | stan każdego testu, zdania bez testu, pytania | test poprawia się dlatego, że zmieniło się zdanie, a nie dlatego, że jest czerwony |
| Planujesz, co automatyzować | R3, P4 | listę sprawdzeń ręcznych, listę testów | które sprawdzenia mają test w całości, częściowo albo wcale; zdania wymagania bez testu | nazwa testu nie dowodzi pokrycia; liczy się to, co test sprawdza |
| Piszesz test | R1, R4, 7 | potwierdzony przypadek, wymaganie, kod zestawu | szkic kodu, asercje ze źródłem, plik danych dla przebiegu | oczekiwany wynik pochodzi z wymagania, nigdy z odpowiedzi builda |
| Rano po nocnym przebiegu | P1 | zapis przebiegu i log | grupy awarii z proponowaną klasyfikacją i dowodem | klasyfikacja jest propozycją; ponowne uruchomienie niczego nie wyjaśnia |
| Czerwony test | 2, 3 | wynik przebiegu, wymaganie | szkic zgłoszenia, ocenę tego, co asercja sprawdza | zgłoszenie opisuje zachowanie systemu, a nie stan testu |
| Test raz zielony, raz czerwony | P3 | historię przebiegów | liczby i przypuszczalny wzorzec | ponowienie i pominięcie to osłabienie bramki |
| Przegląd zmiany w testach | P6 | różnicę wersji i wyniki obu wersji | miejsca, w których bramka stała się słabsza | zielony wynik po zmianie testu nie dowodzi poprawki w produkcie |
| Przychodzi poprawka | P2 | zgłoszenie i przebieg na buildzie z poprawką | zdanie o wyniku kroków ze zgłoszenia | wynik jednego testu nie mówi o regresji obok |
| Przed wydaniem | 5, 6 | liczby dwóch buildów, wyniki | jedno zdanie o liczbach, kartę | progów nie zmienia model |

```powershell
copilot --agent zakres-i-wydanie --prompt "Zestaw listę sprawdzeń ręcznych z testami automatycznymi i pokaż, co nie ma testu."
copilot --agent analiza-wymagania --prompt "Napisz test automatyczny dla przypadku, który potwierdzam: <kroki, dane, oczekiwany wynik>."
copilot --agent analiza-wymagania --prompt "Autorka zmieniła wymaganie resetu hasła. Które testy trzeba poprawić?"
```

## Nawyki, które dają efekt

Wspólne dla obu ról:

1. **Przynosisz wejście.** Model pracuje na wymaganiu, notatkach albo zapisie przebiegu. Bez wejścia zgaduje.
2. **Jedna prośba, jedno zagadnienie.** Prośba „przetestuj reset hasła” daje długą listę bez źródeł. Prośba o konkretny wynik daje coś, co da się sprawdzić w kilka minut.
3. **Najpierw czytasz źródła.** Przy każdej pozycji stoi cytat z wymagania albo etykieta „reguła własna modelu”. Cytat sprawdzasz z tekstem. Reguła własna modelu jest propozycją.
4. **Czytasz część „Czego nie sprawdziłem”.** To lista rzeczy, które zostają do zrobienia albo do świadomego pominięcia.
5. **Pola decyzji wypełniasz ty.** Model ich nie wypełnia. Do zestawu, do zgłoszeń i do karty wchodzi to, co potwierdzisz.
6. **Nie wklejasz danych produkcyjnych ani haseł.** Do przykładów wystarczają dane wymyślone.

Tester manualny:

- Zamiast „wygeneruj przypadki” prosisz o przypadki z techniką (R1). Dostajesz mniej przypadków, a każdy ma powód.
- Notatki prowadzisz na bieżąco, z dosłownymi odpowiedziami systemu. Raport z sesji i szkic zgłoszenia powstają wtedy bez dopisywania z pamięci.
- Przed zgłoszeniem pytasz o możliwe powtórzenia (R2). Czy to powtórzenie, rozstrzygasz ty.

Tester automatyzujący:

- Test piszesz dla przypadku, który ktoś potwierdził (R4). Kod od modelu przechodzi przegląd jak kod każdego autora.
- Czerwony przebieg najpierw klasyfikujesz (P1), dopiero potem uruchamiasz ponownie.
- Prośby „napraw test” nie kierujesz do modelu bez wymagania. Model najłatwiej „naprawia” test zmianą asercji.
- Zmianę w testach, także własną, oddajesz do przeglądu (P6).
- Po zmianie wymagania przeglądasz testy, zanim nowy build zrobi je czerwonymi (R6).

## Rodzaje testów: co zestaw obejmuje

| Rodzaj albo poziom testów | Co daje zestaw | Zagadnienia |
| --- | --- | --- |
| Testy funkcjonalne na poziomie systemu, przez interfejs programistyczny | analiza wymagania, projektowanie przypadków, dane, zgłoszenie, ocena asercji, szkic testu | 1, 7, R1, 2, 3, R2, R4 |
| Testy regresji i testy potwierdzające | zakres po zmianie, klasyfikacja awarii, test niestabilny, ponowny test po poprawce | 4, P1, P3, P2 |
| Testy eksploracyjne | karta sesji, raport z notatek, zgłoszenie z obserwacji | P5, R2 |
| Bezpieczeństwo | tylko przypadki uprawnień z wymagania i pytania do autora | 8, R5 |
| Wydajność | tylko odczyt liczb dwóch buildów względem progów i pytania o progi | 5, R5 |
| Użyteczność, dostępność, zgodność, niezawodność | tylko pytania do autora i nazwa rodzaju testu | R5 |
| Raportowanie przed wydaniem | karta dla osoby decydującej | 6 |
| Testy interfejsu programistycznego i kontraktu | sprawdzenia z opisu OpenAPI i niezgodności z wymaganiem, bez wykonania | R7 |
| Utrzymanie automatyzacji | pokrycie, przegląd zmiany, kandydaci do automatyzacji, testy po zmianie wymagania | P4, P6, R3, R6 |
| Planowanie testów | szkic planu iteracji z ryzykami, rolami i terminami | R8 |

## Czego zestaw nie obejmuje

- **Testy interfejsu użytkownika.** Aplikacja demonstracyjna nie ma ekranu. Nie ma więc testów przez przeglądarkę, lokatorów, testów wizualnych ani zgodności z przeglądarkami i urządzeniami.
- **Wykonanie testów niefunkcjonalnych.** Zestaw nie zawiera skryptów obciążeniowych, skanów bezpieczeństwa, testów penetracyjnych ani badania dostępności. Zagadnienie R5 kończy się na pytaniach i planie.
- **Testy jednostkowe i integracyjne komponentów.** Zestaw działa na poziomie testów systemowych.
- **Wykonanie testów kontraktu.** Zagadnienie R7 kończy się na liście sprawdzeń i niezgodności; nie ma narzędzia, które sprawdza odpowiedzi aplikacji względem opisu.
- **Potok CI.** Przebiegi uruchamia się ręcznie. Zapis nocnego przebiegu jest przygotowany ręcznie.
- **Szacowanie pracy i strategia testów organizacji.** Zagadnienie R8 układa plan jednej iteracji z danych zespołu i nie szacuje pracy.
- **Testy akceptacyjne z użytkownikiem i środowiska testowe.**

Każda z tych pozycji wymaga nowego materiału, nowego narzędzia albo zmiany aplikacji demonstracyjnej.

## Źródła podziału

- Poziomy i typy testów, kwadranty testowe: [ISTQB CTFL 4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf), rozdziały 2.2 i 5.1.
- Praca przy automatyzacji testów: [ISTQB CTAL-TAE 2.0](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTAL-TAE_Syllabus_v2.0.pdf).
- Użycie generatywnej AI w testowaniu: [ISTQB CT-GenAI 1.1](https://istqb.org/wp-content/uploads/2026/05/ISTQB-CT-GenAI-Syllabus-v1.1.pdf), rozdział 2.2.
- Cechy jakości produktu: [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html).
