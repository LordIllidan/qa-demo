"""Podaje listę testów z opisami.

Użycie:  python narzedzia/lista_testow.py
         python narzedzia/lista_testow.py --katalog testy
"""

from __future__ import annotations

import argparse
import ast
from pathlib import Path

from wspolne import TESTY, BladNarzedzia, czytaj_tekst, oddaj, tabela, uruchom_narzedzie, wzgledna


def testy_z_pliku(plik: Path) -> list:
    drzewo = ast.parse(czytaj_tekst(plik))
    wynik = []
    for wezel in drzewo.body:
        if isinstance(wezel, ast.FunctionDef) and wezel.name.startswith("test_"):
            opis = " ".join((ast.get_docstring(wezel) or "").split())
            wynik.append([wzgledna(plik), wezel.name, opis or "brak opisu"])
    return wynik


def main() -> None:
    parser = argparse.ArgumentParser(description="Podaje listę testów z opisami.")
    parser.add_argument("--katalog", type=Path, default=TESTY, help="katalog z plikami test_*.py")
    argumenty = parser.parse_args()
    if not argumenty.katalog.is_dir():
        raise BladNarzedzia(f"nie ma katalogu {wzgledna(argumenty.katalog)}")

    wiersze = []
    for plik in sorted(argumenty.katalog.glob("test_*.py")):
        wiersze += testy_z_pliku(plik)
    if not wiersze:
        raise BladNarzedzia(f"w katalogu {wzgledna(argumenty.katalog)} nie ma testów")

    tresc = [
        "## Lista testów",
        f"katalog: {wzgledna(argumenty.katalog)}",
        f"liczba testów: {len(wiersze)}",
        "opis testu to docstring funkcji testowej",
        "",
        *tabela(["plik", "test", "opis"], wiersze),
        "",
    ]
    oddaj("lista_testow.py", "lista testów", tresc, "lista-testow.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
