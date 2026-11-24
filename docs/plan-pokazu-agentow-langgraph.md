# Plan pokazu agentów LangGraph z modelem z MLflow

Plan pokazu przypadków użycia agentów LangGraph z modelem udostępnianym przez lokalny MLflow w Dockerze. Agenty łączą się z MLflow jak z usługą zgodną z interfejsem OpenAI ([agenci-langgraph-model.md](agenci-langgraph-model.md)), więc kod nie wymaga zmian. Warunek: MLflow musi wystawiać adres `/v1/chat/completions`, tak jak MLflow AI Gateway (serwer deployments).

## Przed pokazem

### 0. Środowisko

Okno 1 PowerShell, z katalogu głównego repozytorium:

```powershell
git pull
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-langgraph.txt
python app/serwer.py
```

Agenty wymagają Pythona 3.11 albo nowszego.

### 1. Czy MLflow odpowiada

Okno 2 PowerShell. Port i nazwę endpointu weź ze swojego kontenera i jego `config.yaml`. Dla serwera gateway domyślny port to 7000; port 5000 to zwykle serwer śledzenia eksperymentów, który czatu nie wystawia.

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:7000/v1/chat/completions" -ContentType "application/json" -Body '{"model":"<nazwa endpointu>","messages":[{"role":"user","content":"ping"}]}'
```

Jeśli przyjdzie odpowiedź, ustaw model w tym samym oknie:

```powershell
$env:QA_DEMO_MODEL_DOSTAWCA = "openai"
$env:QA_DEMO_MODEL_NAZWA = "<nazwa endpointu>"
$env:OPENAI_BASE_URL = "http://localhost:7000/v1"
$env:OPENAI_API_KEY = "nieuzywany"
```

Prawdziwy klucz trzyma MLflow. Zmienna `OPENAI_API_KEY` musi być ustawiona, bo bez niej pakiet `langchain-openai` się nie uruchomi, ale jej wartość nie ma znaczenia.

### 2. Próba generalna

```powershell
python -m pytest agenci_langgraph/testy
python -m agenci_langgraph lista
```

Potem przejdź raz każde polecenie z pokazu na modelu z MLflow i sprawdź trzy rzeczy:

- czy model trzyma format skilla: od części „Decyzja człowieka” zależą pytania przy zatrzymaniu;
- jak długo trwa każdy agent; `zestaw` pyta model pięć razy przed zatrzymaniem;
- czy wnioski modelu zgadzają się z `prowadzacy/odpowiedzi-pokazu.md`. Ten plik jest tylko dla prowadzącego; agenty go nie czytają.

## Pokaz: wariant 20 minut (zagadnienia 1, 2, 5)

Przy każdym zatrzymaniu pokaż osobno blok „ZDANIE MODELU” i blok „DECYZJA CZŁOWIEKA”, a na koniec protokół w `wyniki/agenci/`.

| Krok | Polecenie | Co pokazać | Decyzja prowadzącego przy zatrzymaniu |
| --- | --- | --- | --- |
| 1 | `python -m agenci_langgraph zestaw` | luki i pytania do autora; źródło przy każdej pozycji (zdanie wymagania albo reguła modelu) | numery pozycji do zestawu; do pliku zestawu trafiają tylko one |
| 2 | `python -m agenci_langgraph zgloszenie` | klasyfikacja nocnego przebiegu: produkt, test czy środowisko | czy robić szkic zgłoszenia (`tak`), a po szkicu dotkliwość i to, czy zgłoszenie wychodzi |
| 3 | `python -m agenci_langgraph karta` | przy drugim zatrzymaniu jedno zdanie modelu o dwóch buildach w liczbach | pierwsze zatrzymanie (zakres) można zostawić Enterem; potem decyzja o liczbach, na końcu o wydaniu |

## Pokaz pełny: dalsze zagadnienia, po rolach

Na początku tej części pokaż `python -m agenci_langgraph lista`: widać, że każde zagadnienie ma swoje polecenie.

### Tester automatyzujący

1. `python -m agenci_langgraph ocena-asercji` (3): który test nadaje się na bramkę.
2. `python -m agenci_langgraph test-potwierdzajacy --port 8767 --test test_link_dziala_jeden_raz --plik material/zgloszenia/ZGL-101.md` (P2): czy zamknąć zgłoszenie.
3. `python -m agenci_langgraph test-niestabilny --port 8765` (P3): dwanaście przebiegów, decyzja o kwarantannie albo naprawie.
4. `python -m agenci_langgraph przeglad-zmiany-w-testach` (P6): czy przyjąć zmianę w testach.
5. `python -m agenci_langgraph kandydaci-do-automatyzacji` (R3).
6. `python -m agenci_langgraph szkic-testu-automatycznego --prosba "<przypadek potwierdzony w kroku 1>" --plik testy/conftest.py` (R4). Wpisz przypadek potwierdzony w `zestaw`, bo skill pisze test tylko dla przypadku potwierdzonego przez człowieka.

### Tester manualny

1. `python -m agenci_langgraph sesja-eksploracyjna --prosba "karta sesji przed sesją" --plik material/sesja/ryzyka.md` (P5, przed sesją).
2. `python -m agenci_langgraph sesja-eksploracyjna --prosba "raport po sesji" --plik material/sesja/notatki-z-sesji.md` (P5, po sesji).
3. `python -m agenci_langgraph zgloszenie-z-obserwacji --prosba "<godzina obserwacji z notatek>" --plik material/sesja/notatki-z-sesji.md --plik material/zgloszenia/otwarte.json` (R2).
4. `python -m agenci_langgraph projektowanie-przypadkow` (R1).
5. `python -m agenci_langgraph testy-niefunkcjonalne` (R5).

### Zmiana i plan

1. `python -m agenci_langgraph testy-po-zmianie-wymagania --plik testy/conftest.py` (R6).
2. `python -m agenci_langgraph testy-z-opisu-interfejsu` (R7).
3. `python -m agenci_langgraph plan-testow-iteracji --zmiana-wymagania` (R8).

## Uwagi na pokaz

- Okno 1 z `python app/serwer.py` musi działać przez cały pokaz. Lista poleceń mówi, które agenty go potrzebują.
- Ctrl+C przy zatrzymaniu kończy agenta bez zapisu; kolejne uruchomienie zaczyna od początku.
- Każde uruchomienie nadpisuje swój protokół w `wyniki/agenci/`. Protokoły z próby generalnej, które mają zostać, skopiuj przed pokazem.
