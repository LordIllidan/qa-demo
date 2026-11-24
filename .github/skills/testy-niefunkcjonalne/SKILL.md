---
name: testy-niefunkcjonalne
description: Przegląd wymagania pod kątem jakości innej niż funkcja, czyli wydajności, zgodności, użyteczności i dostępności, niezawodności, bezpieczeństwa, utrzymywalności i przenośności. Dla każdej cechy mówi, co wymaganie zapisuje, o co trzeba zapytać autora i jaki rodzaj testu sprawdziłby odpowiedź. Użyj, gdy tester pyta, jakie rodzaje testów są potrzebne dla historyjki, o wymagania niefunkcjonalne, o testy wydajności, dostępności, użyteczności albo zgodności, albo o to, czego poza funkcją nie sprawdzono.
---

# Testy niefunkcjonalne: co mówi wymaganie

Historyjka zwykle opisuje, co system ma robić, a milczy o tym, jak dobrze ma to robić: jak szybko, dla kogo, na czym, co przy awarii. Tester, który planuje testy tylko z kryteriów akceptacji, sprawdzi funkcję i pominie resztę. Twoim zadaniem jest przejść po cechach jakości i przy każdej oddzielić to, co wymaganie zapisuje, od tego, o co trzeba zapytać. Największe ryzyko polega na tym, że podasz próg albo normę tak, jakby stały w wymaganiu.

## Wejście

Tekst wymagania. W repozytorium qa-demo są dwie historyjki:

```powershell
python narzedzia/wymaganie.py reset-hasla
python narzedzia/wymaganie.py filtr-zamowien
```

Jeśli tester wkleił wymaganie do rozmowy, pracujesz na wklejonym tekście.

## Jak pracować

1. Przejdź po liście cech jakości. Lista pochodzi z modelu jakości produktu ISO/IEC 25010:2023, bez przydatności funkcjonalnej.
   - **Wydajność**: czas odpowiedzi, zużycie zasobów, pojemność.
   - **Zgodność**: współdziałanie z innymi systemami i formatami, współistnienie.
   - **Użyteczność i dostępność**: zrozumiałość, obsługa, ochrona przed błędem użytkownika, korzystanie przez osoby z niepełnosprawnościami.
   - **Niezawodność**: dostępność usługi, zachowanie przy awarii, odtwarzanie.
   - **Bezpieczeństwo**: poufność, integralność, rozliczalność, uwierzytelnienie, odporność na atak.
   - **Utrzymywalność**: możliwość analizy, zmiany i testowania.
   - **Przenośność**: dostosowanie do środowisk, skalowanie, instalacja.
   - **Bezpieczeństwo użytkowania**: ochrona życia, zdrowia, mienia i środowiska.
2. Dla każdej cechy znajdź zdania wymagania, które jej dotyczą, i zacytuj je.
3. Gdy zdania nie ma, ustal, czy cecha ma zastosowanie w tej historyjce. Jeśli ma, zapisz pytanie do autora. Pytanie ma dać odpowiedź, którą da się sprawdzić. Jeśli nie ma, napisz dlaczego; to reguła własna modelu.
4. Dla każdej cechy, która ma zastosowanie, nazwij rodzaj testu, który sprawdziłby odpowiedź, i napisz, czy zwykle wykonuje się go ręcznie, automatycznie czy narzędziem. To reguła własna modelu, a nie wymaganie.
5. Napisz, czego z samego tekstu nie da się ocenić, na przykład wyglądu i obsługi interfejsu bez makiet.

Normę albo zalecenie, na przykład WCAG albo OWASP, możesz przywołać w pytaniu jako uzasadnienie. Pozostają one regułą własną modelu, dopóki autor wymagania ich nie potwierdzi.

## Format wyniku

```markdown
# Testy niefunkcjonalne: <identyfikator albo nazwa wymagania>

## Zdanie modelu

<jedno albo dwa zdania: o których cechach wymaganie mówi, o których milczy i ile pytań z tego wynika>

### Cechy jakości a wymaganie

| Cecha | Co mówi wymaganie | Pytanie do autora | Rodzaj testu (reguła własna modelu) | Zwykle ręcznie, automatycznie czy narzędziem (reguła własna modelu) |
| --- | --- | --- | --- | --- |
| <cecha> | zdanie z wymagania <numer>: „<cytat>” albo „nic” | <pytanie albo „–”> | <rodzaj testu> | <sposób wykonania> |

### Cechy bez zastosowania w tej historyjce

- <cecha i powód; reguła własna modelu>

### Czego nie da się ocenić z tekstu wymagania

- <na przykład: obsługi interfejsu bez makiet, zachowania pod obciążeniem bez pomiaru>

## Decyzja człowieka

- [ ] Które pytania idą do autora wymagania:
- [ ] Które rodzaje testów wchodzą do planu i kto je wykonuje:
```

## Czego nie robisz

- Nie wymyślasz progów: czasu odpowiedzi, liczby użytkowników, poziomu zgodności z normą, dopuszczalnego czasu niedostępności.
- Nie podajesz normy ani dobrej praktyki jako wymagania.
- Nie ogłaszasz, że cecha jest spełniona albo że system jest wydajny, dostępny czy bezpieczny.
- Nie wykonujesz testów: nie obciążasz systemu, nie prowadzisz ataków i nie uruchamiasz skanerów.
- Nie pomijasz cechy dlatego, że wymaganie o niej milczy. Milczenie zapisujesz jako pytanie albo jako brak zastosowania z powodem.

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
