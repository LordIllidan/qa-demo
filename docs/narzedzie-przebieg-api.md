# Narzędzie: przebieg_api.py

Wykonuje wywołania API z pliku i podaje żądanie, status i treść odpowiedzi.

- Zagadnienia: R13
- Rodzaj wejścia: wynik przebiegu API
- Wymaga działającej aplikacji

## Użycie

```powershell
python narzedzia/przebieg_api.py --port 8765
python narzedzia/przebieg_api.py --port 8765 --plik material/api/wywolania-reset.json
```

| Opcja | Znaczenie |
| --- | --- |
| `--port` | port builda |
| `--plik` | plik JSON z listą wywołań; domyślnie `material/api/wywolania-reset.json` |

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| plik wywołań | `wyniki/przebieg-api-<port>.txt` |

Każde wywołanie ma identyfikator, opis, metodę, ścieżkę i dane. Skrypt wysyła je po kolei.

## Czego nie robi

Nie porównuje odpowiedzi z opisem interfejsu ani z wymaganiem.
