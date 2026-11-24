# Agenty LangGraph: testy na modelu zastępczym

Testy sprawdzają przepływ grafów bez klucza i bez sieci: kolejność kroków, zatrzymanie, wznowienie po decyzji człowieka i zapis. Wejście jest prawdziwe, bo pochodzi ze skryptów z katalogu `narzedzia`. Zastąpiony jest tylko model.

Kod: `agenci_langgraph/testy`.

## Uruchomienie

Z katalogu głównego repozytorium, po instalacji z `requirements-langgraph.txt`:

```powershell
python -m pytest agenci_langgraph/testy
```

Jeden plik albo jeden test:

```powershell
python -m pytest agenci_langgraph/testy/test_dwa_buildy_i_karta.py
python -m pytest agenci_langgraph/testy -k "zatrzymuje"
```

Zmienne `QA_DEMO_MODEL_DOSTAWCA` i `QA_DEMO_MODEL_NAZWA` nie są potrzebne.

Polecenie `python -m pytest` bez ścieżki uruchamia jak dotąd tylko katalog `testy`, czyli testy aplikacji. Testy agentów trzeba wskazać ścieżką.

## Aplikacja

Część testów uruchamia skrypt `przebieg.py`, więc potrzebuje buildów pod portami 8765 i 8766. Jeśli aplikacja działa w drugim oknie, testy z niej korzystają. Jeśli nie działa, testy uruchamiają brakujące buildy na czas przebiegu i zatrzymują je po zakończeniu.

## Model zastępczy

Plik `agenci_langgraph/testy/model_zastepczy.py`. Model zastępczy ma tę samą metodę `invoke` co model czatu z LangChain. Niczego nie ocenia i nie zawiera gotowych odpowiedzi: z instrukcji, którą dostał, wycina niewypełniony szablon wyniku ze skilla i oddaje go jako swoją odpowiedź. Odpowiedź ma więc te same części i tabele co odpowiedź prawdziwego modelu, ale w miejscu treści stoją pola szablonu, na przykład `<przypadek>`.

Model zastępczy zapisuje każde wywołanie. Dzięki temu testy sprawdzają, co dokładnie dostał model: instrukcję złożoną ze skilla i wejście złożone z tekstu skryptów.

Model zastępczy jest tylko w testach. Polecenie `python -m agenci_langgraph` zawsze używa modelu ze zmiennych środowiskowych.

## Co sprawdzają testy

| Plik | Co sprawdza |
| --- | --- |
| `test_wspolne.py` | wejście pochodzi ze skryptu w stałej ramce; model dostaje skill jako instrukcję i wynik skryptu jako wejście; błąd skryptu, brak skilla, błąd modelu i pusta odpowiedź zatrzymują agenta; lista decyzji pochodzi z części „Decyzja człowieka” |
| `test_od_wymagania_do_zestawu.py` | graf zatrzymuje się przed zapisem i do decyzji niczego nie zapisuje; każdy krok modelu dostaje swój skill i tylko wejście ze skryptów; po wznowieniu do zestawu i do pliku dla przebiegu wchodzą tylko wskazane numery; bez potwierdzenia nic nie wchodzi; po decyzji model nie jest pytany ponownie |
| `test_od_przebiegu_do_zgloszenia.py` | pierwsze zatrzymanie pokazuje klasyfikację i pytanie o dalszy krok; bez słowa „tak” graf nie uruchamia przebiegów i nie prosi o szkic; po słowie „tak” bierze dwa przebiegi i wymaganie, zatrzymuje się drugi raz i zapisuje protokół dopiero po decyzji o zgłoszeniu; porty buildów można wskazać |
| `test_dwa_buildy_i_karta.py` | graf zatrzymuje się trzy razy i po każdej decyzji idzie dalej; przy ostatnim zatrzymaniu pokazuje wcześniejsze decyzje ze stanu grafu; model karty dostaje tylko zbiór wyników, bez decyzji człowieka; protokół powstaje po ostatniej decyzji |
| `test_uruchomienie.py` | przebieg agenta w konsoli od początku do końca z odpowiedziami człowieka; brak odpowiedzi kończy agenta bez zapisu; brak zmiennych środowiskowych daje komunikat z nazwami zmiennych; dostawca i nazwa modelu pochodzą ze zmiennych |

Testy z plików `test_od_przebiegu_do_zgloszenia.py` i `test_dwa_buildy_i_karta.py` uruchamiają testy aplikacji na buildach przez skrypt `przebieg.py`, tak samo jak agent.

## Czego testy nie sprawdzają

- Treści zdania prawdziwego modelu: czy trzyma się formatu ze skilla, czy oznacza źródła i czy nie łamie zasad pokazu. To zależy od modelu i wymaga uruchomienia agenta z kluczem.
- Połączenia z dostawcą modelu.

## Pliki zapisywane przez testy

Zapis agentów trafia w testach do katalogu tymczasowego, a nie do `wyniki/agenci`. Skrypty z katalogu `narzedzia` zapisują swoje pliki w katalogu `wyniki`, tak jak przy zwykłym uruchomieniu.
