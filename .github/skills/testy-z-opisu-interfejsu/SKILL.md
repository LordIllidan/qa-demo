---
name: testy-z-opisu-interfejsu
description: Sprawdzenia kontraktu z opisu interfejsu, na przykład OpenAPI, zestawione z wymaganiem. Dla każdej operacji wypisuje sprawdzenia kodów odpowiedzi, pól i ograniczeń, każde ze źródłem w opisie albo w wymaganiu, i wskazuje miejsca, w których opis i wymaganie mówią co innego. Użyj, gdy tester prosi o testy API z dokumentacji interfejsu, testy kontraktu, sprawdzenie zgodności opisu interfejsu z wymaganiem albo o listę sprawdzeń dla endpointów.
---

# Testy z opisu interfejsu

Opis interfejsu pisze zwykle zespół programistów, a wymaganie właściciel produktu. Oba dokumenty mówią o tych samych operacjach i nie zawsze mówią to samo. Test kontraktu napisany z samego opisu utrwali to, co zespół zaimplementował, także tam, gdzie wymaganie mówi coś innego. Twoim zadaniem jest wypisać sprawdzenia kontraktu ze źródłem i pokazać każdą niezgodność między opisem a wymaganiem jako pytanie. Który dokument ma rację, rozstrzyga człowiek.

## Wejście

- Opis interfejsu.
- Wymaganie, którego dotyczy interfejs.

W repozytorium qa-demo:

```powershell
python narzedzia/opis_interfejsu.py
python narzedzia/wymaganie.py reset-hasla
```

Pierwsze polecenie podaje operacje, pola żądania z ograniczeniami i odpowiedzi z kodami i polami. Jeśli tester wkleił opis interfejsu z własnego projektu, pracujesz na wklejonym tekście.

## Jak pracować

1. Dla każdej operacji z opisu wypisz sprawdzenia kontraktu: kod odpowiedzi dla każdego opisanego przypadku, wymagane pola żądania i odpowiedzi, ich typy i ograniczenia. Przy każdym podaj źródło: wiersz opisu, zdanie wymagania albo oba.
2. Zestaw opis z wymaganiem operacja po operacji. Niezgodność to:
   - kod, pole albo ograniczenie, które wymaganie podaje, a opis nie, albo odwrotnie,
   - ten sam przypadek z różnym wynikiem w opisie i w wymaganiu,
   - operacja w jednym dokumencie, której nie ma w drugim.
3. Przy każdej niezgodności zacytuj oba źródła i zapisz pytanie do autora wymagania albo do autora opisu. Sprawdzenie, którego dotyczy niezgodność, oznacz jako „wstrzymane do odpowiedzi”.
4. Wypisz, czego z opisu nie da się sprawdzić bez działającej aplikacji, i to, czego opis w ogóle nie mówi, na przykład o kodowaniu znaków albo o limitach żądań.
5. Przy każdym sprawdzeniu napisz, czy nadaje się do testu automatycznego. To reguła własna modelu.

## Format wyniku

```markdown
# Testy z opisu interfejsu: <tytuł i wersja opisu>

## Zdanie modelu

<jedno albo dwa zdania: ile sprawdzeń, ile niezgodności z wymaganiem i która jest najważniejsza>

### Sprawdzenia kontraktu

| Nr | Operacja | Sprawdzenie | Oczekiwanie | Źródło | Stan |
| --- | --- | --- | --- | --- | --- |
| 1 | <metoda i ścieżka> | <kod, pole albo ograniczenie> | <wartość> | opis: <wiersz>; wymaganie: <numer>: „<cytat>” | gotowe albo wstrzymane do odpowiedzi |

### Niezgodności opisu i wymagania

| Nr | Operacja | Opis interfejsu | Wymaganie | Pytanie |
| --- | --- | --- | --- | --- |
| N1 | <...> | <cytat> | <numer>: „<cytat>” albo „nic” | <pytanie i do kogo> |

### Czego opis nie mówi

- <...>

### Czego nie sprawdziłem

- <na przykład: nie wysyłałem żądań do aplikacji>

## Decyzja człowieka

- [ ] Który dokument rozstrzyga każdą niezgodność albo komu ją zgłosić:
- [ ] Które sprawdzenia wchodzą do zestawu, ręcznie czy automatycznie:
```

## Czego nie robisz

- Nie rozstrzygasz, który dokument ma rację.
- Nie bierzesz oczekiwania z odpowiedzi aplikacji. Nie wysyłasz żądań, żeby sprawdzić, który dokument zgadza się z buildem.
- Nie poprawiasz opisu interfejsu ani wymagania.
- Nie dopisujesz kodów, pól ani ograniczeń, których nie ma w żadnym z dokumentów. Brak zapisujesz jako pytanie.
- Nie piszesz kodu testów.

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
