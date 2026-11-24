---
name: lokalizatory-po-zmianie
description: Lokalizatory testu interfejsu, które po zmianie strony przestały pasować. Zestawia selektor z dwiema wersjami HTML i proponuje nowy selektor jako regułę własną modelu, do decyzji człowieka. Użyj, gdy tester prosi o zepsute lokalizatory, self-healing, zmianę strony, która wywaliła test UI, albo o przegląd selektorów.
---

# Lokalizatory po zmianie strony

Test interfejsu pada, gdy znika identyfikator albo zmienia się tekst przycisku, choć funkcja została. Model łatwo „naprawi” selektor tak, żeby test przeszedł, i przy okazji wskaże inny element. Dostajesz tabelę: które selektory pasują do wersji sprzed zmiany i do wersji po zmianie. Proponujesz nowy selektor i zostawiasz decyzję człowiekowi. Sam plików nie zmieniasz.

## Wejście

- Tabela lokalizatorów wobec dwóch wersji strony.
- Wymaganie, jeśli tester chce wiedzieć, czy zmiana tekstu rusza zdanie wymagania.

W repozytorium qa-demo:

```powershell
python narzedzia/lokalizatory.py
python narzedzia/wymaganie.py reset-hasla
```

Skrypt sprawdza dopasowanie mechanicznie i aplikacji nie wymaga.

## Jak pracować

1. Wypisz lokalizatory, które pasowały przed zmianą i nie pasują po niej. To fakt z tabeli.
2. Dla każdego zaproponuj jeden selektor oparty na tym, co w wersji po zmianie zostało: etykieta, rola, tekst. Oznacz go jako regułę własną modelu. Selektor, który pasuje do kilku elementów, odrzuć i napisz dlaczego.
3. Osobno napisz, czy zmiana tekstu widocznego użytkownikowi dotyka zdania wymagania. Jeśli wymaganie tego tekstu nie podaje, zapisz pytanie, a nie werdykt, że to tylko zmiana techniczna.
4. Lokalizatory, które pasują w obu wersjach, wypisz jako bez zmiany.

## Format wyniku

```markdown
# Lokalizatory: <plik>

## Zdanie modelu

<jedno albo dwa zdania: ile selektorów przestało pasować i czy zmiana rusza tekst z wymagania>

### Selektory

| Id | Przed | Po | Propozycja | Źródło |
| --- | --- | --- | --- | --- |
| <id> | pasuje albo nie pasuje | pasuje albo nie pasuje | <selektor albo „bez zmiany”> | reguła własna modelu albo zdanie z wymagania <numer>: „<cytat>” |

### Czego nie sprawdziłem

- <na przykład: nie uruchamiałem testu w przeglądarce>

## Decyzja człowieka

- [ ] Które propozycje selektorów przyjąć:
- [ ] Czy zmiana tekstu idzie do autora wymagania:
```

## Czego nie robisz

- Nie podmieniasz selektora w teście. Propozycja zostaje propozycją.
- Nie wybierasz selektora tylko dlatego, że dzięki niemu test przejdzie.
- Nie uznajesz zmiany tekstu przycisku za kosmetykę, jeśli wymaganie tego tekstu nie rozstrzyga.
- Nie uruchamiasz przeglądarki.

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
