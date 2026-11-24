---
name: przeglad-przypadkow-recznych
description: Przegląd istniejących przypadków testowych ręcznych względem wymagania. Dla każdego przypadku wskazuje oczekiwany wynik bez źródła albo sprzeczny z wymaganiem, krok bez oczekiwanego wyniku, wynik, którego nie da się sprawdzić, brak warunków początkowych lub danych, kilka sprawdzeń w jednym przypadku i przypadki, które sprawdzają to samo. Użyj, gdy tester prosi o przegląd, ocenę albo uporządkowanie przypadków testowych, scenariuszy ręcznych, regresji ręcznej albo pyta, czy przypadki są dobrze napisane.
---

# Przegląd przypadków testowych ręcznych

Przypadek ręczny jest wart tyle, ile jego oczekiwany wynik. Wynik „wszystko działa poprawnie” każdy wykonawca oceni inaczej, wynik bez źródła w wymaganiu utrwala czyjeś założenie, a krok bez wyniku nie sprawdza niczego. Model może przy przeglądzie łatwo przepisać przypadki „na lepsze” i przy okazji wpisać oczekiwania, których wymaganie nie podaje. Twoim zadaniem jest wskazać problemy w przypadkach ze źródłem i zaproponować poprawki tylko tam, gdzie wymaganie daje oczekiwany wynik. Które poprawki przyjąć, decyduje człowiek.

## Wejście

- Przypadki ręczne: warunki początkowe, kroki i oczekiwane wyniki.
- Wymaganie, którego dotyczą.

W repozytorium qa-demo:

```powershell
python narzedzia/przypadki_reczne.py
python narzedzia/wymaganie.py reset-hasla
```

Jeśli tester wkleił przypadki z własnego narzędzia do zarządzania testami, pracujesz na wklejonym tekście.

## Jak pracować

1. Dla każdego oczekiwanego wyniku znajdź zdanie wymagania, z którego wynika, i zacytuj je. Wynik, którego wymaganie nie podaje, oznacz jako „bez źródła” i zapisz pytanie do autora. Wynik sprzeczny ze zdaniem wymagania oznacz jako „sprzeczny” z cytatem.
2. Wskaż w każdym przypadku problemy:
   - krok bez oczekiwanego wyniku,
   - wynik, którego nie da się jednoznacznie sprawdzić, na przykład „działa poprawnie”,
   - kilka sprawdzeń w jednym kroku albo w jednym przypadku,
   - brak warunków początkowych albo danych, od których zależy wynik,
   - krok, którego wykonawca nie odtworzy bez dodatkowej wiedzy.
3. Wskaż przypadki, które sprawdzają to samo, i podaj, czym się różnią, jeśli w ogóle.
4. Zaproponuj poprawione brzmienie tylko tam, gdzie oczekiwany wynik daje wymaganie. Tam, gdzie wymaganie milczy, zamiast poprawki stoi pytanie.
5. Wypisz zdania wymagania, których nie sprawdza żaden przypadek z wejścia.

## Format wyniku

```markdown
# Przegląd przypadków ręcznych: <wymaganie>

## Zdanie modelu

<jedno albo dwa zdania: ile przypadków ma problemy i który problem jest najważniejszy>

### Problemy w przypadkach

| Nr | Przypadek i krok | Problem | Źródło | Proponowana poprawka albo pytanie |
| --- | --- | --- | --- | --- |
| U1 | <id, krok> | <bez źródła, sprzeczny, bez wyniku, nieweryfikowalny, kilka sprawdzeń, brak warunków> | zdanie z wymagania <numer>: „<cytat>” albo „wymaganie nie podaje” | <brzmienie z wymagania albo pytanie do autora> |

### Przypadki, które sprawdzają to samo

- <id i id>: <co wspólne, czym się różnią>

### Zdania wymagania bez przypadku

- <numer>: „<cytat>”

### Czego nie sprawdziłem

- <na przykład: nie wykonywałem przypadków; nie sprawdzałem testów automatycznych>

## Decyzja człowieka

- [ ] Które poprawki przyjąć i kto poprawia przypadki:
- [ ] Które pytania idą do autora wymagania:
- [ ] Co zrobić z przypadkami, które sprawdzają to samo:
```

## Czego nie robisz

- Nie wpisujesz oczekiwanego wyniku, którego nie ma w wymaganiu, także jako poprawki. W tym miejscu stoi pytanie.
- Nie usuwasz przypadków i nie łączysz ich. Wskazujesz, co sprawdzają to samo.
- Nie zmieniasz pliku z przypadkami.
- Nie wykonujesz przypadków na buildzie i nie bierzesz oczekiwanego wyniku z odpowiedzi aplikacji.
- Nie oceniasz autora przypadków.

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
