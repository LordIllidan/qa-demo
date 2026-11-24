"""Podaje zdanie o zmianie i listę sprawdzeń z czasami wykonania.

Użycie:  python narzedzia/lista_sprawdzen.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from wspolne import MATERIAL, czytaj_json, oddaj, tabela, uruchom_narzedzie, wzgledna

PLIK_DOMYSLNY = MATERIAL / "zakres" / "lista-sprawdzen.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Podaje listę sprawdzeń z czasami.")
    parser.add_argument("--plik", type=Path, default=PLIK_DOMYSLNY, help="plik z listą sprawdzeń")
    argumenty = parser.parse_args()

    dane = czytaj_json(argumenty.plik)
    wiersze = [[s["id"], s["obszar"], s["sprawdzenie"], s["czas_min"]] for s in dane["sprawdzenia"]]
    tresc = [
        "## Zmiana i okno czasu",
        f"zdanie o zmianie: {dane['zmiana']}",
        f"wymaganie: {dane['wymaganie']}",
        "",
        "## Lista sprawdzeń",
        f"plik: {wzgledna(argumenty.plik)}",
        "",
        *tabela(["id", "obszar", "sprawdzenie", "czas wykonania [min]"], wiersze),
        "",
    ]
    oddaj("lista_sprawdzen.py", "lista sprawdzeń z czasami", tresc, "lista-sprawdzen.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
