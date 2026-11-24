---
name: zgloszenie-z-obserwacji
description: Szkic zgłoszenia defektu z obserwacji testera pracującego ręcznie, czyli z notatek, kroków albo opisu tego, co zobaczył. Zestawia obserwację ze zdaniem wymagania, wypisuje, czego brakuje do odtworzenia, i wskazuje otwarte zgłoszenia, które mogą dotyczyć tego samego zachowania. Użyj, gdy tester opisuje własnymi słowami, co zrobił i co zobaczył, i prosi o zgłoszenie błędu, opis defektu z testów ręcznych albo o sprawdzenie, czy to już zgłoszono.
---

# Zgłoszenie z obserwacji ręcznej

Tester pracujący ręcznie nie ma zapisu przebiegu. Ma notatki: co zrobił, co zobaczył i czego nie jest pewien. Z takich notatek łatwo zrobić zgłoszenie, które brzmi pewniej niż obserwacja: z dopisanym krokiem, którego nie było, albo z oczekiwanym wynikiem, którego wymaganie nie podaje. Twoim zadaniem jest przepisać obserwację wiernie, zestawić ją z wymaganiem i powiedzieć, czego w niej brakuje. Drugie ryzyko to powtórzenie: to samo zachowanie mogło zostać już zgłoszone.

## Wejście

- Obserwacja testera: notatki z sesji albo opis w rozmowie. Tester wskazuje, której obserwacji dotyczy zgłoszenie.
- Wymaganie, z którego wynika oczekiwany wynik.
- Lista otwartych zgłoszeń, jeśli zespół ją ma.

W repozytorium qa-demo przykładowe notatki leżą w pliku `material/sesja/notatki-z-sesji.md`, a lista otwartych zgłoszeń w pliku `material/zgloszenia/otwarte.json`. Wymaganie podaje polecenie:

```powershell
python narzedzia/wymaganie.py reset-hasla
```

Jeśli tester nie wskazał obserwacji, zapytaj, której dotyczy zgłoszenie. Wyboru nie robisz za niego: to, która obserwacja jest defektem, jest decyzją człowieka. Jeśli lista otwartych zgłoszeń podaje plik z treścią zgłoszenia, przeczytaj ten plik.

## Jak pracować

1. Wypisz z notatek to, co dotyczy wskazanej obserwacji: czynności, dane, dosłowne odpowiedzi systemu, build, godzinę. Weź także wcześniejsze czynności, od których zależy stan systemu w chwili obserwacji.
2. Znajdź w wymaganiu zdanie, które mówi, jak system ma się zachować. Zacytuj je dosłownie. Jeśli takiego zdania nie ma, napisz to w pierwszym zdaniu wyniku: bez zdania z wymagania nie wiadomo, czy to defekt, a w miejscu wyniku oczekiwanego stoi pytanie do autora.
3. Ułóż kroki do odtworzenia wyłącznie z tego, co jest w notatkach. Kroku, którego w notatkach nie ma, nie dopisujesz. Wpisujesz go do części „Czego brakuje do odtworzenia”.
4. Wypisz, czego brakuje: danych, kolejności, informacji o buildzie, powtórzenia obserwacji, porównania z innym buildem.
5. Porównaj obserwację z otwartymi zgłoszeniami. Dla każdego, które może dotyczyć tego samego zachowania, podaj identyfikator, to, co jest wspólne, i to, czego nie wiesz. Jeśli znasz tylko tytuł zgłoszenia, opierasz się na tytule i tak to zapisujesz.
6. Ułóż tytuł i zdanie o wyniku faktycznym tak, żeby mówiły o zachowaniu systemu.

## Format wyniku

```markdown
# Szkic zgłoszenia z obserwacji: <tytuł: zachowanie systemu>

## Zdanie modelu

<jedno zdanie: co system zrobił i co miał zrobić według wymagania albo że wymaganie tego nie określa>

- Build i środowisko: <z notatek>
- Źródło obserwacji: <plik albo rozmowa, tester, godzina>

### Kroki do odtworzenia

1. <krok z notatek>
2. <...>

### Wynik faktyczny

<dosłowna odpowiedź systemu z notatek>

### Wynik oczekiwany

<zdanie z wymagania <numer>: „<cytat>” albo pytanie do autora, gdy wymaganie tego nie określa>

### Czego brakuje do odtworzenia

- <czego nie ma w notatkach>

### Możliwe powtórzenia wśród otwartych zgłoszeń

| Zgłoszenie | Co jest wspólne | Czego nie wiem |
| --- | --- | --- |
| <identyfikator i tytuł> | <kroki, zachowanie, build> | <na przykład: znam tylko tytuł> |

### Fakty pomocne przy ustaleniu dotkliwości

- <kogo dotyczy zachowanie, jak łatwo do niego doprowadzić>

## Decyzja człowieka

- [ ] Czy to defekt:
- [ ] Czy to powtórzenie otwartego zgłoszenia, czy nowe zgłoszenie:
- [ ] Dotkliwość i priorytet:
- [ ] Czy zgłoszenie wychodzi i do kogo:
```

Gdy żadne otwarte zgłoszenie nie pasuje, tabela zostaje z wpisem „nie znalazłem podobnego zgłoszenia na liście”. Gdy listy nie dostałeś, piszesz, że powtórzeń nie sprawdziłeś.

## Czego nie robisz

- Nie dopisujesz kroków, danych ani odpowiedzi systemu, których nie ma w notatkach. Nie wygładzasz wątpliwości testera.
- Nie odtwarzasz obserwacji sam: nie wysyłasz żądań do systemu i nie uruchamiasz testów.
- Nie rozstrzygasz, czy to powtórzenie. Nie dopisujesz niczego do istniejącego zgłoszenia.
- Nie wysyłasz zgłoszenia i nie zakładasz go w żadnym systemie.
- Nie nadajesz dotkliwości ani priorytetu. Dotkliwości zgłoszeń z listy nie zmieniasz.
- Nie podajesz domysłu o przyczynie w kodzie jako faktu.

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
