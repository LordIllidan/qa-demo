---
name: szkic-testu-automatycznego
description: Szkic testu automatycznego dla przypadku, który człowiek potwierdził. Pisze kod w konwencji istniejącego zestawu, każdą asercję wiąże ze zdaniem wymagania i mówi, czego test nie sprawdza; kodu nie zapisuje w zestawie przed przyjęciem. Użyj, gdy tester prosi o napisanie albo zautomatyzowanie testu dla potwierdzonego przypadku, o zamianę przypadku ręcznego na test automatyczny albo o szkic skryptu testowego.
---

# Szkic testu automatycznego

Model szybko pisze kod testu. Ryzyko leży w tym, skąd bierze oczekiwany wynik. Jeśli uruchomi kroki na buildzie i wpisze do asercji to, co build zwrócił, test będzie zielony także wtedy, gdy build ma defekt, i utrwali ten defekt jako zachowanie oczekiwane. Dlatego piszesz test tylko dla przypadku, który człowiek potwierdził, a każda asercja ma źródło w wymaganiu. Kod jest propozycją do przeglądu, tak jak kod każdego innego autora.

## Wejście

- Przypadek testowy potwierdzony przez człowieka: kroki, dane i oczekiwany wynik. Tester podaje go w prośbie albo wskazuje numer przypadku z wcześniejszego wyniku i potwierdza, że ten przypadek wchodzi do zestawu.
- Wymaganie.
- Istniejące testy i ich zaplecze.

W repozytorium qa-demo:

```powershell
python narzedzia/wymaganie.py reset-hasla
python narzedzia/lista_testow.py
```

Kod testów leży w katalogu `testy`. Wspólne zaplecze, czyli klient aplikacji i przygotowanie konta, jest w pliku `testy/conftest.py`. Jeśli tester nie podał przypadku albo nie potwierdził go, zapytaj. Testu dla przypadku niepotwierdzonego nie piszesz.

## Jak pracować

1. Zapisz przypadek tak, jak go potwierdzono. Dla oczekiwanego wyniku znajdź zdanie wymagania i zacytuj je. Jeśli wymaganie go nie podaje, a człowiek podał go w rozmowie, oznacz źródło jako „ustalenie człowieka z rozmowy”. Jeśli nie podał, zapytaj.
2. Sprawdź na liście testów i w kodzie, czy taki test już istnieje. Jeśli istnieje, powiedz to i nie pisz drugiego.
3. Przeczytaj istniejące testy i zaplecze. Użyj kroków, nazw i układu, które już tam są. Jeśli zaplecze nie ma potrzebnego kroku, napisz, czego brakuje. Zmianę zaplecza proponujesz osobno.
4. Napisz test, który sprawdza jedną rzecz. Asercja stoi po każdym kroku, dla którego przypadek podaje oczekiwany wynik. Jeśli zdanie wymagania mówi o skutku, sprawdź skutek, a nie tylko kod odpowiedzi.
5. Dla każdej asercji podaj, co sprawdza i z którego zdania wymagania pochodzi.
6. Wypisz, czego test nie sprawdza: części zdania wymagania bez asercji, kroki przypadku pominięte w kodzie, założenia o danych.

Po przyjęciu kodu przez człowieka zapisujesz dokładnie ten kod, który przyjął, w nowym pliku w katalogu `testy`. Nazwę pliku podaje człowiek; jeśli jej nie podał, zaproponuj ją i zapytaj. Test uruchamiasz na wyraźne polecenie człowieka:

```powershell
python narzedzia/przebieg.py --port <port builda> --zestaw <plik z testem> --test <nazwa testu>
```

Wynik opisujesz zachowaniem systemu. Czerwony wynik nie jest powodem do zmiany asercji: jeśli test jest czerwony, piszesz, co system odpowiedział i co miał odpowiedzieć według wymagania.

## Format wyniku

```markdown
# Szkic testu: <nazwa testu>

## Zdanie modelu

<jedno zdanie: co test sprawdza i z którego zdania wymagania to wynika>

### Przypadek potwierdzony przez człowieka

- Kroki: <...>
- Dane: <...>
- Oczekiwany wynik: <...>
- Potwierdzenie: <kto i gdzie potwierdził: prośba w rozmowie albo numer przypadku z wcześniejszego wyniku>

### Kod

<kod testu w bloku kodu, w konwencji istniejącego zestawu>

### Asercje i ich źródło

| Asercja | Co sprawdza | Źródło |
| --- | --- | --- |
| <wiersz kodu> | <zachowanie systemu> | zdanie z wymagania <numer>: „<cytat>” |

### Czego ten test nie sprawdza

- <część zdania wymagania bez asercji, pominięty krok, założenie o danych>

### Czego nie zrobiłem

- <na przykład: kodu nie zapisałem w katalogu testy i nie uruchomiłem go na żadnym buildzie>

## Decyzja człowieka

- [ ] Czy kod wchodzi do zestawu po przeglądzie:
- [ ] Na których buildach go uruchomić:
```

## Czego nie robisz

- Nie piszesz testu dla przypadku, którego człowiek nie potwierdził.
- Nie bierzesz oczekiwanego wyniku z odpowiedzi aplikacji. Nie uruchamiasz kroków po to, żeby zobaczyć, co build zwróci, i wpisać to do asercji.
- Nie zapisujesz kodu w zestawie przed przyjęciem i nie scalasz zmian.
- Nie zmieniasz istniejących testów ani wspólnego zaplecza.
- Nie dodajesz pominięć, ponowień ani oczekiwania o stałej długości po to, żeby test był zielony.
- Nie zmieniasz asercji po czerwonym wyniku.

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
