# Narzędzie: zmiana_w_testach.py

Podaje różnicę dwóch wersji pliku z testami oraz wyniki obu wersji na dwóch buildach.

- Zagadnienia: P6
- Rodzaj wejścia: wynik przebiegu
- Wymaga działającej aplikacji

## Użycie

```powershell
python narzedzia/zmiana_w_testach.py
python narzedzia/zmiana_w_testach.py --porty 8765 8766
```

## Co czyta

| Plik | Rola |
| --- | --- |
| `testy/test_reset_hasla.py` | wersja przed zmianą |
| `material/zmiana-w-testach/test_reset_hasla.py` | wersja po zmianie |
| `material/zmiana-w-testach/opis-zmiany.md` | opis zmiany od autora |

## Co podaje

1. Opis zmiany od autora.
2. Różnicę wersji w układzie `diff`.
3. Tabelę wyników: wiersz na test, kolumny dla każdego builda przed zmianą i po zmianie. Test, którego w danej wersji nie ma, ma wpis „nie ma testu”.
4. Szczegóły uruchomień z wynikiem innym niż zaliczony.

## Co zapisuje

`wyniki/zmiana-w-testach.txt` i `wyniki/zmiana-w-testach.json`.

## Czego nie robi

Nie zmienia żadnego pliku z testami: wersję po zmianie uruchamia z katalogu `material`. Nie klasyfikuje fragmentów różnicy i nie mówi, czy zmiana osłabia testy.
