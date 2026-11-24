---
name: zgloszenie-defektu
description: Szkic zgłoszenia defektu z czerwonego wyniku testu. Opisuje zachowanie systemu (kroki, wynik faktyczny, wynik oczekiwany z cytatem wymagania, porównanie z buildem, na którym test jest zielony), a nie sam fakt niezaliczenia testu. Użyj, gdy tester ma czerwony test albo czerwony przebieg i chce z niego zgłoszenie, raport o defekcie albo opis błędu.
---

# Zgłoszenie defektu z czerwonego przebiegu

Zgłoszenie czyta ktoś, kto nie widział przebiegu. Potrzebuje wiedzieć, co system zrobił, co miał zrobić i jak to powtórzyć. Zdanie „test padł” mówi tylko o teście, więc nic mu nie daje. Twoim zadaniem jest przełożyć wynik przebiegu na opis zachowania systemu i zostawić człowiekowi ocenę, czy to defekt i co z nim dalej.

## Wejście

- Wynik testu na buildzie, na którym test jest czerwony.
- Wynik tego samego testu na buildzie, na którym jest zielony.
- Wymaganie, z którego wynika oczekiwany wynik.

W repozytorium qa-demo:

```powershell
python narzedzia/przebieg.py --port 8766
python narzedzia/przebieg.py --port 8765
python narzedzia/wymaganie.py reset-hasla
```

Wynik przebiegu zawiera dla każdego testu wymianę żądań i odpowiedzi z aplikacją. To z niej bierzesz kroki i wynik faktyczny. Jeśli brakuje któregoś z trzech wejść, poproś o nie albo napisz zgłoszenie bez tej części i zaznacz, czego zabrakło.

## Jak pracować

1. Znajdź w czerwonym wyniku miejsce, w którym odpowiedź systemu rozeszła się z oczekiwaniem testu. Odczytaj z wymiany, jakie żądania do niego doprowadziły.
2. Znajdź w wymaganiu zdanie, które mówi, jak system ma się zachować w tym miejscu. Zacytuj je dosłownie. Jeśli takiego zdania nie ma, napisz to: bez zdania z wymagania nie wiadomo, czy to defekt, i zamiast wyniku oczekiwanego stawiasz pytanie do autora.
3. Porównaj tę samą wymianę na obu buildach i opisz różnicę jednym zdaniem o zachowaniu systemu.
4. Zapisz kroki tak, żeby dało się je powtórzyć ręcznie, bez uruchamiania testu.
5. Wypisz, czego nie sprawdziłeś. Jeśli test zatrzymał się na pierwszej niespełnionej asercji, dalsze sprawdzenia się nie wykonały i nie wiesz, jaki dałyby wynik. Które to sprawdzenia, odczytasz z kodu testu albo z wymiany na buildzie, na którym test przeszedł.

## Format wyniku

```markdown
# Szkic zgłoszenia: <tytuł opisujący zachowanie systemu>

## Zdanie modelu

- Build: <numer i port builda, na którym test jest czerwony>
- Build do porównania: <numer i port>

### Kroki

1. <krok>
2. <krok>

### Wynik faktyczny

<co system zrobił na tym buildzie, z kodem i treścią odpowiedzi>

### Wynik oczekiwany

<co system ma zrobić> Źródło: zdanie z wymagania <numer>: „<cytat>”.

### Porównanie buildów

<jedno zdanie: na buildzie A system robi X, na buildzie B robi Y>

### Dowody

- <nazwa testu, plik, wynik na każdym buildzie, pliki z zapisem przebiegu>

### Fakty pomocne przy ocenie dotkliwości

- <co to zachowanie umożliwia albo uniemożliwia użytkownikowi; tylko to, co widać w wejściu>

### Czego nie sprawdziłem

- <...>

## Decyzja człowieka

- [ ] Czy to defekt:
- [ ] Dotkliwość:
- [ ] Priorytet:
- [ ] Czy zgłoszenie wychodzi i do kogo:
```

Tytuł i wynik faktyczny mówią o systemie, na przykład „na tym buildzie link działa drugi raz”. Nazwa testu trafia do dowodów.

## Czego nie robisz

- Nie wysyłasz zgłoszenia i nie zakładasz go w żadnym systemie.
- Nie nadajesz dotkliwości ani priorytetu. Wypisujesz fakty, które pomogą je ustalić.
- Nie podajesz domysłu o przyczynie w kodzie jako faktu. Jeśli masz przypuszczenie, oznacz je jako przypuszczenie.
- Nie zmieniasz testu ani oczekiwanego wyniku tak, żeby przebieg był zielony.

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
