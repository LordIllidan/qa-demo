"""Sprawdza, które lokalizatory pasują do dwóch wersji strony.

Użycie:  python narzedzia/lokalizatory.py

Selektor „#id” pasuje, gdy w pliku jest id="id". Selektor „tekst …: …”
pasuje, gdy ten tekst jest w pliku. Skrypt nie proponuje nowego lokalizatora.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from wspolne import KATALOG, MATERIAL, czytaj_json, czytaj_tekst, oddaj, tabela, uruchom_narzedzie, wzgledna

PLIK_DOMYSLNY = MATERIAL / "ui" / "lokalizatory.json"


def pasuje(selektor: str, html: str) -> str:
    if selektor.startswith("#"):
        return "pasuje" if f'id="{selektor[1:]}"' in html else "nie pasuje"
    if selektor.startswith("tekst "):
        tekst = selektor.split(": ", 1)[1]
        return "pasuje" if tekst in html else "nie pasuje"
    return "selektor spoza obsługiwanych: #id oraz tekst …: …"


def main() -> None:
    parser = argparse.ArgumentParser(description="Lokalizatory wobec dwóch wersji strony.")
    parser.add_argument("--plik", type=Path, default=PLIK_DOMYSLNY, help="plik z lokalizatorami i ścieżkami stron")
    argumenty = parser.parse_args()
    dane = czytaj_json(argumenty.plik)
    przed = czytaj_tekst(KATALOG / dane["przed"])
    po = czytaj_tekst(KATALOG / dane["po"])
    wiersze = [
        [lokalizator["id"], lokalizator["opis"], lokalizator["selektor"],
         pasuje(lokalizator["selektor"], przed), pasuje(lokalizator["selektor"], po)]
        for lokalizator in dane["lokalizatory"]
    ]
    tresc = [
        "## Lokalizatory",
        f"plik: {wzgledna(argumenty.plik)}",
        f"wersja przed: {dane['przed']}",
        f"wersja po: {dane['po']}",
        "",
        *tabela(["id", "opis", "selektor", "przed", "po"], wiersze),
        "",
    ]
    oddaj("lokalizatory.py", "lokalizatory wobec dwóch wersji strony", tresc, "lokalizatory.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
