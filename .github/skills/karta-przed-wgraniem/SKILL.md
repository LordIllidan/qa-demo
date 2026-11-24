---
name: karta-przed-wgraniem
description: Karta dla osoby, która decyduje o wydaniu. Składa wyniki przebiegów, liczby, otwarte zgłoszenia i zakres w jedno zdanie o stałym układzie trzech części (co sprawdzone, co czerwone, czego nie ruszano) i nie zawiera decyzji o wydaniu. Użyj, gdy tester prosi o podsumowanie przed wydaniem, kartę albo raport dla decydenta, status testów przed wgraniem lub zebranie wyników w jedno zdanie.
---

# Karta przed wgraniem

Osoba, która decyduje o wydaniu, nie czyta przebiegów. Potrzebuje krótkiej, uczciwej informacji: co sprawdzono, co jest czerwone i czego nikt nie dotknął. Twoim zadaniem jest tę informację złożyć z zebranych wyników. Decyzja o wydaniu należy do człowieka, który za nią odpowiada, więc karta jej nie zawiera ani nie podpowiada.

## Wejście

Zebrane wyniki: przebiegi testów, liczby, otwarte zgłoszenia, zakres planowany i wykonany. W repozytorium qa-demo zbiera je jedno polecenie:

```powershell
python narzedzia/zbierz_wyniki.py
```

Narzędzie bierze wyniki przebiegów z plików zapisanych wcześniej przez `python narzedzia/przebieg.py --port <port>`. Jeśli w zbiorze stoi, że pliku przebiegu brakuje, tego builda nie sprawdzono i tak to zapisujesz na karcie. Domyślnie zbiór obejmuje buildy z portów 8765 i 8766; inne dołącza opcja `--porty`.

## Jak pracować

1. Przejdź po zbiorze i każdą informację przypisz do jednej z trzech części: sprawdzone, czerwone, nie ruszane.
2. „Sprawdzone” to to, na co jest wynik w wejściu. Pozycję planu oznaczoną jako wykonana, na którą w zbiorze nie ma wyniku, wpisujesz z dopiskiem „według planu wykonane, wyniku nie widziałem”.
3. „Czerwone” to każdy wynik inny niż zaliczony, każda metryka ponad progiem i każde otwarte zgłoszenie. Opisz je zachowaniem systemu i liczbami, bez łagodzenia. Niczego czerwonego nie pomijasz, także wtedy, gdy wydaje się drobne. Wyraźną zmianę liczby, która nie ma progu, podajesz obok jako liczbę, bez oceny.
4. „Nie ruszane” to pozycje planu niewykonane, buildy bez wyniku i obszary, o których wejście milczy.
5. Ułóż jedno zdanie, które zawiera wszystkie trzy części. Pod nim daj kartę z pozycjami.

Jeśli tester pyta wprost o decyzję, odpowiadasz jednym zdaniem, że podejmuje ją osoba odpowiedzialna za wydanie, i oddajesz kartę.

## Format wyniku

```markdown
# Karta przed wgraniem: <wydanie albo build>

## Zdanie modelu

<jedno zdanie: sprawdzono ...; czerwone jest ...; nie ruszano ...>

### Sprawdzone

- <co, na którym buildzie, z jakim wynikiem, skąd wynik>

### Czerwone

- <zachowanie systemu albo liczba ponad progiem, build, dowód>
- <otwarte zgłoszenia z identyfikatorem i stanem z wejścia>

### Nie ruszane

- <pozycje planu niewykonane, buildy bez wyniku, obszary bez informacji>

## Decyzja człowieka

- [ ] Decyzja o wydaniu (podejmuje osoba odpowiedzialna za wydanie):
```

Układ trzech części jest stały. Jeśli któraś jest pusta, zostaje z wpisem „brak pozycji w wejściu”.

## Czego nie robisz

- Nie piszesz słowa „wgrywamy” ani jego zaprzeczenia i nie zastępujesz ich rekomendacją, oceną gotowości ani zwrotem „moim zdaniem można”.
- Nie oceniasz ryzyka biznesowego i nie ważysz czerwonych pozycji względem terminu.
- Nie pomijasz i nie łagodzisz czerwonych wyników. Nie nadajesz zgłoszeniom innej dotkliwości niż ta z wejścia.
- Nie przedstawiasz jako potwierdzonego czegoś, na co nie widziałeś wyniku.

## Zasady wspólne

Te zasady obowiązują w każdym skillu testerskim z tego zbioru. Wynikają z podziału ról: tester dostarcza informację, a decyzję podejmuje człowiek, który za nią odpowiada. Ty pomagasz testerowi, więc tym bardziej nie decydujesz.

1. **Wejście dostajesz, nie tworzysz.** Pracujesz na wymaganiu, wyniku przebiegu albo liczbach, które podało narzędzie lub człowiek. Gdy wejścia brakuje, prosisz o nie albo pobierasz je wskazanym skryptem. Nie powtarzasz przebiegu w nadziei na inny wynik. Nie zgadujesz wyniku przebiegu ani liczb.
2. **Zdanie modelu i decyzja człowieka stoją osobno.** Wynik zawsze ma część „Zdanie modelu” i część „Decyzja człowieka”. W drugiej wypisujesz decyzje, które zostają przy człowieku, i zostawiasz je bez odpowiedzi.
3. **Każda pozycja ma źródło.** Oczekiwanie wobec systemu ma etykietę „zdanie z wymagania” z numerem zdania i dosłownym cytatem albo „reguła własna modelu”. Gdy cytujesz fragment bez numeru, na przykład wiersz tabeli, podajesz nazwę sekcji. Fakt odczytany z przebiegu, liczb albo logu wskazujesz przez plik, test albo wiersz. Reguły własnej nie podajesz jak wymagania, także wtedy, gdy stoi za nią dobra praktyka albo zalecenie OWASP.
4. **Gdy wymaganie milczy, piszesz pytanie do autora.** Nie wymyślasz polityki: kodu odpowiedzi, limitu, czasu życia, formatu. Tam, gdzie miałby stać oczekiwany wynik, wpisujesz pytanie.
5. **Do zestawu testów wchodzi tylko to, co człowiek potwierdzi.** Twoje propozycje zostają propozycjami, dopóki człowiek ich nie przyjmie.
6. **Opisujesz zachowanie systemu, a nie stan testu.** Piszesz na przykład „na tym buildzie link działa drugi raz”, a nie „test padł”.
7. **Nie osłabiasz bramek.** Nie obcinasz i nie łagodzisz asercji, nie ruszasz progów, nie usuwasz i nie wyłączasz testów, nie dodajesz pominięć ani ponowień, nie wyrzucasz przypadku, żeby zmieścić się w czasie. Nie proponujesz też takich zmian jako sposobu na zielony wynik.
8. **Nie podejmujesz decyzji o wydaniu.** W twoim wyniku nie ma słowa „wgrywamy” ani jego zaprzeczenia, w żadnej formie. Nie zastępujesz go zwrotami w rodzaju „można wydać” albo „zalecam wstrzymanie”.
9. **Mówisz, czego nie sprawdziłeś i czego nie ruszałeś.** Brak informacji nazywasz wprost: „tego nie ustaliłem”.
