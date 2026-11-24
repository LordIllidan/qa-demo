# Narzędzie: tabela_asercji.py

Podaje kod dwóch testów i tabelę ich wyników na dwóch buildach.

- Zagadnienia: 3
- Rodzaj wejścia: wynik przebiegu
- Wymaga działającej aplikacji

## Użycie

```powershell
python narzedzia/tabela_asercji.py
python narzedzia/tabela_asercji.py --porty 8765 8766 --testy test_link_dziala_jeden_raz test_wystarczy_kod_200
```

| Opcja | Znaczenie |
| --- | --- |
| `--porty` | porty buildów; domyślnie 8765 i 8766 |
| `--testy` | nazwy testów; domyślnie `test_link_dziala_jeden_raz` i `test_wystarczy_kod_200` |
| `--zestaw` | plik z testami; domyślnie `testy/test_reset_hasla.py` |

## Co podaje

1. Kod źródłowy wskazanych testów.
2. Tabelę: wiersz na test, kolumna na build, w komórce wynik testu.
3. Szczegóły każdego uruchomienia razem z wymianą żądań i odpowiedzi.

Układ tabeli dla ustawień domyślnych:

| test | build 1.4.0 (port 8765) | build 1.5.0 (port 8766) |
| --- | --- | --- |
| test_link_dziala_jeden_raz | <wynik> | <wynik> |
| test_wystarczy_kod_200 | <wynik> | <wynik> |

Wypełniona tabela jest w pliku dla prowadzącego `prowadzacy/odpowiedzi-pokazu.md`.

## Co zapisuje

`wyniki/tabela-asercji.txt` i `wyniki/tabela-asercji.json`.

## Czego nie robi

Nie mówi, który test jest lepszy, i nie zmienia kodu testów. Wymagania nie podaje; służy do tego `wymaganie.py`.
