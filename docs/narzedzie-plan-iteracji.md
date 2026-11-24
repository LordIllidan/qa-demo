# Narzędzie: plan_iteracji.py

Podaje dane iteracji, listę ryzyk, otwarte zgłoszenia i treść historii iteracji w jednym wejściu.

- Zagadnienia: R8
- Rodzaj wejścia: dane iteracji
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/plan_iteracji.py
python narzedzia/plan_iteracji.py --plik material/plan/iteracja.json
```

| Opcja | Znaczenie |
| --- | --- |
| `--plik` | plik z danymi iteracji; domyślnie `material/plan/iteracja.json` |

## Co czyta i co zapisuje

| Czyta | Rola |
| --- | --- |
| plik z danymi iteracji | historie, zespół, środowisko, ustalenia |
| `material/sesja/ryzyka.md` | lista ryzyk z poziomami ustalonymi przez zespół |
| `material/zgloszenia/otwarte.json` | otwarte zgłoszenia |
| pliki historii wskazane w danych iteracji | treść historii |

Zapisuje `wyniki/plan-iteracji.txt`.

## Format pliku z danymi iteracji

```json
{
  "format": "qa-demo/iteracja/1",
  "iteracja": "<nazwa>",
  "od": "<data>",
  "do": "<data>",
  "wydanie": "<numer wydania>",
  "historie": [{"id": "<id>", "tytul": "<tytuł>", "plik": "<ścieżka do historii>", "uwagi": "<uwagi>"}],
  "zespol": [{"osoba": "<imię>", "rola": "<rola>", "godziny_na_testy": 0}],
  "srodowisko": ["<wpis>"],
  "ustalenia_zespolu": ["<wpis>"]
}
```

## Czego nie robi

Nie szacuje pracy, nie przypisuje zadań, nie ustala zakresu i nie łączy ryzyk z historiami.
