---
name: ocena-asercji
description: Ocena, czy test wykryłby znany defekt. Zestawia asercje testów ze zdaniem wymagania i z wynikami na buildzie zgodnym oraz wadliwym, a potem mówi, który test nadaje się na bramkę i dlaczego drugi defektu nie łapie. Użyj, gdy tester pyta o siłę asercji, o to, czy test coś sprawdza, który z testów ma być bramką albo dlaczego test jest zielony na wadliwym buildzie.
---

# Ocena asercji

Zielony test jest wart tyle, ile jego asercja. Test, który sprawdza za mało, przechodzi także na wadliwym buildzie i daje fałszywe poczucie bezpieczeństwa. Twoim zadaniem jest pokazać na wynikach, który test odróżnia build zgodny z wymaganiem od builda z defektem. Samych testów nie ruszasz: ocena służy człowiekowi do decyzji, co jest bramką.

## Wejście

- Kod ocenianych testów.
- Wyniki tych testów na dwóch buildach: zgodnym z wymaganiem i wadliwym. Który build jest który, mówi tester w prośbie albo wynika to z wejścia; skill tego nie przesądza.
- Wymaganie.

W repozytorium qa-demo:

```powershell
python narzedzia/tabela_asercji.py
python narzedzia/wymaganie.py reset-hasla
```

Pierwsze polecenie podaje kod dwóch testów, tabelę ich wyników na dwóch buildach oraz wymianę żądań i odpowiedzi z każdego uruchomienia. Inne buildy wskazuje opcja `--porty`.

## Jak pracować

1. Dla każdego testu wypisz jego asercje, czyli to, co faktycznie sprawdza. Nazwa i opis testu mówią o zamiarze; liczy się kod.
2. Wskaż zdanie wymagania, którego test dotyczy, i oceń, którą część tego zdania asercje pokrywają, a której nie.
3. Zestaw wyniki na obu buildach. Jeśli tester nie powiedział, który build jest zgodny z wymaganiem, a który wadliwy, ustal to z wymiany z aplikacją zestawionej ze zdaniem wymagania i napisz, na czym to opierasz. Test, który ma ten sam wynik na buildzie zgodnym i na wadliwym, nie odróżnia ich od siebie.
4. Na podstawie wymiany z aplikacją powiedz, co system zrobił na wadliwym buildzie i dlaczego dana asercja to zauważyła albo przepuściła.
5. Sformułuj jedno zdanie: który test nadaje się na bramkę i dlaczego drugi defektu nie wykrywa.

## Format wyniku

```markdown
# Ocena asercji: <nazwy testów>

## Zdanie modelu

<jedno zdanie: test A nadaje się na bramkę, bo ...; test B tego defektu nie wykrywa, bo ...>

| Test | Co sprawdzają asercje | Zdanie wymagania | Wynik na <build zgodny> | Wynik na <build wadliwy> | Czy odróżnia buildy |
| --- | --- | --- | --- | --- | --- |
| <test> | <asercje własnymi słowami> | <numer>: „<cytat>” | <wynik> | <wynik> | <tak albo nie, z powodem> |

### Co system zrobił na wadliwym buildzie

<zachowanie systemu odczytane z wymiany żądań i odpowiedzi>

### Czego nie sprawdziłem

- <na przykład: oceniam tylko ten jeden defekt; nie wiem, jak testy zachowają się przy innych>

## Decyzja człowieka

- [ ] Który test jest bramką:
- [ ] Co dzieje się ze słabszym testem (zostaje, do wzmocnienia, do usunięcia):
```

## Czego nie robisz

- Nie zmieniasz kodu testów: nie obcinasz, nie dopisujesz i nie łagodzisz asercji.
- Nie usuwasz ani nie wyłączasz słabszego testu.
- Nie zmieniasz oczekiwanego wyniku tak, żeby test był zielony na wadliwym buildzie.
- Nie wyprowadzasz oczekiwanego wyniku z tego, co robi aplikacja. Oczekiwany wynik pochodzi z wymagania. Asercja „nauczona” od wadliwego builda utrwaliłaby defekt.

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
