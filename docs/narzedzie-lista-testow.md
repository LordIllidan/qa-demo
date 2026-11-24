# Narzędzie: lista_testow.py

Podaje listę testów z opisami.

- Zagadnienia: P4
- Rodzaj wejścia: lista testów
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/lista_testow.py
python narzedzia/lista_testow.py --katalog testy
```

## Co podaje

Tabelę z trzema kolumnami: plik, nazwa testu, opis. Opisem jest docstring funkcji testowej. Skrypt czyta pliki `test_*.py` ze wskazanego katalogu i nie uruchamia testów.

## Co zapisuje

`wyniki/lista-testow.txt`.

## Czego nie robi

Nie przypisuje testów do zdań wymagania i nie mówi, czego brakuje. Wymaganie podaje osobno `wymaganie.py`.
