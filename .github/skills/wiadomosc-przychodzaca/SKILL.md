---
name: wiadomosc-przychodzaca
description: Sprawdzenie przychodzącej wiadomości e-mail, na przykład maila z linkiem resetu. Zestawia nadawcę, odbiorcę, temat, treść, link i token z wymaganiem i mówi, czego w wiadomości nie ma. Użyj, gdy tester prosi o walidację maila, sprawdzenie wiadomości z linkiem, nadawcy, treści albo tokenu.
---

# Wiadomość przychodząca

Wiadomość z linkiem jest częścią funkcji, nie dodatkiem. Model łatwo uzna mail za poprawny, bo „wygląda jak mail z resetem”. Dlatego zestawiasz nadawcę, odbiorcę, temat, treść, link i token z wymaganiem, a tam, gdzie wymaganie milczy, piszesz pytanie.

## Wejście

- Wiadomość: nadawca, odbiorca, temat, treść, link i token.
- Wymaganie.

W repozytorium qa-demo skrypt prosi o reset i czyta skrzynkę builda:

```powershell
python narzedzia/wiadomosc.py --port <port builda> --email <adres>
python narzedzia/wymaganie.py reset-hasla
```

Skrypt wymaga działającej aplikacji. Adres skrzynki podaje tester. Domyślnie jest to konto startowe.

## Jak pracować

1. Wypisz nadawcę, odbiorcę, temat, zdania treści, link i token tak, jak podaje wejście.
2. Przy każdej pozycji wskaż zdanie wymagania, które o niej mówi, z cytatem. Pozycja, o której wymaganie milczy (nadawca, kształt tematu, czas ważności linku), dostaje pytanie do autora, a nie ocenę „zgodne”.
3. Sprawdź, czy link z treści jest tym samym linkiem, który skrypt podaje osobno, i czy token z linku jest tym samym tokenem. Rozbieżność zapisz jako fakt.
4. Wypisz, czego nie sprawdziłeś: dostarczenia na prawdziwą skrzynkę, nagłówków technicznych, których skrypt nie podaje, drugiego builda.

## Format wyniku

```markdown
# Wiadomość: <temat>, build <numer>

## Zdanie modelu

<jedno albo dwa zdania: co w wiadomości jest ze zdania wymagania, a o czym wymaganie milczy>

### Pozycje wiadomości

| Pozycja | Wartość z wiadomości | Źródło |
| --- | --- | --- |
| nadawca | <...> | zdanie z wymagania <numer>: „<cytat>” albo „wymaganie milczy” |
| odbiorca | <...> | <...> |
| temat | <...> | <...> |
| treść | <zdanie> | <...> |
| link | <...> | <...> |
| token | <...> | <...> |

### Czego nie sprawdziłem

- <...>

## Decyzja człowieka

- [ ] Które pytania o milczące pola idą do autora:
- [ ] Czy wiadomość nadaje się do pokazania odbiorcy:
```

## Czego nie robisz

- Nie wymyślasz wymaganego nadawcy, tematu ani czasu ważności linku.
- Nie otwierasz linku i nie ustawiasz hasła. Mówisz tylko o tym, co jest w wiadomości.
- Nie uznajesz wiadomości za dostarczoną poza skrzynką testową builda.
- Nie zmieniasz treści wiadomości w aplikacji.

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
