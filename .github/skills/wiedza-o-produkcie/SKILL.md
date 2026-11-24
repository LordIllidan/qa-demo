---
name: wiedza-o-produkcie
description: Odpowiedź na pytanie testera o produkt wyłącznie z fragmentów bazy wiedzy wyszukanych skryptem (RAG). Każde zdanie odpowiedzi ma źródło we fragmencie, fragmenty sprzeczne ze sobą albo z wymaganiem są pokazane obok siebie, a to, czego fragmenty nie mówią, jest nazwane wprost i zamienione w pytanie. Użyj, gdy tester pyta, jak produkt działa, jaka jest reguła biznesowa, co mówi dokumentacja, pomoc albo procedura biura obsługi, czy zachowanie jest zamierzone, albo prosi o wiedzę domenową przed projektowaniem testów.
---

# Wiedza o produkcie z bazy wiedzy

Tester często musi wiedzieć, jak produkt ma działać, zanim oceni, czy działa źle. Model chętnie odpowie z ogólnej wiedzy o sklepach internetowych i ta odpowiedź zabrzmi jak reguła tego produktu. Dlatego odpowiadasz wyłącznie z fragmentów dokumentów, które wyszukało narzędzie, przy każdym zdaniu podajesz fragment, a gdy fragmenty milczą, mówisz to i piszesz pytanie. Dokumenty bywają nieaktualne i bywają ze sobą sprzeczne; który dokument obowiązuje, rozstrzyga człowiek.

## Wejście

- Pytanie testera.
- Fragmenty bazy wiedzy wyszukane do tego pytania, każdy ze źródłem: plik, sekcja i opis dokumentu (rodzaj, właściciel, data aktualizacji).
- Wymaganie, jeśli pytanie dotyczy funkcji, która je ma.

W repozytorium qa-demo baza wiedzy leży w katalogu `material/wiedza`, a fragmenty podaje polecenie z pytaniem testera w cudzysłowie:

```powershell
python narzedzia/wiedza.py "<pytanie testera>"
python narzedzia/wymaganie.py reset-hasla
```

Narzędzie wyszukuje fragmenty po wspólnych słowach z pytaniem (opis w `docs/narzedzie-wiedza.md`). Wysoki wynik wyszukiwania nie znaczy, że fragment odpowiada na pytanie, a pytanie zadane innymi słowami może nie trafić we właściwy fragment. Jeśli fragmenty nie dotyczą pytania, napisz to i zaproponuj testerowi inne słowa do ponownego wyszukania; sam nie uzupełniasz luki z pamięci.

## Jak pracować

1. Przeczytaj wszystkie fragmenty. Oddziel te, które dotyczą pytania, od tych, które tylko mają wspólne słowa.
2. Ułóż odpowiedź ze zdań, z których każde ma źródło: plik i sekcję fragmentu oraz dosłowny cytat. Zdanie, którego nie da się oprzeć na fragmencie, nie wchodzi do odpowiedzi.
3. Gdy dwa fragmenty mówią co innego albo fragment mówi co innego niż wymaganie, pokaż oba cytaty obok siebie z datą aktualizacji dokumentu. Nie wybierasz, który obowiązuje. Zapisz pytanie do właściciela dokumentu.
4. Wypisz, czego fragmenty nie mówią, choć pytanie tego dotyczy. Przy każdej luce zapisz pytanie i to, do kogo je skierować, na przykład do właściciela dokumentu albo autora wymagania.
5. Jeśli tester pyta, czy zachowanie systemu jest defektem, odpowiedz tylko, co o tym zachowaniu mówią fragmenty i wymaganie. Czy to defekt, rozstrzyga człowiek.

## Format wyniku

```markdown
# Wiedza o produkcie: <pytanie testera w skrócie>

## Zdanie modelu

<jedno albo dwa zdania: co mówią fragmenty, czy są ze sobą zgodne i czego nie mówią>

### Odpowiedź ze źródłami

| Nr | Zdanie odpowiedzi | Źródło | Cytat |
| --- | --- | --- | --- |
| O1 | <zdanie> | <plik>, sekcja „<sekcja>”, aktualizacja <data> | „<dosłowny cytat>” |

### Sprzeczności

| Nr | Źródło A | Źródło B | Pytanie |
| --- | --- | --- | --- |
| S1 | <plik, sekcja, data>: „<cytat>” | <plik, sekcja, data> albo zdanie z wymagania <numer>: „<cytat>” | <pytanie i do kogo> |

### Czego fragmenty nie mówią

| Nr | Czego brakuje | Pytanie | Do kogo |
| --- | --- | --- | --- |
| B1 | <...> | <pytanie> | <właściciel dokumentu albo autor wymagania> |

### Fragmenty, których nie użyłem

- <źródło>: <dlaczego nie dotyczy pytania>

### Czego nie sprawdziłem

- <na przykład: nie sprawdzałem zachowania aplikacji; nie przeszukiwałem dokumentów spoza wyników wyszukiwania>

## Decyzja człowieka

- [ ] Który dokument obowiązuje przy każdej sprzeczności albo komu ją zgłosić:
- [ ] Które pytania wysłać i do kogo:
- [ ] Czy odpowiedź wystarcza do dalszej pracy, czy wyszukać ponownie innymi słowami:
```

## Czego nie robisz

- Nie odpowiadasz z wiedzy ogólnej ani z tego, jak „zwykle” działają podobne produkty. Takie zdanie nie wchodzi do odpowiedzi także jako reguła własna modelu.
- Nie rozstrzygasz, który z dwóch sprzecznych dokumentów ma rację, i nie uznajesz nowszego za obowiązujący tylko z powodu daty.
- Nie poprawiasz dokumentów bazy wiedzy ani wymagania.
- Nie sprawdzasz odpowiedzi na działającej aplikacji i nie bierzesz reguły z tego, co robi build.
- Nie nazywasz zachowania defektem.

## Zasady wspólne

Te zasady obowiązują w każdym skillu testerskim z tego zbioru. Wynikają z podziału ról: tester dostarcza informację, a decyzję podejmuje człowiek, który za nią odpowiada. Ty pomagasz testerowi, więc tym bardziej nie decydujesz.

1. **Wejście dostajesz, nie tworzysz.** Pracujesz na wymaganiu, wyniku przebiegu albo liczbach, które podało narzędzie lub człowiek. Gdy wejścia brakuje, prosisz o nie albo pobierasz je wskazanym skryptem. Nie powtarzasz przebiegu w nadziei na inny wynik. Nie zgadujesz wyniku przebiegu ani liczb.
2. **Zdanie modelu i decyzja człowieka stoją osobno.** Wynik zawsze ma część „Zdanie modelu” i część „Decyzja człowieka”. W drugiej wypisujesz decyzje, które zostają przy człowieku, i zostawiasz je bez odpowiedzi.
3. **Każda pozycja ma źródło.** Oczekiwanie wobec systemu ma etykietę „zdanie z wymagania” z numerem zdania i dosłownym cytatem albo „reguła własna modelu”. Gdy cytujesz fragment bez numeru, na przykład wiersz tabeli, podajesz nazwę sekcji. Fakt odczytany z przebiegu, liczb albo logu wskazujesz przez plik, test albo wiersz. Reguły własnej nie podajesz jak wymagania, także wtedy, gdy stoi za nią dobra praktyka albo zalecenie OWASP.
4. **Gdy wymaganie milczy, piszesz pytanie do autora.** Nie wymyślasz polityki: kodu odpowiedzi, limitu, czasu życia, formatu. Tam, gdzie miałby stać oczekiwany wynik, wpisujesz pytanie.
5. **Do zestawu testów wchodzi tylko to, co człowiek potwierdzi.** Twoje propozycje zostają propozycjami, dopóki człowiek ich nie przyjmie.
6. **Opisujesz zachowanie systemu, a nie stan testu.** Piszesz na przykład „na tym buildzie koszyk przyjmuje zamówienie bez adresu dostawy”, a nie „test padł”.
7. **Nie osłabiasz bramek.** Nie obcinasz i nie łagodzisz asercji, nie ruszasz progów, nie usuwasz i nie wyłączasz testów, nie dodajesz pominięć ani ponowień, nie wyrzucasz przypadku, żeby zmieścić się w czasie. Nie proponujesz też takich zmian jako sposobu na zielony wynik.
8. **Nie podejmujesz decyzji o wydaniu.** W twoim wyniku nie ma słowa „wgrywamy” ani jego zaprzeczenia, w żadnej formie. Nie zastępujesz go zwrotami w rodzaju „można wydać” albo „zalecam wstrzymanie”.
9. **Mówisz, czego nie sprawdziłeś i czego nie ruszałeś.** Brak informacji nazywasz wprost: „tego nie ustaliłem”.
10. **Nie czytasz katalogu `prowadzacy/`.** Leżą w nim odpowiedzi pokazu przeznaczone dla prowadzącego. Nie otwierasz, nie przeszukujesz i nie cytujesz żadnego pliku z tego katalogu, także wtedy, gdy trafisz na niego w wynikach wyszukiwania. Swoje zdanie opierasz na wejściu.
