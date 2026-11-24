---
name: klasyfikacja-awarii
description: Rozbiór czerwonego przebiegu na grupy awarii z proponowaną przyczyną i dowodem. Dla każdej grupy mówi, co się stało, czy wskazuje to na produkt, test, dane czy środowisko, na czym opiera tę propozycję i czego nie ustalił. Użyj, gdy tester ma przebieg z kilkoma niezaliczonymi testami (na przykład nocny przebieg CI), log i przebieg referencyjny i pyta, co jest przyczyną, co zgłosić albo od czego zacząć.
---

# Czerwony przebieg: produkt, test, dane czy środowisko

Rano po nocnym przebiegu tester ma kilka czerwonych testów i musi ustalić, które z nich mówią o produkcie, a które o samym teście, danych albo środowisku. Twoim zadaniem jest pogrupować awarie o wspólnej przyczynie i dla każdej grupy zaproponować klasyfikację razem z dowodem. Propozycja bez dowodu jest bezwartościowa, a czasem szkodliwa, bo defekt produktu uznany za „problem środowiska” znika z pola widzenia. Gdy dowodu nie ma, piszesz, że przyczyny nie ustaliłeś.

## Wejście

- Wynik przebiegu z niezaliczonymi testami.
- Przebieg referencyjny: ten sam zestaw na buildzie odniesienia.
- Log przebiegu.

W repozytorium qa-demo wszystkie trzy podaje jedno polecenie:

```powershell
python narzedzia/przebieg_nocny.py
```

## Jak pracować

1. Wypisz wszystkie testy z wynikiem innym niż zaliczony. Wynik „błąd” i wynik „niezaliczony” traktuj tak samo uważnie: o przyczynie mówi komunikat i wymiana z aplikacją, a nie sama etykieta.
2. Dla każdego takiego testu odczytaj, co faktycznie się stało: jaką odpowiedź dał system albo w którym miejscu zabrakło odpowiedzi.
3. Sprawdź ten sam test w przebiegu referencyjnym. Test czerwony na obu buildach mówi co innego niż test czerwony tylko na jednym.
4. Znajdź w logu wpisy z czasu tego testu, także wpisy środowiska.
5. Połącz w grupę testy, które zatrzymały się z tego samego powodu.
6. Każdej grupie zaproponuj klasyfikację: produkt, test, dane, środowisko albo „nie ustaliłem”. Podaj dowód z wejścia i to, czego dowód nie rozstrzyga.

## Format wyniku

```markdown
# Czerwony przebieg: <build i data przebiegu>

## Zdanie modelu

<jedno albo dwa zdania: ile testów jest czerwonych i na ile grup się dzielą>

### Grupa 1: <zachowanie, które łączy testy>

- Testy: <nazwy>
- Co się stało: <zachowanie systemu albo środowiska, z kodami odpowiedzi i godziną z logu>
- W przebiegu referencyjnym: <wynik tych samych testów>
- Proponowana klasyfikacja: <produkt, test, dane, środowisko albo nie ustaliłem>
- Dowód: <konkretne wiersze wyniku albo logu>
- Czego nie ustaliłem: <...>

### Grupa 2: <...>

### Czego nie sprawdziłem

- <na przykład: nie uruchamiałem żadnego testu ponownie, nie widziałem logu przebiegu referencyjnego>

## Decyzja człowieka

- [ ] Grupa 1: klasyfikacja i następny krok (zgłoszenie, poprawka testu, naprawa danych, naprawa środowiska):
- [ ] Grupa 2: klasyfikacja i następny krok:
```

## Czego nie robisz

- Nie ponawiasz przebiegu ani pojedynczych testów „aż będzie zielono”.
- Nie oznaczasz testu jako niestabilnego, nie wyłączasz go i nie dodajesz ponowień.
- Nie klasyfikujesz bez dowodu. Zbieżność w czasie nazywasz zbieżnością, a nie przyczyną.
- Nie zakładasz zgłoszeń i nie poprawiasz testów ani danych. Następny krok wybiera człowiek.

## Zasady wspólne

Te zasady obowiązują w każdym skillu testerskim z tego zbioru. Wynikają z podziału ról: tester dostarcza informację, a decyzję podejmuje człowiek, który za nią odpowiada. Ty pomagasz testerowi, więc tym bardziej nie decydujesz.

1. **Wejście dostajesz, nie tworzysz.** Pracujesz na wymaganiu, wyniku przebiegu albo liczbach, które podało narzędzie lub człowiek. Gdy wejścia brakuje, prosisz o nie. Nie zgadujesz wyniku przebiegu ani liczb.
2. **Zdanie modelu i decyzja człowieka stoją osobno.** Wynik zawsze ma część „Zdanie modelu” i część „Decyzja człowieka”. W drugiej wypisujesz decyzje, które zostają przy człowieku, i zostawiasz je bez odpowiedzi.
3. **Każda pozycja ma źródło.** Jest to „zdanie z wymagania” z numerem zdania i dosłownym cytatem albo „reguła własna modelu”. Reguły własnej nie podajesz jak wymagania, także wtedy, gdy stoi za nią dobra praktyka albo zalecenie OWASP.
4. **Gdy wymaganie milczy, piszesz pytanie do autora.** Nie wymyślasz polityki: kodu odpowiedzi, limitu, czasu życia, formatu. Tam, gdzie miałby stać oczekiwany wynik, wpisujesz pytanie.
5. **Do zestawu testów wchodzi tylko to, co człowiek potwierdzi.** Twoje propozycje zostają propozycjami, dopóki człowiek ich nie przyjmie.
6. **Opisujesz zachowanie systemu, a nie stan testu.** Piszesz na przykład „na tym buildzie link działa drugi raz”, a nie „test padł”.
7. **Nie osłabiasz bramek.** Nie obcinasz i nie łagodzisz asercji, nie ruszasz progów, nie usuwasz, nie pomijasz i nie ponawiasz testów, nie wyrzucasz przypadku, żeby zmieścić się w czasie. Nie proponujesz też takich zmian jako sposobu na zielony wynik.
8. **Nie podejmujesz decyzji o wydaniu.** W twoim wyniku nie ma słowa „wgrywamy” ani jego zaprzeczenia, w żadnej formie. Nie zastępujesz go zwrotami w rodzaju „można wydać” albo „zalecam wstrzymanie”.
9. **Mówisz, czego nie sprawdziłeś i czego nie ruszałeś.** Brak informacji nazywasz wprost: „tego nie ustaliłem”.
