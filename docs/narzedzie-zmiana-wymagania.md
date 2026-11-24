# Narzędzie: zmiana_wymagania.py

Podaje dwie wersje wymagania resetu hasła, ich porównanie zdanie po zdaniu, opis zmiany od autorki i listę testów.

- Zagadnienia: R6, R8
- Rodzaj wejścia: zmiana wymagania
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/zmiana_wymagania.py
```

## Co czyta i co zapisuje

| Czyta | Rola |
| --- | --- |
| `material/wymagania/reset-hasla.md` | wersja obecna, realizowana przez aplikację demonstracyjną |
| `material/zmiana-wymagania/reset-hasla.md` | wersja po zmianie |
| `material/zmiana-wymagania/opis-zmiany.md` | opis zmiany od autorki |
| `testy/test_*.py` | nazwy i opisy testów |

Zapisuje `wyniki/zmiana-wymagania.txt`.

## Co podaje

1. Opis zmiany od autorki.
2. Tabelę zdań kryteriów akceptacji (`R1`, `R2`, …) i wierszy tabeli interfejsu z obu wersji. Kolumna „stan” ma jedną z wartości: „bez zmian”, „zmienione”, „dodane”, „usunięte”. To wynik porównania tekstu.
3. Różnicę obu plików w układzie `diff`.
4. Listę testów z opisami, w tym samym układzie co `lista_testow.py`.

## Czego nie robi

Nie zmienia testów i ich nie uruchamia. Nie mówi, których testów dotyczy zmiana, i nie porównuje opisu zmiany z tekstem wymagania.
