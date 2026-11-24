"""Podaje przypadki testowe ręczne z krokami i oczekiwanymi wynikami.

Użycie:  python narzedzia/przypadki_reczne.py
         python narzedzia/przypadki_reczne.py --plik material/przypadki-reczne/reset-hasla.json

Skrypt przepisuje przypadki tak, jak je zapisano. Nie ocenia ich i nie
porównuje z wymaganiem.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from wspolne import MATERIAL, BladNarzedzia, czytaj_json, oddaj, tabela, uruchom_narzedzie, wzgledna

PLIK_DOMYSLNY = MATERIAL / "przypadki-reczne" / "reset-hasla.json"
BRAK = "(puste)"


def main() -> None:
    parser = argparse.ArgumentParser(description="Przypadki testowe ręczne do przeglądu.")
    parser.add_argument("--plik", type=Path, default=PLIK_DOMYSLNY, help="plik z przypadkami w JSON")
    argumenty = parser.parse_args()

    dane = czytaj_json(argumenty.plik)
    if "przypadki" not in dane:
        raise BladNarzedzia(f"plik {wzgledna(argumenty.plik)} nie ma listy przypadki")

    tresc = [
        "## Przypadki ręczne",
        f"plik: {wzgledna(argumenty.plik)}",
        f"wymaganie: {dane.get('wymaganie') or 'nie podano'}",
        f"autor: {dane.get('autor') or 'nie podano'}",
        f"liczba przypadków: {len(dane['przypadki'])}",
        "",
    ]
    for przypadek in dane["przypadki"]:
        tresc += [
            f"### {przypadek['id']}: {przypadek['tytul']}",
            f"warunki początkowe: {przypadek.get('warunki_poczatkowe') or BRAK}",
            "",
            *tabela(["krok", "czynność", "oczekiwany wynik"],
                    [[n, k["krok"], k.get("oczekiwany") or BRAK] for n, k in enumerate(przypadek["kroki"], start=1)]),
            "",
        ]
    oddaj("przypadki_reczne.py", "przypadki testowe ręczne", tresc, "przypadki-reczne.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
