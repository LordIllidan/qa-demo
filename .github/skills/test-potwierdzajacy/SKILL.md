---
name: test-potwierdzajacy
description: Ponowny test po poprawce. Zestawia zgłoszenie defektu z wynikiem tego samego testu na buildzie z poprawką, mówi, czy kroki ze zgłoszenia dają teraz wynik oczekiwany, i wypisuje, czego wokół poprawki nie sprawdzono. Zgłoszenia nie zamyka. Użyj, gdy tester ma zgłoszenie i nowy build i pyta, czy defekt ustąpił, czy poprawka działa albo czy można zamknąć zgłoszenie.
---

# Ponowny test po poprawce

Po poprawce tester powtarza test, który pokazał defekt, i sprawdza, czy opisane zachowanie ustąpiło. Twoim zadaniem jest zestawić zgłoszenie z nowym wynikiem krok po kroku. Zielony test potwierdza tylko to, co sprawdza, więc równie ważna jest druga połowa wyniku: czego wokół poprawki nikt nie sprawdził. Zamknięcie zgłoszenia jest decyzją człowieka.

## Wejście

- Zgłoszenie defektu z krokami, wynikiem faktycznym i oczekiwanym.
- Wynik tego samego testu na buildzie z poprawką.

W repozytorium qa-demo zgłoszenie leży w pliku `material/zgloszenia/ZGL-101.md`, a build z poprawką działa na porcie 8767:

```powershell
python narzedzia/przebieg.py --port 8767 --test test_link_dziala_jeden_raz
```

## Jak pracować

1. Odczytaj ze zgłoszenia kroki, wynik faktyczny, wynik oczekiwany i build, na którym defekt zgłoszono.
2. Sprawdź w nowym wyniku numer builda. Ma to być inny build niż w zgłoszeniu. Jeśli jest ten sam, powiedz o tym i nie wyciągaj wniosku o poprawce.
3. Przejdź po krokach zgłoszenia i znajdź dla każdego odpowiadające mu żądanie w wymianie z aplikacją. Zapisz, co system odpowiedział teraz.
4. Sformułuj jedno zdanie: kroki ze zgłoszenia dają teraz wynik oczekiwany albo nie dają.
5. Wypisz, czego ten wynik nie obejmuje: których kroków zgłoszenia test nie wykonuje, których innych testów nie uruchomiono na nowym buildzie, których zachowań w pobliżu poprawki nikt nie sprawdził.

## Format wyniku

```markdown
# Ponowny test: <identyfikator zgłoszenia> na buildzie <numer i port>

## Zdanie modelu

<jedno zdanie: na buildzie X kroki ze zgłoszenia dają wynik oczekiwany albo nadal dają wynik opisany w zgłoszeniu>

| Krok ze zgłoszenia | Wynik oczekiwany | Wynik na buildzie ze zgłoszenia | Wynik na buildzie z poprawką |
| --- | --- | --- | --- |
| <krok> | <ze zgłoszenia> | <ze zgłoszenia> | <z wymiany w nowym wyniku> |

### Czego wokół poprawki nie sprawdzono

- <...>

## Decyzja człowieka

- [ ] Zgłoszenie <identyfikator>: zamknąć czy otworzyć ponownie:
- [ ] Czy przed tą decyzją wykonać dodatkowe sprawdzenia, a jeśli tak, to które:
```

## Czego nie robisz

- Nie zamykasz zgłoszenia i nie zmieniasz jego stanu.
- Nie piszesz, że defekt jest naprawiony. Piszesz, co system zrobił w tym teście na tym buildzie.
- Nie rozszerzasz wniosku na zachowania, których test nie sprawdza.
- Nie zmieniasz testu, żeby pasował do nowego builda.

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
