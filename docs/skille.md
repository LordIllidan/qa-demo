# Zbiór skilli dla testerów

Dwadzieścia dwa skille GitHub Copilot: czternaście dla zagadnień pokazu i osiem dla zagadnień rozszerzających (R1–R8), po jednym na zagadnienie. Skill to instrukcja wielokrotnego użytku: mówi modelowi, jakiego wejścia potrzebuje, jak ma pracować, w jakim formacie oddać wynik i czego mu nie wolno.

## Gdzie leżą i w jakim formacie

Skille leżą w katalogu `.github/skills`. To miejsce, z którego GitHub Copilot ładuje skille projektu (dokumentacja: [Adding agent skills for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills)). Każdy skill ma własny katalog z plikiem `SKILL.md`:

```text
.github/skills/
└── luki-w-wymaganiu/
    └── SKILL.md
```

Plik `SKILL.md` to Markdown z nagłówkiem YAML. Nagłówek ma dwa wymagane pola:

| Pole | Reguły |
| --- | --- |
| `name` | małe litery, cyfry i łączniki; do 64 znaków; takie samo jak nazwa katalogu |
| `description` | co skill robi i kiedy go użyć; do 1024 znaków; na tej podstawie Copilot decyduje, czy załadować skill |

Skille nie mają pola `allowed-tools`, więc żadnego narzędzia nie zatwierdzają z góry: o zgodę na polecenia w terminalu Copilot pyta według własnych ustawień. Format jest zgodny ze specyfikacją [Agent Skills](https://agentskills.io/specification).

## Lista skilli

| Skill | Zagadnienie | Co oddaje model |
| --- | --- | --- |
| `luki-w-wymaganiu` | 1. Luki w wymaganiu | pytania do autora i dopisane przypadki, każda pozycja ze źródłem |
| `zgloszenie-defektu` | 2. Defekt z czerwonego przebiegu | szkic zgłoszenia, które opisuje zachowanie systemu |
| `ocena-asercji` | 3. Ocena asercji | zdanie o tym, który test nadaje się na bramkę i dlaczego drugi defektu nie wykrywa |
| `zakres-po-zmianie` | 4. Zakres po zmianie | kolejność sprawdzeń od najwyższego ryzyka, dopisany przypadek i to, co nie mieści się w oknie |
| `dwa-buildy-w-liczbach` | 5. Zdanie o dwóch buildach | jedno zdanie o zmianie w liczbach, z kontrolą profilu i progami bez zmian |
| `karta-przed-wgraniem` | 6. Karta przed wgraniem | jedno zdanie i karta: co sprawdzone, co czerwone, czego nie ruszano |
| `dane-pod-regule` | 7. Dane pod regułę | tabela wejść z oczekiwanym wynikiem i jego źródłem oraz plik dla przebiegu |
| `przypadki-uprawnien` | 8. Uprawnienia przy zwykłej historyjce | przypadki uprawnień z wynikiem z wymagania albo z pytaniem |
| `klasyfikacja-awarii` | P1. Czerwony przebieg: produkt, test czy środowisko | grupy awarii z proponowaną klasyfikacją, dowodem i tym, czego nie ustalono |
| `test-potwierdzajacy` | P2. Ponowny test po poprawce | zdanie o tym, czy kroki ze zgłoszenia dają wynik oczekiwany, i co zostało niesprawdzone |
| `test-niestabilny` | P3. Test niestabilny | zdanie z liczbami o teście o zmiennym wyniku i przypuszczalny wzorzec |
| `pokrycie-wymagania` | P4. Pokrycie wymagania testami | zdania bez testu i testy bez zdania |
| `sesja-eksploracyjna` | P5. Karta sesji eksploracyjnej | karta przed sesją albo raport z notatek po sesji |
| `przeglad-zmiany-w-testach` | P6. Przegląd zmiany w testach | lista miejsc, w których bramka stała się słabsza, ze skutkiem w wynikach |
| `projektowanie-przypadkow` | R1. Przypadki testowe techniką | technika dobrana do zdania wymagania, jej model i przypadki z krokami, danymi i wynikiem ze źródłem |
| `zgloszenie-z-obserwacji` | R2. Zgłoszenie z obserwacji ręcznej | szkic zgłoszenia z notatek testera, braki do odtworzenia i możliwe powtórzenia wśród otwartych zgłoszeń |
| `kandydaci-do-automatyzacji` | R3. Kandydaci do automatyzacji | zestawienie sprawdzeń ręcznych z testami automatycznymi: w całości, częściowo, brak, z czasem ręcznej pracy |
| `szkic-testu-automatycznego` | R4. Szkic testu automatycznego | kod testu dla potwierdzonego przypadku, asercje ze zdaniem wymagania i to, czego test nie sprawdza |
| `testy-niefunkcjonalne` | R5. Testy niefunkcjonalne | tabela cech jakości: co mówi wymaganie, pytanie do autora, rodzaj testu |
| `testy-po-zmianie-wymagania` | R6. Testy po zmianie wymagania | stan każdego testu po zmianie wymagania, zdania bez testu i pytania do autora |
| `testy-z-opisu-interfejsu` | R7. Testy z opisu interfejsu | sprawdzenia kontraktu ze źródłem i niezgodności opisu interfejsu z wymaganiem |
| `plan-testow-iteracji` | R8. Plan testów iteracji | szkic planu: rodzaje testów dla historii, ryzyka, role, terminy i pytania |

Które skille służą testerowi manualnemu, a które automatyzującemu, opisuje [role-testerow.md](role-testerow.md).

## Budowa skilla

Każdy plik `SKILL.md` ma te same części:

1. Wstęp: po co tester to robi i gdzie leży ryzyko użycia modelu.
2. **Wejście**: czego model potrzebuje i którym poleceniem z katalogu `narzedzia` je dostaje.
3. **Jak pracować**: kroki.
4. **Format wyniku**: stały szablon z częścią „Zdanie modelu” i częścią „Decyzja człowieka”.
5. **Czego nie robisz**: zakazy właściwe dla tego zagadnienia.
6. **Zasady wspólne**: dziesięć zasad, takich samych w każdym skillu.

## Zasady wspólne

Każdy skill zawiera ten sam blok zasad. Blok jest powtórzony w każdym pliku, bo Copilot ładuje skille pojedynczo i nie ma gwarancji, że razem z jednym skillem przeczyta inny plik.

| Nr | Zasada |
| --- | --- |
| 1 | Wejście dostajesz, nie tworzysz |
| 2 | Zdanie modelu i decyzja człowieka stoją osobno |
| 3 | Każda pozycja ma źródło: zdanie z wymagania albo reguła własna modelu |
| 4 | Gdy wymaganie milczy, pytanie do autora zamiast wymyślonej polityki |
| 5 | Do zestawu testów wchodzi tylko to, co człowiek potwierdzi |
| 6 | Opis zachowania systemu, a nie stanu testu |
| 7 | Bez osłabiania bramek: asercje, progi, pominięcia, ponowienia, usuwanie przypadków |
| 8 | Bez decyzji o wydaniu: w wyniku nie ma słowa „wgrywamy” |
| 9 | Jawnie, czego model nie sprawdził i czego nie ruszał |
| 10 | Bez czytania katalogu `prowadzacy`, w którym leżą odpowiedzi pokazu dla prowadzącego |

## Jak użyć skilla

Copilot sam dobiera skill na podstawie prośby i pola `description`. Skill można też wskazać wprost.

W czacie Visual Studio Code, w trybie agenta, skill jest dostępny jako polecenie z ukośnikiem:

```text
/luki-w-wymaganiu dla wymagania reset-hasla
```

W GitHub Copilot CLI nazwę skilla podaje się w prośbie, a listę skilli pokazuje polecenie `/skills list`:

```text
Użyj skilla /zgloszenie-defektu dla przebiegu na porcie 8766.
```

Przed pracą ze skillami, które korzystają z przebiegów, uruchom aplikację w osobnym oknie PowerShell:

```powershell
python app/serwer.py
```

## Zmiana skilla

Przy zmianie zasad wspólnych trzeba poprawić blok „Zasady wspólne” we wszystkich dwudziestu dwóch plikach, żeby pozostał jednakowy. Nazwa w polu `name` musi być taka sama jak nazwa katalogu; wymaga tego specyfikacja.
