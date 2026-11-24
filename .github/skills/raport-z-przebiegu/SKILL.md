---
name: raport-z-przebiegu
description: Krótki raport z jednego przebiegu testów dla osoby spoza zespołu. Mówi, co sprawdzono, co system zrobił i czego przebieg nie obejmuje, bez decyzji o wydaniu. Użyj, gdy tester prosi o raport z przebiegu, podsumowanie dla kierownika, notatkę ze sprintu albo o opis wyniku testów językiem zachowania systemu.
---

# Raport z jednego przebiegu

Osoba spoza zespołu czyta „5 zaliczonych, 1 niezaliczony” i nie wie, co system zrobił. Raport ma mówić o zachowaniu systemu, o tym, co przebieg objął, i o tym, czego nie objął. Nie jest kartą przed wgraniem i nie kończy się decyzją o wydaniu.

## Wejście

- Wynik jednego przebiegu: build, zestaw, liczby i szczegóły testów.

W repozytorium qa-demo:

```powershell
python narzedzia/przebieg.py --port <port builda>
```

Skrypt wymaga działającej aplikacji. Innych przebiegów, liczb obciążenia i listy zgłoszeń ten raport nie dostaje. Gdyby tester o nie pytał, napisz, że ich nie masz.

## Jak pracować

1. Napisz, jaki build i jaki zestaw objął przebieg. Liczby przepisz z wejścia.
2. Dla testu z wynikiem innym niż zaliczony opisz zachowanie systemu z wymiany żądań, nie stan testu. Wskaż test i krok wymiany.
3. Dla testów zaliczonych podaj jednym zdaniem, jakiego zachowania dotyczą, na podstawie opisów testów. Nie przepisuj każdego żądania.
4. Wypisz, czego ten jeden przebieg nie obejmuje.

## Format wyniku

```markdown
# Raport z przebiegu: build <numer>, <zestaw>

## Zdanie modelu

<jedno albo dwa zdania o zachowaniu systemu na tym buildzie, bez słowa o wydaniu>

### Co przebieg objął

- Build, zestaw, liczby: <przepisane z wejścia>

### Co system zrobił

| Test | Zachowanie | Źródło |
| --- | --- | --- |
| <nazwa> | <zachowanie systemu> | przebieg, test <nazwa>, wymiana <krok> albo opis testu |

### Czego przebieg nie obejmuje

- <...>

## Decyzja człowieka

- [ ] Czy raport wychodzi do odbiorcy spoza zespołu i w jakiej postaci:
- [ ] Czy potrzebny jest drugi przebieg albo inne wejście, zanim raport wyjdzie:
```

## Czego nie robisz

- Nie piszesz karty przed wgraniem i nie podejmujesz decyzji o wydaniu. Słowa „wgrywamy” w raporcie nie ma.
- Nie klasyfikujesz awarii na produkt, test i środowisko. To osobne zagadnienie.
- Nie piszesz zgłoszenia. Raport może wskazać zachowanie, które zgłoszenia wymaga, i zatrzymać się na decyzji człowieka.
- Nie powtarzasz przebiegu.

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
