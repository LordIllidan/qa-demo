---
name: dostepnosc-strony
description: Inwentarz HTML strony pod kątem dostępności. Język, nagłówki, etykiety pól, tekst przycisków i obrazki bez alt, zestawione z tym, co o stronie mówi wymaganie. Użyj, gdy tester prosi o dostępność, a11y, etykiety formularza, audyt strony albo o to, co na stronie da się sprawdzić bez przeglądarki.
---

# Dostępność strony

Automatyczny spis znaczników nie jest audytem dostępności. Dostajesz inwentarz: język, nagłówki, pola i etykiety, przyciski, obrazki. Mówisz, co w nim jest, i czego wymaganie o stronie nie mówi. Werdyktu „strona jest dostępna” nie wydajesz.

## Wejście

- Inwentarz HTML jednej albo kilku stron.
- Wymaganie, jeśli funkcja je ma.

W repozytorium qa-demo:

```powershell
python narzedzia/dostepnosc.py --port <port builda>
python narzedzia/wymaganie.py reset-hasla
```

Skrypt wymaga działającej aplikacji. Czyta HTML, nie uruchamia przeglądarki i nie liczy kontrastu, fokusu ani czytników ekranu.

## Jak pracować

1. Przepisz fakty z inwentarza: język, nagłówki, pola bez etykiety, przyciski bez tekstu, obrazki bez alt.
2. Dla każdego faktu wskaż, czy wymaganie o nim mówi. Gdy milczy, zapisz pytanie do autora, a nie próg z normy.
3. Wypisz, czego inwentarz nie obejmuje. To nie jest lista braków strony, tylko lista granic skryptu.
4. Nie nadawaj stronie oceny procentowej ani poziomu zgodności.

## Format wyniku

```markdown
# Dostępność: <strony i build>

## Zdanie modelu

<jedno albo dwa zdania: co inwentarz pokazuje i że wymaganie o dostępności strony milczy albo co mówi>

### Fakty z inwentarza

| Strona | Fakt | Źródło |
| --- | --- | --- |
| <ścieżka> | <fakt> | inwentarz; zdanie z wymagania <numer>: „<cytat>” albo „wymaganie milczy” |

### Pytania do autora

- <pytanie>

### Czego inwentarz nie obejmuje

- <kontrast, fokus, czytnik, powiększenie>

## Decyzja człowieka

- [ ] Które pytania idą do autora:
- [ ] Czy potrzebny jest audyt z przeglądarką i czytnikiem, i kto go robi:
```

## Czego nie robisz

- Nie ogłaszasz, że strona spełnia normę dostępności. Inwentarz do tego nie wystarcza.
- Nie wymyślasz progów kontrastu ani obowiązującego poziomu normy.
- Nie poprawiasz HTML.
- Nie zastępujesz audytu ręcznego spisem znaczników.

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
