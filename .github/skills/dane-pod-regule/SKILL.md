---
name: dane-pod-regule
description: Zamiana reguły z wymagania na konkretne dane testowe. Oddaje tabelę wejść z oczekiwanym wynikiem i źródłem tego wyniku oraz te same dane w formacie pliku, który można wstawić w przebieg. Użyj, gdy tester prosi o dane testowe, wartości wejściowe, przypadki brzegowe albo zestaw danych do reguły z wymagania.
---

# Dane pod regułę

Reguła w wymaganiu mówi ogólnie, a test potrzebuje konkretnej wartości i konkretnego oczekiwanego wyniku. Twoim zadaniem jest ułożyć takie wartości i przy każdej pokazać, z którego zdania wymagania wynika oczekiwany wynik. Jeśli wymaganie nie mówi, co ma się stać dla danego wejścia, nie zgadujesz: w miejscu wyniku stoi pytanie. Dane muszą dać się wstawić w przebieg bez przepisywania.

## Wejście

Tekst wymagania. W repozytorium qa-demo:

```powershell
python narzedzia/wymaganie.py reset-hasla
```

## Jak pracować

1. Wskaż regułę, pod którą układasz dane, i zacytuj ją.
2. Ułóż wejścia, które tę regułę pokazują z każdej strony: przypadek zgodny, przypadek naruszający regułę, przypadki brzegowe i puste wartości.
3. Dla każdego wejścia podaj oczekiwany wynik i zdanie wymagania, z którego on pochodzi. Gdy takiego zdania nie ma, wpisz pytanie do autora zamiast wyniku.
4. Używaj wyłącznie danych syntetycznych. Adresy w domenie example.com, hasła wymyślone na potrzeby testu.
5. Podaj dane w tabeli, a pod nią w formacie pliku dla przebiegu.

## Format wyniku

```markdown
# Dane pod regułę: <numer zdania i krótka nazwa reguły>

## Zdanie modelu

Reguła: zdanie z wymagania <numer>: „<cytat>”.

| Id | Wejście | Oczekiwany wynik | Źródło oczekiwanego wyniku |
| --- | --- | --- | --- |
| D1 | <konkretne wartości> | <wynik> | zdanie z wymagania <numer>: „<cytat>” |
| D2 | <konkretne wartości> | pytanie: <pytanie do autora> | reguła własna modelu |

### Plik dla przebiegu

<dane w formacie pliku, patrz niżej>

### Czego nie sprawdziłem

- <na przykład: danych nie wysłałem do żadnego builda>

## Decyzja człowieka

- [ ] Które wejścia trafiają do przebiegu:
```

### Format pliku w repozytorium qa-demo

Narzędzie `narzedzia/przebieg_danych.py` wysyła wejścia po kolei do operacji `POST /reset/potwierdz` i zapisuje odpowiedzi obok oczekiwań z pliku. Plik ma postać:

```json
{
  "format": "qa-demo/dane/1",
  "wymaganie": "reset-hasla",
  "operacja": "POST /reset/potwierdz",
  "wejscia": [
    {
      "id": "D1",
      "opis": "<krótki opis wejścia>",
      "token": "{nowy-link}",
      "haslo": "<hasło>",
      "oczekiwany_status": 200,
      "zrodlo": "zdanie z wymagania <numer>: „<cytat>”"
    },
    {
      "id": "D2",
      "opis": "<krótki opis wejścia>",
      "token": "<dosłowna wartość>",
      "haslo": "<hasło>",
      "oczekiwany_status": null,
      "pytanie": "<pytanie do autora>",
      "zrodlo": "reguła własna modelu"
    }
  ]
}
```

Pole `token` przyjmuje `{nowy-link}` (narzędzie prosi o reset i wstawia token z nowej wiadomości), `{ten-sam-link}` (token z poprzedniego `{nowy-link}`) albo dosłowną wartość, także pustą. Gdy oczekiwanego wyniku nie ma w wymaganiu, `oczekiwany_status` ma wartość `null`, a pytanie trafia do pola `pytanie`.

Plik zapisujesz dopiero wtedy, gdy człowiek wskaże wejścia, i tylko z tymi wejściami. Przebieg uruchamia człowiek albo ty na jego wyraźne polecenie:

```powershell
python narzedzia/przebieg_danych.py --port 8766 --dane <ścieżka do pliku>
```

## Czego nie robisz

- Nie wpisujesz oczekiwanego wyniku, którego nie ma w wymaganiu.
- Nie odczytujesz oczekiwanego wyniku z odpowiedzi aplikacji. To, co build zwraca dziś, może być defektem.
- Nie sięgasz po dane produkcyjne ani prawdziwe dane osobowe.
- Nie uruchamiasz przebiegu z własnej inicjatywy i nie dopisujesz do pliku wejść, których człowiek nie wybrał.

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
