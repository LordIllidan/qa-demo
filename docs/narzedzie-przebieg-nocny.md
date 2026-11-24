# Narzędzie: przebieg_nocny.py

Podaje zapisany nocny przebieg: wynik z kilkoma awariami, przebieg referencyjny i log.

- Zagadnienia: P1
- Rodzaj wejścia: wynik przebiegu
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/przebieg_nocny.py
```

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| `material/przebieg-nocny/wynik-8766.json` | `wyniki/przebieg-nocny.txt` |
| `material/przebieg-nocny/wynik-8765.json` | |
| `material/przebieg-nocny/log-8766.txt` | |

## Co podaje

1. Nocny przebieg na buildzie 1.5.0: dziesięć testów, każdy z opisem, wynikiem, komunikatem i wymianą z aplikacją.
2. Przebieg referencyjny tego samego zestawu na buildzie 1.4.0.
3. Log nocnego przebiegu z wpisami trzech źródeł: przebiegu, aplikacji i środowiska.

Wyniki mają ten sam układ co wynik skryptu `przebieg.py`. Pole `pochodzenie` mówi, że to materiał przygotowany, a nie wynik uruchomienia.

## Czego nie robi

Niczego nie uruchamia. Nie grupuje awarii, nie porównuje przebiegów i nie dopasowuje wpisów logu do testów.
