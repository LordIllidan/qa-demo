# Narzędzie: historia.py

Uruchamia ten sam zestaw testów wiele razy na jednym buildzie i podaje historię wyników.

- Zagadnienia: P3
- Rodzaj wejścia: wynik przebiegu
- Wymaga działającej aplikacji

## Użycie

```powershell
python narzedzia/historia.py --port 8765
python narzedzia/historia.py --port 8765 --powtorzenia 20
```

| Opcja | Znaczenie |
| --- | --- |
| `--port` | port builda; wymagana |
| `--powtorzenia` | liczba przebiegów; domyślnie 12 |
| `--zestaw` | plik albo katalog z testami; domyślnie cały katalog `testy` |

Domyślny zestaw obejmuje oba pliki z testami opisane w `docs/testy.md`. Dwanaście przebiegów trwa od kilku do kilkunastu sekund.

## Co podaje

1. Tabelę wyników: wiersz na test, kolumna na przebieg.
2. Tabelę czasów testów w tym samym układzie.
3. Szczegóły każdego uruchomienia z wynikiem innym niż zaliczony: komunikat, wiersz zatrzymania, wymianę z aplikacją.

## Co zapisuje

| Plik | Zawartość |
| --- | --- |
| `wyniki/historia-<port>.txt` | tekst w stałej ramce |
| `wyniki/historia-<port>.json` | wszystkie przebiegi, także uruchomienia zaliczone, z pełną wymianą |

Dwie historie mogą się od siebie różnić. Plik `.json` pozwala wrócić do tej samej historii.

## Czego nie robi

Nie liczy, ile razy test nie przeszedł, nie nazywa żadnego testu niestabilnym i nie ponawia testów w ramach jednego przebiegu. Każdy przebieg to jedno zwykłe uruchomienie zestawu.
