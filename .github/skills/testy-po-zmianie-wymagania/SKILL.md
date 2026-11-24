---
name: testy-po-zmianie-wymagania
description: Przegląd testów po zmianie wymagania. Zestawia zdania zmienione, dodane i usunięte z istniejącymi testami i mówi, który test trzeba poprawić, który przestaje pasować do wymagania, które nowe zdania nie mają testu i o co zapytać autora. Testów nie zmienia. Użyj, gdy tester prosi o przegląd testów po zmianie historyjki albo kryteriów akceptacji, o utrzymanie testów przy nowej wersji wymagania albo o listę testów do poprawy.
---

# Testy po zmianie wymagania

Gdy wymaganie się zmienia, testy dalej sprawdzają starą wersję. Część z nich stanie się czerwona dopiero na buildzie z nową wersją i wtedy łatwo „naprawić” je tak, żeby przeszły, zamiast sprawdzić, czy zmiana w teście wynika ze zmiany wymagania. Inne zostaną zielone, choć nie sprawdzają już tego, co wymaganie mówi. Twoim zadaniem jest przed zmianą w produkcie wskazać, których testów dotyka każde zmienione zdanie i co z tego wynika. Opis zmiany od autora jest wejściem, a nie prawdą: porównaj go z tekstem obu wersji.

## Wejście

- Obie wersje wymagania i ich porównanie zdanie po zdaniu.
- Opis zmiany od autora, jeśli jest.
- Lista testów z opisami i kod testów razem ze wspólnym zapleczem.

W repozytorium qa-demo:

```powershell
python narzedzia/zmiana_wymagania.py
```

Skrypt podaje opis zmiany, tabelę zdań i wierszy interfejsu w obu wersjach, różnicę tekstu i listę testów. Kod testów leży w katalogu `testy`, wspólne zaplecze w pliku `testy/conftest.py`. Obecne buildy realizują wersję sprzed zmiany, więc przebieg na nich nie mówi nic o nowej wersji.

## Jak pracować

1. Zestaw opis zmiany od autora z tabelą zdań. Wypisz zmiany, których opis nie wymienia, i to, co opis wymienia, a czego w tekście nie ma.
2. Dla każdego zdania zmienionego, dodanego albo usuniętego, także wiersza interfejsu, przeczytaj kod testów i wskaż testy, których dotyczy. Test dotyczy zdania, gdy sprawdza zachowanie z tego zdania albo gdy jego kroki lub dane podlegają nowej regule, choć test sprawdza coś innego.
3. Każdemu testowi nadaj jeden stan:
   - **do poprawy**: przy nowej wersji krok, dane albo asercja testu kłóci się z wymaganiem; wskaż wiersz i zdanie,
   - **przestaje pasować**: test sprawdza zachowanie, którego nowa wersja już nie wymaga,
   - **bez wpływu**: żadna zmiana go nie dotyczy,
   - **do sprawdzenia**: nie da się tego ustalić z kodu; napisz, czego brakuje.
4. Wypisz zdania nowej wersji, których nie sprawdza żaden test.
5. Gdy nowa wersja nie podaje oczekiwanego wyniku, na przykład kodu odpowiedzi albo chwili, od której liczy się czas, zapisz pytanie do autora.

Propozycja poprawki testu to opis: co zmienić i z którego zdania to wynika. Kodu nie piszesz; nowy test dla potwierdzonego przypadku powstaje w osobnym kroku, według skilla `szkic-testu-automatycznego`.

## Format wyniku

```markdown
# Testy po zmianie wymagania: <identyfikator wymagania, wersja przed i po>

## Zdanie modelu

<jedno albo dwa zdania: ile testów trzeba poprawić, ile nowych zdań nie ma testu i czy opis zmiany obejmuje wszystkie zmiany>

### Opis zmiany a tekst wymagania

- <zmiana z tekstu, której opis nie wymienia, albo pozycja opisu bez pokrycia w tekście>

### Testy a zmienione zdania

| Test | Stan | Zdanie | Co się kłóci albo dlaczego bez wpływu | Proponowana poprawka |
| --- | --- | --- | --- | --- |
| <nazwa> | <stan z listy> | <numer>: „<cytat z nowej wersji>” | <wiersz kodu i powód> | <opis zmiany albo „–”> |

### Zdania bez testu

- <numer>: „<cytat>”

### Pytania do autora

- <pytanie, które daje sprawdzalną odpowiedź>

### Czego nie sprawdziłem

- <na przykład: nie uruchamiałem testów; obecne buildy realizują wersję sprzed zmiany>

## Decyzja człowieka

- [ ] Które testy poprawić i kiedy, przed zmianą w produkcie czy razem z nią:
- [ ] Które testy usunąć albo zostawić:
- [ ] Które pytania idą do autora:
- [ ] Dla których zdań bez testu powstaną przypadki:
```

## Czego nie robisz

- Nie zmieniasz testów ani zaplecza i nie piszesz kodu poprawek.
- Nie usuwasz testu dlatego, że przestaje pasować. Usunięcie jest decyzją człowieka.
- Nie uruchamiasz testów na obecnych buildach jako dowodu zgodności z nową wersją.
- Nie przyjmujesz opisu autora za pełny, jeśli tekst wersji mówi co innego.
- Nie wpisujesz oczekiwanego wyniku, którego nowa wersja nie podaje.

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
