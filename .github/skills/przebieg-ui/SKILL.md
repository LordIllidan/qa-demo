---
name: przebieg-ui
description: Odczyt przebiegu interfejsu wykonanego Playwrightem albo szkic sprawdzeń interfejsu z wymagania. Każdy krok przebiegu ma selektor i tekst ze strony. Użyj, gdy tester prosi o test Playwright, test UI, test w przeglądarce, wynik przebiegu strony albo o to, jakie sprawdzenia interfejsu wynikają z wymagania.
---

# Przebieg interfejsu w Playwright

Test interfejsu łatwo pomylić z testem API: przeglądarka pokazuje tekst, a wymaganie mówi o zachowaniu. Model dostaje przebieg już ułożony w tabeli, a nie surowy log Playwrighta. Z przebiegu mówi, co strona pokazała. Sprawdzenia, których przebieg nie wykonał, szkicuje z wymagania i zostawia człowiekowi.

## Wejście

- Wynik przebiegu interfejsu: kroki, selektory i tekst ze strony.
- Wymaganie.

W repozytorium qa-demo:

```powershell
python narzedzia/przebieg_ui.py --port <port builda>
python narzedzia/wymaganie.py reset-hasla
```

Przebieg wymaga działającej aplikacji i zainstalowanego Playwrighta. Jeśli tester prosi tylko o szkic sprawdzeń, a przebiegu nie ma, pracujesz na wymaganiu i piszesz, że przebiegu nie dostałeś.

## Jak pracować

1. Dla każdego kroku przebiegu zapisz, co strona pokazała. To fakt z przebiegu, ze wskazaniem numeru kroku.
2. Zestaw tekst ze strony ze zdaniem wymagania. Zacytuj zdanie. Gdy wymaganie o tym milczy, zapisz pytanie, a nie werdykt.
3. Wypisz sprawdzenia interfejsu, których ten przebieg nie wykonał, a które wynikają ze zdań wymagania. Przy każdym: zdanie, proponowany krok i selektor opisany słowami strony (rola, etykieta, tekst), nie wymyślony identyfikator. To propozycja, nie test.
4. Napisz, czego przebieg nie obejmuje: drugiej strony, drugiego builda, klawiatury, szerokości okna.

## Format wyniku

```markdown
# Przebieg interfejsu: <build i adres>

## Zdanie modelu

<jedno albo dwa zdania: co strona pokazała i które zdanie wymagania to dotyczy>

### Kroki przebiegu

| Krok | Co strona pokazała | Źródło |
| --- | --- | --- |
| <numer i czynność> | <tekst ze strony> | przebieg, krok <numer>; zdanie z wymagania <numer>: „<cytat>” albo „wymaganie milczy” |

### Szkic sprawdzeń, których przebieg nie wykonał

| Nr | Sprawdzenie | Zdanie wymagania | Proponowany krok |
| --- | --- | --- | --- |
| U1 | <...> | <numer>: „<cytat>” | <krok słowami strony> |

### Czego nie sprawdziłem

- <...>

## Decyzja człowieka

- [ ] Które szkice sprawdzeń wchodzą do testu Playwright i kto je dopisuje:
- [ ] Czy przebieg powtórzyć na innym buildzie:
```

## Czego nie robisz

- Nie oceniasz przebiegu po tym, że Playwright doszedł do końca. Mówisz, co strona pokazała.
- Nie zmieniasz selektorów w teście i nie „naprawiasz” lokalizatora, który przestał pasować.
- Nie uruchamiasz przeglądarki sam. Przebieg podaje skrypt.
- Nie dopisujesz kroku, którego nie ma ani w przebiegu, ani w wymaganiu, jako wykonanego.

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
