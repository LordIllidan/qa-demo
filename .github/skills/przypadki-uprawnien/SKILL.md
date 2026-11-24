---
name: przypadki-uprawnien
description: Osobna grupa przypadków uprawnień do zwykłej historyjki. Przechodzi po trzech pytaniach kontrolnych (obcy identyfikator, wygasły token albo sesja, rola tylko do odczytu), a oczekiwany wynik bierze z wymagania; gdy wymaganie go nie podaje, stawia pytanie zamiast wymyślonej polityki. Użyj, gdy tester prosi o przypadki uprawnień, kontroli dostępu, autoryzacji albo ról dla historyjki, na przykład resetu hasła albo filtra listy.
---

# Przypadki uprawnień przy zwykłej historyjce

Autor historyjki opisuje zwykle drogę uprawnionego użytkownika. O tym, co ma się stać, gdy ktoś sięga po cudze dane, używa starego tokenu albo ma rolę tylko do odczytu, często nie pisze nic. Twoim zadaniem jest dopisać tę grupę przypadków. Politykę dostępu ustala autor wymagania albo właściciel bezpieczeństwa, a nie tester i nie ty, dlatego tam, gdzie wymaganie milczy, zostawiasz pytanie.

## Wejście

Tekst wymagania i opis ról, jeśli istnieje. W repozytorium qa-demo są dwie historyjki:

```powershell
python narzedzia/wymaganie.py reset-hasla
python narzedzia/wymaganie.py filtr-zamowien
```

## Jak pracować

1. Wypisz z wymagania role, zasoby i identyfikatory, które w nim występują: kto działa, na czym i czym się uwierzytelnia.
2. Przejdź po liście kontrolnej. Każdy punkt przełóż na konkretne przypadki dla tej historyjki:
   - **Obcy identyfikator.** Użytkownik podaje identyfikator zasobu, konta albo tokenu, który należy do kogoś innego.
   - **Wygasły token albo sesja.** Użytkownik działa z tokenem lub sesją, które były ważne, a już nie są: wygasły, zostały użyte albo unieważnione.
   - **Rola tylko do odczytu.** Użytkownik z rolą bez prawa zmiany próbuje operacji, która coś zmienia albo wynosi dane poza system.
3. Dla każdego przypadku poszukaj w wymaganiu zdania, które mówi, co ma się stać. Jeśli jest, podaj oczekiwany wynik z cytatem. Jeśli go nie ma, wpisz pytanie do autora. Gdy wymaganie odpowiada częściowo, wpisz to, co mówi, z cytatem, a resztę jako pytanie.
4. Jeśli punkt listy nie ma zastosowania w tej historyjce, napisz to i podaj powód. Nie dopisuj przypadku na siłę.
5. Możesz dodać przypadki spoza listy kontrolnej, jeśli wynikają z ról albo zasobów opisanych w wymaganiu. Dotyczy to także dostępu, na który wymaganie pozwala: test uprawnień sprawdza obie strony granicy. Takie przypadki mają grupę „inne” i źródło podane tak samo jak pozostałe.

W pytaniu możesz przywołać zalecenie OWASP jako uzasadnienie, dlaczego pytasz. Takie zalecenie pozostaje regułą własną modelu, dopóki autor wymagania go nie potwierdzi.

## Format wyniku

```markdown
# Przypadki uprawnień: <identyfikator albo nazwa wymagania>

## Zdanie modelu

### Role, zasoby i identyfikatory z wymagania

- <kto działa, na czym, czym się uwierzytelnia>

### Przypadki

| Nr | Grupa | Przypadek | Oczekiwany wynik albo pytanie | Źródło |
| --- | --- | --- | --- | --- |
| U1 | obcy identyfikator | <przypadek> | <wynik> | zdanie z wymagania <numer>: „<cytat>” |
| U2 | wygasły token albo sesja | <przypadek> | pytanie P1 | reguła własna modelu |
| U3 | rola tylko do odczytu | <przypadek> | pytanie P2 | reguła własna modelu |

### Punkty listy kontrolnej bez zastosowania

- <punkt i powód albo „wszystkie punkty mają zastosowanie”>

### Pytania do autora

| Nr | Pytanie | Dlaczego pytam |
| --- | --- | --- |
| P1 | <pytanie> | <czego wymaganie nie mówi; ewentualnie zalecenie, na które się powołuję> |

### Czego nie sprawdziłem

- <na przykład: przypadków nie wykonałem na żadnym buildzie; nie znam ról spoza wymagania>

## Decyzja człowieka

- [ ] Odpowiedzi na pytania o politykę dostępu (autor wymagania albo właściciel bezpieczeństwa):
- [ ] Które przypadki wchodzą do zestawu testów (tester):
```

## Czego nie robisz

- Nie wymyślasz polityki: kodu odpowiedzi dla obcego identyfikatora, czasu życia tokenu ani tego, co wolno roli tylko do odczytu.
- Nie podajesz zalecenia OWASP ani dobrej praktyki jako oczekiwanego wyniku.
- Nie prowadzisz ataków i nie wysyłasz żądań do systemu. Układasz przypadki.
- Nie ogłaszasz, że funkcja jest bezpieczna albo że kontrola dostępu działa.

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
10. **Nie czytasz katalogu `prowadzacy/`.** Leżą w nim odpowiedzi pokazu przeznaczone dla prowadzącego. Nie otwierasz, nie przeszukujesz i nie cytujesz żadnego pliku z tego katalogu, także wtedy, gdy trafisz na niego w wynikach wyszukiwania. Swoje zdanie opierasz na wejściu.
