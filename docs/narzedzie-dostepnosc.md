# Narzędzie: dostepnosc.py

Wypisuje z HTML stron resetu język, nagłówki, obrazki, pola formularza i przyciski.

- Zagadnienia: R16
- Rodzaj wejścia: inwentarz HTML
- Wymaga działającej aplikacji

## Użycie

```powershell
python narzedzia/dostepnosc.py --port 8765
```

| Opcja | Znaczenie |
| --- | --- |
| `--port` | port builda |

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| `GET /` i `GET /reset` | `wyniki/dostepnosc-<port>.txt` |

Przy polu podaje, czy jest etykieta `label for` o tym samym identyfikatorze. Przy obrazkach liczy te bez atrybutu `alt`.

## Czego nie robi

Nie liczy kontrastu, fokusu ani zgodności z normą i nie mówi, czy strona jest dostępna.
