---
name: przebieg-api
description: Odczyt wyniku wywołań API albo ułożenie przypadków API z opisu interfejsu i wymagania. Każde wywołanie ma żądanie, status i treść odpowiedzi. Użyj, gdy tester prosi o test API, wynik wywołań endpointów, przypadki do interfejsu REST albo o porównanie odpowiedzi z opisem OpenAPI.
---

# Przebieg wywołań API

Odpowiedź API jest zgodna z opisem interfejsu albo z wymaganiem, a te dwa dokumenty nie muszą mówić tego samego. Dostajesz wykonane wywołania: metodę, ścieżkę, dane, status i treść. Mówisz, co system odpowiedział i z którego dokumentu wynika oczekiwanie. Przypadki, których przebieg nie wykonał, szkicujesz i zostawiasz człowiekowi.

## Wejście

- Wynik wywołań API.
- Opis interfejsu.
- Wymaganie.

W repozytorium qa-demo:

```powershell
python narzedzia/przebieg_api.py --port <port builda>
python narzedzia/opis_interfejsu.py
python narzedzia/wymaganie.py reset-hasla
```

Pierwsze polecenie wymaga działającej aplikacji.

## Jak pracować

1. Dla każdego wywołania zapisz status i treść odpowiedzi jako fakt z przebiegu.
2. Znajdź oczekiwanie w opisie interfejsu i w wymaganiu. Zacytuj oba, gdy oba o tym mówią. Gdy mówią co innego, pokaż oba i zapisz pytanie. Nie wybierasz, który dokument ma rację.
3. Wypisz wywołania, których przebieg nie wykonał, a które wynikają z opisu albo z wymagania. To propozycje, z numerem zdania albo wierszem opisu.
4. Napisz, czego przebieg nie obejmuje.

## Format wyniku

```markdown
# Przebieg API: <build>

## Zdanie modelu

<jedno albo dwa zdania: co system odpowiedział i gdzie opis albo wymaganie mówi co innego>

### Wywołania

| Id | Żądanie | Odpowiedź | Źródło oczekiwania |
| --- | --- | --- | --- |
| <id> | <metoda i ścieżka> | <status i treść> | opis: <wiersz>; zdanie z wymagania <numer>: „<cytat>” albo „milczy” |

### Wywołania, których przebieg nie wykonał

| Nr | Żądanie | Oczekiwanie | Źródło |
| --- | --- | --- | --- |
| A1 | <...> | <...> | <...> |

### Czego nie sprawdziłem

- <...>

## Decyzja człowieka

- [ ] Który dokument rozstrzyga rozbieżność opisu i wymagania:
- [ ] Które propozycje wywołań dopisać do pliku przebiegu:
```

## Czego nie robisz

- Nie wysyłasz własnych żądań. Przebieg podaje skrypt.
- Nie uznajesz statusu z przebiegu za oczekiwany wynik. Oczekiwanie bierzesz z opisu albo z wymagania.
- Nie poprawiasz opisu interfejsu ani wymagania.
- Nie nazywasz odpowiedzi defektem. Mówisz, co system odpowiedział i co mówi dokument.

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
