# Narzędzie: przypadki_reczne.py

Podaje przypadki testowe ręczne z warunkami początkowymi, krokami i oczekiwanymi wynikami.

- Zagadnienia: R11
- Rodzaj wejścia: przypadki testowe ręczne
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/przypadki_reczne.py
python narzedzia/przypadki_reczne.py --plik material/przypadki-reczne/reset-hasla.json
```

| Opcja | Znaczenie |
| --- | --- |
| `--plik` | plik JSON z przypadkami; domyślnie `material/przypadki-reczne/reset-hasla.json` |

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| plik z listą `przypadki` | `wyniki/przypadki-reczne.txt` |

Dla każdego przypadku podaje tytuł, warunki początkowe i tabelę kroków. Puste warunki i pusty oczekiwany wynik zapisuje jako „(puste)”.

Plik bez listy `przypadki` kończy pracę kodem wyjścia 2.

## Czego nie robi

Nie ocenia przypadków i nie porównuje ich z wymaganiem.
