# Narzędzie: lokalizatory.py

Sprawdza, które lokalizatory pasują do dwóch wersji pliku HTML.

- Zagadnienia: R17
- Rodzaj wejścia: lokalizatory wobec dwóch wersji strony
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/lokalizatory.py
python narzedzia/lokalizatory.py --plik material/ui/lokalizatory.json
```

| Opcja | Znaczenie |
| --- | --- |
| `--plik` | plik JSON z lokalizatorami i ścieżkami obu wersji; domyślnie `material/ui/lokalizatory.json` |

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| plik lokalizatorów i dwa pliki HTML, które wskazuje | `wyniki/lokalizatory.txt` |

Selektor `#id` pasuje, gdy w pliku jest `id="id"`. Selektor zaczynający się od `tekst ` pasuje, gdy tekst po dwukropku jest w pliku.

## Czego nie robi

Nie proponuje nowego selektora i nie uruchamia przeglądarki.
