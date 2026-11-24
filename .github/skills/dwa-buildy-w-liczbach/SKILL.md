---
name: dwa-buildy-w-liczbach
description: Jedno zdanie o tym, co zmieniło się w liczbach między dwoma buildami. Sprawdza zgodność profilu obciążenia, zestawia czasy odpowiedzi każdej ścieżki, odnosi je do progów i niczego w progach nie zmienia. Użyj, gdy tester ma liczby z dwóch buildów (czasy odpowiedzi, błędy, progi, profil) i pyta o regresję wydajności, porównanie buildów albo o to, co się zmieniło.
---

# Dwa buildy w liczbach

Dwie tabele liczb trudno przeczytać w biegu, a osoba decydująca o wydaniu potrzebuje jednego zdania. Twoim zadaniem jest to zdanie ułożyć i pokazać liczby, na których stoi. Porównanie ma sens tylko wtedy, gdy oba buildy dostały to samo obciążenie, dlatego zaczynasz od profilu. Próg jest kryterium ustalonym przez ludzi: odnosisz do niego liczby, ale go nie dotykasz.

## Wejście

Liczby dwóch buildów: profil obciążenia, progi i metryki każdej ścieżki. W repozytorium qa-demo podaje je polecenie:

```powershell
python narzedzia/liczby.py
```

Liczby pochodzą z gotowych plików wyników. Narzędzie niczego nie mierzy. Opisujesz je jako liczby z tych plików i nie przypisujesz im narzędzia pomiarowego, którego wejście nie wymienia.

## Jak pracować

1. Porównaj profil obu buildów parametr po parametrze. Jeśli profile się różnią, napisz, że porównanie nie jest uprawnione, wskaż różnice i na tym zakończ ocenę liczb.
2. Dla każdej ścieżki zestaw te same metryki z obu buildów. Podaj wartości z wejścia; zaokrąglenie zaznacz słowem „około”.
3. Odnieś liczby do progów z wejścia: która metryka której ścieżki mieści się w progu, a która go przekracza. To stwierdzenie faktu, a nie ocena, czy próg jest dobry.
4. Sprawdź liczbę żądań i odsetek błędów. Jeśli różnią się między buildami, powiedz o tym, bo to wpływa na odczyt czasów.
5. Ułóż jedno zdanie: co zwolniło albo przyspieszyło i o ile, co stoi w miejscu, czy profil był ten sam, czego dotyczy zmiana.

## Format wyniku

```markdown
# Dwa buildy w liczbach: <build A> i <build B>

## Zdanie modelu

<jedno zdanie: ścieżka X zmieniła się z około A ms do około B ms, ścieżka Y stoi, profil był ten sam, więc to zmiana na ścieżce X>

### Profil

<„ten sam w obu buildach” albo lista różnic; przy różnicach: porównanie nie jest uprawnione>

### Liczby

| Ścieżka | Metryka | <build A> | <build B> | Próg | Względem progu |
| --- | --- | --- | --- | --- | --- |
| <ścieżka> | <metryka> | <wartość> | <wartość> | <próg z wejścia> | <mieści się albo przekracza, dla każdego builda> |

### Progi

Progi zostają bez zmian: <wypisz progi z wejścia>.

### Czego nie wiem

- <na przykład: przyczyny w kodzie, tego, czy oba pomiary zrobiono w tym samym środowisku>

## Decyzja człowieka

- [ ] Czy ta zmiana blokuje wydanie:
- [ ] Czy powstaje zgłoszenie:
- [ ] Czy potrzebna jest dalsza diagnoza:
```

## Czego nie robisz

- Nie zmieniasz progów i nie proponujesz ich podniesienia, żeby wynik się zmieścił.
- Nie porównujesz liczb, gdy profile się różnią.
- Nie orzekasz o przyczynie w kodzie. Liczby mówią, gdzie i o ile, a nie dlaczego.
- Nie pomijasz metryki, która wygląda źle, i nie uśredniasz ścieżek ze sobą.

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
