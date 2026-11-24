# Zagadnienia rozszerzające R1–R5

Pięć zagadnień dodanych do czternastu zagadnień pokazu. Powstały po przeglądzie tego, jak zestaw pokrywa pracę testera manualnego i testera automatyzującego. Każde ma skill w `.github/skills` i jest przypisane do jednego z trzech agentów GitHub Copilot.

## Po co

Czternaście zagadnień pokazu dotyczy miejsc, w których model formułuje zdanie przy gotowym wejściu: wymaganiu, wyniku przebiegu albo liczbach. Przegląd pokazał pięć prac, których żadne z nich nie obejmowało:

| Brak | Kogo dotyczy | Zagadnienie |
| --- | --- | --- |
| projektowanie przypadków testowych z krokami, techniką projektowania testów | obie role | R1 |
| zgłoszenie defektu bez automatycznego przebiegu, z notatek testera | tester manualny | R2 |
| wybór tego, co automatyzować | tester automatyzujący | R3 |
| napisanie testu automatycznego | tester automatyzujący | R4 |
| testy inne niż funkcjonalne | obie role | R5 |

## Lista

| Nr | Zagadnienie | Skill | Agent | Wejście |
| --- | --- | --- | --- | --- |
| R1 | Przypadki testowe techniką | `projektowanie-przypadkow` | Analiza wymagania | `wymaganie.py` |
| R2 | Zgłoszenie z obserwacji ręcznej | `zgloszenie-z-obserwacji` | Analiza przebiegu | notatki testera, `wymaganie.py`, `material/zgloszenia/otwarte.json` |
| R3 | Kandydaci do automatyzacji | `kandydaci-do-automatyzacji` | Zakres i wydanie | `lista_sprawdzen.py`, `lista_testow.py` |
| R4 | Szkic testu automatycznego | `szkic-testu-automatycznego` | Analiza wymagania | przypadek potwierdzony przez człowieka, `wymaganie.py`, `lista_testow.py`, kod w `testy` |
| R5 | Testy niefunkcjonalne | `testy-niefunkcjonalne` | Analiza wymagania | `wymaganie.py` |

Opis każdego zagadnienia w układzie „sytuacja, model dostaje, model oddaje, czego nie robi, decyzja człowieka” jest w `README.md`, w sekcji „Zagadnienia rozszerzające”.

## Czym różnią się od zagadnień pokazu

- Nie należą do scenariusza pokazu ani do wariantu 20-minutowego.
- Nie mają agenta LangGraph.
- Nie dodają skryptów, materiału, testów ani zmian w aplikacji. Korzystają z tego, co już jest w repozytorium.
- Skilli i agentów dla tych zagadnień nie uruchomiono w GitHub Copilot. Sprawdzono, że wejście, które skille wskazują, istnieje i że polecenia działają.

Zasady są te same: blok „Zasady wspólne” w każdym z pięciu skilli jest taki sam jak w pozostałych czternastu.

## Zasada, którą każde zagadnienie trzyma

| Nr | Największe ryzyko użycia modelu | Jak skill je ogranicza |
| --- | --- | --- |
| R1 | długa lista przypadków bez powodu, z wymyślonym oczekiwanym wynikiem | każdy przypadek ma element modelu techniki i źródło; gdzie wymaganie milczy, stoi pytanie |
| R2 | zgłoszenie pewniejsze niż obserwacja | kroki tylko z notatek; braki do odtworzenia wypisane osobno; o powtórzeniu rozstrzyga człowiek |
| R3 | „mamy to zautomatyzowane”, bo nazwa testu pasuje | porównanie tego, co test sprawdza, ze sprawdzeniem ręcznym; bez wyliczeń, na które nie ma danych |
| R4 | test, który utrwala zachowanie builda, w tym defekt | test tylko dla potwierdzonego przypadku; asercja ma zdanie wymagania; kod przed zapisem przechodzi przegląd |
| R5 | próg albo norma podane jak wymaganie | progi tylko od autora wymagania; norma jako uzasadnienie pytania |

## Jak użyć

W GitHub Copilot CLI, z katalogu repozytorium:

```powershell
copilot --agent analiza-wymagania --prompt "Zaprojektuj przypadki testowe techniką dla wymagania reset-hasla."
copilot --agent analiza-przebiegu --prompt "Przygotuj zgłoszenie z obserwacji z godziny 10:13 w material/sesja/notatki-z-sesji.md."
copilot --agent zakres-i-wydanie --prompt "Które sprawdzenia ręczne mają już test automatyczny?"
copilot --agent analiza-wymagania --prompt "Jakie testy niefunkcjonalne wynikają z wymagania filtr-zamowien?"
```

Zagadnienie R4 zaczyna się od przypadku, który tester potwierdza w prośbie:

```powershell
copilot --agent analiza-wymagania --prompt "Napisz test automatyczny dla przypadku, który potwierdzam: <kroki, dane, oczekiwany wynik>."
```

Po przyjęciu kodu test uruchamia się na wskazanym buildzie, z aplikacją działającą w drugim oknie PowerShell:

```powershell
python app/serwer.py
```

```powershell
python narzedzia/przebieg.py --port 8765 --zestaw <plik z testem> --test <nazwa testu>
```

W czacie Visual Studio Code wybiera się agenta z listy albo wskazuje skill poleceniem z ukośnikiem, na przykład `/projektowanie-przypadkow dla wymagania filtr-zamowien`.

## Odpowiedzi dla prowadzącego

To, czego można się spodziewać po modelu w każdym z pięciu zagadnień, jest w pliku `prowadzacy/odpowiedzi-pokazu.md`, w części „Zagadnienia rozszerzające (R1–R5)”. Ten plik i `README.md` tego nie podają.

## Podział na role

Które z zagadnień służy testerowi manualnemu, a które automatyzującemu, opisuje [role-testerow.md](role-testerow.md).
