"""Podaje dwie wersje wymagania, różnicę zdań, opis zmiany od autora i listę testów.

Użycie:  python narzedzia/zmiana_wymagania.py

Wersja obecna to material/wymagania/reset-hasla.md, wersja po zmianie leży
w material/zmiana-wymagania. Skrypt niczego w testach nie zmienia i nie
mówi, których testów zmiana dotyczy.
"""

from __future__ import annotations

import argparse
import difflib
import re

from lista_testow import testy_z_pliku
from wspolne import KATALOG, TESTY, czytaj_tekst, oddaj, tabela, uruchom_narzedzie

PRZED = "material/wymagania/reset-hasla.md"
PO = "material/zmiana-wymagania/reset-hasla.md"
OPIS = "material/zmiana-wymagania/opis-zmiany.md"

ZDANIE = re.compile(r"^- (R\d+)\. (.+)$")
WIERSZ_INTERFEJSU = re.compile(r"^\| ([^|]+?) \| (`[^|]+?) \| ([^|]+?) \|$")


def elementy(tekst: str) -> dict:
    """Zdania kryteriów akceptacji i wiersze tabeli interfejsu, każde pod swoim kluczem."""
    wynik = {}
    for wiersz in tekst.splitlines():
        if (zdanie := ZDANIE.match(wiersz)):
            wynik[zdanie.group(1)] = zdanie.group(2)
        elif (operacja := WIERSZ_INTERFEJSU.match(wiersz)):
            wynik[f"interfejs: {operacja.group(1)}"] = f"{operacja.group(2)} -> {operacja.group(3)}"
    return wynik


def main() -> None:
    argparse.ArgumentParser(description="Dwie wersje wymagania, różnica zdań i lista testów.").parse_args()

    przed = czytaj_tekst(KATALOG / PRZED)
    po = czytaj_tekst(KATALOG / PO)
    stare, nowe = elementy(przed), elementy(po)

    wiersze = []
    for klucz in list(stare) + [k for k in nowe if k not in stare]:
        if klucz not in nowe:
            stan = "usunięte"
        elif klucz not in stare:
            stan = "dodane"
        elif stare[klucz] != nowe[klucz]:
            stan = "zmienione"
        else:
            stan = "bez zmian"
        wiersze.append([klucz, stan, stare.get(klucz, "–"), nowe.get(klucz, "–")])

    roznica = list(difflib.unified_diff(
        przed.splitlines(), po.splitlines(),
        fromfile=f"wersja obecna: {PRZED}", tofile=f"wersja po zmianie: {PO}", lineterm="", n=1,
    ))

    testy = []
    for plik in sorted(TESTY.glob("test_*.py")):
        testy += testy_z_pliku(plik)

    tresc = [
        "## Opis zmiany od autora",
        f"plik: {OPIS}",
        "",
        czytaj_tekst(KATALOG / OPIS).rstrip("\n"),
        "",
        "## Zdania i wiersze interfejsu w obu wersjach",
        "stan to wynik porównania tekstu, a nie ocena zmiany",
        "",
        *tabela(["element", "stan", "wersja obecna", "wersja po zmianie"], wiersze),
        "",
        "## Różnica wersji wymagania",
        "",
        "```diff",
        *roznica,
        "```",
        "",
        "## Lista testów",
        "kod testów leży w katalogu testy; wspólne zaplecze w testy/conftest.py",
        "",
        *tabela(["plik", "test", "opis"], testy),
        "",
    ]
    oddaj("zmiana_wymagania.py", "zmiana wymagania", tresc, "zmiana-wymagania.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
