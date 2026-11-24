# Agenty LangGraph

Proste agenty w LangGraph, każdy jako krótki graf kroków. Każde z 22 zagadnień zestawu da się uruchomić jednym poleceniem `python -m agenci_langgraph <polecenie>`: dziewięć obsługują trzy agenty z własnym grafem, pozostałe trzynaście jeden wspólny graf „Jedno zagadnienie”. W każdym widać osobno dwie rzeczy: zdanie modelu i decyzję człowieka. Graf zatrzymuje się przed decyzją i bez odpowiedzi człowieka nie idzie dalej.

Kod: katalog `agenci_langgraph`. Baza zestawu (aplikacja, testy, skrypty, skille) działa bez LangGraph; zależności agentów są w osobnym pliku `requirements-langgraph.txt`.

## Lista agentów

| Polecenie | Agent | Zagadnienia | Zatrzymania | Opis |
| --- | --- | --- | --- | --- |
| `zestaw` | Od wymagania do potwierdzonego zestawu | 1, 7, 8, P4 | jedno | [agent-langgraph-zestaw.md](agent-langgraph-zestaw.md) |
| `zgloszenie` | Od czerwonego przebiegu do zgłoszenia | P1, 2 | dwa | [agent-langgraph-zgloszenie.md](agent-langgraph-zgloszenie.md) |
| `karta` | Dwa buildy i karta | 4, 5, 6 | trzy | [agent-langgraph-karta.md](agent-langgraph-karta.md) |
| nazwa skilla zagadnienia, na przykład `ocena-asercji` | Jedno zagadnienie | 3, P2, P3, P5, P6, R1–R18 | jedno | [agent-langgraph-jedno-zagadnienie.md](agent-langgraph-jedno-zagadnienie.md) |

Listę poleceń z zagadnieniem, które każde obsługuje, wypisuje:

```powershell
python -m agenci_langgraph lista
```

## Podział ról w grafie

| Kto | Co robi | Gdzie w kodzie |
| --- | --- | --- |
| skrypt z `narzedzia` | przygotowuje wejście: wymaganie, wynik przebiegu albo liczby | krok wejścia, `krok_wejscia` |
| skill z `.github/skills` | jest instrukcją dla modelu; graf wczytuje plik `SKILL.md` przy każdym kroku i nie powiela jego treści | `wczytaj_skill` |
| model | formułuje zdanie na podstawie skilla i wejścia | krok modelu, `krok_modelu` |
| człowiek | podejmuje decyzję przy zatrzymaniu grafu | krok decyzji, `krok_decyzji` |
| graf | pilnuje kolejności, zatrzymuje się, zapisuje wynik po decyzji | `zbuduj` w pliku agenta |

Graf niczego nie ocenia. Nie czyta wyniku testów, nie porównuje liczb i nie poprawia zdania modelu. Z tekstu modelu bierze tylko dwie rzeczy, mechanicznie: listę decyzji z części „Decyzja człowieka” oraz wiersze tabel o numerach, które wpisał człowiek.

Model w grafie nie ma narzędzi: nie uruchamia poleceń i nie czyta plików. Dostaje skill i tekst oddany przez skrypty, a w agencie „Jedno zagadnienie” także prośbę i pliki, które człowiek sam wskazał w wierszu poleceń. Nic więcej. Decyzje człowieka nie trafiają do modelu. Katalogu `prowadzacy` agenty nie czytają; pliku z tego katalogu agent „Jedno zagadnienie” nie przyjmuje także od człowieka.

## Instalacja

Agenty wymagają Pythona 3.11 albo nowszego (tego wymaga pakiet `langchain`). Polecenia w składni PowerShell, z katalogu głównego repozytorium, w aktywnym środowisku `.venv`:

```powershell
python -m pip install -r requirements-langgraph.txt
```

Plik instaluje zależności bazy oraz `langgraph`, `langchain` i pakiety integracji dla dostawców `openai` i `anthropic`. Wersje są przypięte.

## Uruchomienie

1. Ustaw model: [agenci-langgraph-model.md](agenci-langgraph-model.md).
2. Dla agentów, które uruchamiają testy na buildach (`zgloszenie`, `karta` i zagadnienia 3, P2, P3, P6), uruchom aplikację w osobnym oknie PowerShell: `python app/serwer.py`. Lista poleceń mówi, które to są.
3. Uruchom agenta z katalogu głównego repozytorium:

```powershell
python -m agenci_langgraph zestaw
python -m agenci_langgraph zgloszenie
python -m agenci_langgraph karta
python -m agenci_langgraph ocena-asercji
```

Polecenia dla pozostałych zagadnień i ich opcje opisuje [agent-langgraph-jedno-zagadnienie.md](agent-langgraph-jedno-zagadnienie.md). Opcje każdego polecenia pokazuje `python -m agenci_langgraph <polecenie> --help`.

## Co widać w oknie

Agent wypisuje każdy wykonany krok, a przy zatrzymaniu pokazuje zdanie modelu i pyta o decyzje:

```text
[krok wejscie_zakres] wejście ze skryptów: python narzedzia/lista_sprawdzen.py; python narzedzia/wymaganie.py reset-hasla
[krok zakres] model powiedział swoje zdanie według skilla zakres-po-zmianie

========================================================================
ZATRZYMANIE GRAFU: decyzja_zakres
Graf czeka na decyzję człowieka i bez niej nie pójdzie dalej.
========================================================================

ZDANIE MODELU (krok zakres, skill zakres-po-zmianie)

<tekst modelu w formacie ze skilla>

DECYZJA CZŁOWIEKA (krok zakres); sam Enter zostawia pozycję bez odpowiedzi
  Co wykonać w oknie: _
```

Pytania pod nagłówkiem „DECYZJA CZŁOWIEKA” to pozycje, które model wypisał w części „Decyzja człowieka” swojego wyniku, zgodnie z formatem ze skilla. Jeśli model takiej listy nie wypisał, graf zadaje jedno ogólne pytanie o decyzję. Odpowiedź jest dowolnym tekstem. Sam Enter zostawia pozycję bez odpowiedzi i tak jest zapisywana.

## Zatrzymanie i wznowienie

Zatrzymanie to wywołanie `interrupt` z LangGraph w kroku decyzji. Graf zapisuje wtedy swój stan i oddaje sterowanie. Po odpowiedzi człowieka program wznawia graf poleceniem `Command(resume=...)` i graf idzie dalej od kroku decyzji. Kroki przed zatrzymaniem nie wykonują się drugi raz, więc model nie jest pytany ponownie, a skrypty nie są ponownie uruchamiane.

Stan grafu ma cztery pola:

| Pole | Zawartość |
| --- | --- |
| `wejscie` | polecenie i tekst, który oddał skrypt |
| `zdanie_modelu` | krok, nazwa skilla, polecenia wejścia i dosłowny tekst modelu |
| `decyzja_czlowieka` | krok, pytanie i odpowiedź człowieka |
| `zapisane` | pliki zapisane po decyzji |

Stan żyje w pamięci programu (`InMemorySaver`). Przerwanie programu przez Ctrl+C w trakcie zatrzymania kończy przebieg bez zapisu; następne uruchomienie zaczyna od początku.

## Co zapisuje

Pliki trafiają do katalogu `wyniki/agenci`, który nie trafia do repozytorium. Każdy agent zapisuje protokół dopiero po ostatniej decyzji. Protokół ma dla każdego kroku trzy części: polecenia, z których pochodzi wejście, zdanie modelu zapisane dosłownie jako cytat oraz decyzję człowieka. Kolejne uruchomienie agenta nadpisuje jego pliki.

## Gdy coś pójdzie nie tak

Agent kończy się kodem 2 i komunikatem „Agent zatrzymany: ...”, gdy nie ma ustawionego modelu, skrypt nie przygotował wejścia (na przykład aplikacja nie działa), model nie odpowiedział albo nie ma odpowiedzi człowieka. W takim przypadku niczego nie zapisuje.

## Pliki

| Plik | Zawartość |
| --- | --- |
| `agenci_langgraph/wspolne.py` | stan grafu, wejście ze skryptów, wczytanie skilla, rozmowa z modelem, krok decyzji, zapis protokołu |
| `agenci_langgraph/model.py` | model ze zmiennych środowiskowych |
| `agenci_langgraph/rozmowa.py` | przebieg grafu w konsoli: kroki, zatrzymanie, wznowienie |
| `agenci_langgraph/od_wymagania_do_zestawu.py` | graf agenta `zestaw` |
| `agenci_langgraph/od_przebiegu_do_zgloszenia.py` | graf agenta `zgloszenie` |
| `agenci_langgraph/dwa_buildy_i_karta.py` | graf agenta `karta` |
| `agenci_langgraph/jedno_zagadnienie.py` | wspólny graf dla zagadnień bez własnego agenta i lista tych zagadnień ze skryptami |
| `agenci_langgraph/__main__.py` | uruchamianie z konsoli i lista agentów |
| `agenci_langgraph/testy` | testy przepływu na modelu zastępczym: [agenci-langgraph-testy.md](agenci-langgraph-testy.md) |
| `requirements-langgraph.txt` | zależności agentów z wersjami |
