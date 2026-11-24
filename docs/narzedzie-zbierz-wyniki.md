# Narzędzie: zbierz_wyniki.py

Zbiera w jeden plik wyniki przebiegów, liczby, otwarte zgłoszenia i zakres planowany oraz wykonany.

- Zagadnienia: 6
- Rodzaj wejścia: wynik przebiegu i liczby
- Aplikacja nie musi działać

## Użycie

Najpierw zapisz przebiegi, potem zbierz wyniki:

```powershell
python narzedzia/przebieg.py --port 8765
python narzedzia/przebieg.py --port 8766
python narzedzia/zbierz_wyniki.py
```

Opcja `--porty` wskazuje, których buildów zapisane przebiegi mają trafić do zbioru (domyślnie 8765 i 8766).

## Co czyta

| Plik | Co z niego trafia do zbioru |
| --- | --- |
| `wyniki/przebieg-<port>.json` | ostatni zapisany przebieg builda: liczby testów, tabela wyników, szczegóły testów z wynikiem innym niż zaliczony |
| `material/liczby/build-8765.json`, `material/liczby/build-8766.json` | profil, metryki i progi każdej ścieżki |
| `material/zgloszenia/otwarte.json` | lista otwartych zgłoszeń |
| `material/zakres/zakres-wydania.json` | pozycje planu ze stanem wykonania |

Gdy pliku przebiegu dla portu nie ma, w zbiorze stoi wpis o braku pliku. Skrypt nie uruchamia wtedy testów sam.

## Co zapisuje

`wyniki/zbior-wynikow.txt` i `wyniki/zbior-wynikow.json`.

## Czego nie robi

Nie podsumowuje, nie wybiera tego, co ważne, i nie formułuje wniosku. Nie zawiera żadnego zdania o wydaniu.
