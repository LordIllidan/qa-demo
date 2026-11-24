"""Podaje tekst wymagania.

Użycie:  python narzedzia/wymaganie.py reset-hasla
         python narzedzia/wymaganie.py filtr-zamowien
"""

from __future__ import annotations

import argparse

from wspolne import MATERIAL, BladNarzedzia, czytaj_tekst, oddaj, uruchom_narzedzie, wzgledna

KATALOG_WYMAGAN = MATERIAL / "wymagania"


def dostepne() -> list:
    return sorted(plik.stem for plik in KATALOG_WYMAGAN.glob("*.md"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Podaje tekst wymagania.")
    parser.add_argument("nazwa", nargs="?", help="nazwa wymagania: " + ", ".join(dostepne()))
    argumenty = parser.parse_args()
    if argumenty.nazwa not in dostepne():
        raise BladNarzedzia("podaj nazwę wymagania; dostępne: " + ", ".join(dostepne()))

    plik = KATALOG_WYMAGAN / f"{argumenty.nazwa}.md"
    tresc = [
        "## Wymaganie",
        f"plik: {wzgledna(plik)}",
        "",
        czytaj_tekst(plik).rstrip("\n"),
        "",
    ]
    oddaj("wymaganie.py", "wymaganie", tresc, f"wymaganie-{argumenty.nazwa}.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
