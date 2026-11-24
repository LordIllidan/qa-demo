"""Podaje różnicę dwóch wersji pliku z testami oraz wyniki obu wersji na dwóch buildach.

Użycie:  python narzedzia/zmiana_w_testach.py
         python narzedzia/zmiana_w_testach.py --porty 8765 8766

Wersja przed zmianą to testy/test_reset_hasla.py, wersja po zmianie leży
w material/zmiana-w-testach. Skrypt niczego w testach nie zmienia.
"""

from __future__ import annotations

import argparse
import difflib

from wspolne import (
    KATALOG,
    WYNIKI,
    czytaj_tekst,
    oddaj,
    opisz_build,
    opisz_test,
    tabela,
    uruchom_narzedzie,
    uruchom_testy,
    zapisz_json,
)

PRZED = "testy/test_reset_hasla.py"
PO = "material/zmiana-w-testach/test_reset_hasla.py"
OPIS = "material/zmiana-w-testach/opis-zmiany.md"
PORTY_DOMYSLNE = [8765, 8766]


def main() -> None:
    parser = argparse.ArgumentParser(description="Różnica wersji testów i wyniki przed zmianą oraz po niej.")
    parser.add_argument("--porty", type=int, nargs="+", default=PORTY_DOMYSLNE)
    argumenty = parser.parse_args()

    przed = czytaj_tekst(KATALOG / PRZED)
    po = czytaj_tekst(KATALOG / PO)
    roznica = list(difflib.unified_diff(
        przed.splitlines(), po.splitlines(),
        fromfile=f"przed zmianą: {PRZED}", tofile=f"po zmianie: {PO}", lineterm="", n=3,
    ))

    przebiegi = []
    for port in argumenty.porty:
        przebiegi.append(("przed zmianą", uruchom_testy(port, PRZED)))
        przebiegi.append(("po zmianie", uruchom_testy(port, PO)))

    nazwy = []
    for _, przebieg in przebiegi:
        for test in przebieg["testy"]:
            if test["nazwa"] not in nazwy:
                nazwy.append(test["nazwa"])

    def wynik(przebieg: dict, nazwa: str) -> str:
        for test in przebieg["testy"]:
            if test["nazwa"] == nazwa:
                return test["wynik"]
        return "nie ma testu"

    naglowki = ["test"] + [f"build {opisz_build(p['build'])}, {wersja}" for wersja, p in przebiegi]
    tresc = [
        "## Opis zmiany od autora",
        f"plik: {OPIS}",
        "",
        czytaj_tekst(KATALOG / OPIS).rstrip("\n"),
        "",
        "## Różnica wersji pliku z testami",
        "",
        "```diff",
        *roznica,
        "```",
        "",
        "## Wyniki przed zmianą i po zmianie",
        "",
        *tabela(naglowki, [[nazwa] + [wynik(p, nazwa) for _, p in przebiegi] for nazwa in nazwy]),
        "",
        "## Szczegóły uruchomień z wynikiem innym niż zaliczony",
        "",
    ]
    szczegoly = 0
    for wersja, przebieg in przebiegi:
        for test in przebieg["testy"]:
            if test["wynik"] != "zaliczony":
                szczegoly += 1
                tresc.append(f"### Build {opisz_build(przebieg['build'])}, {wersja}")
                tresc += opisz_test(test, poziom="####")
    if not szczegoly:
        tresc += ["brak takich uruchomień", ""]

    plik_json = WYNIKI / "zmiana-w-testach.json"
    zapisz_json(plik_json, {
        "format": "qa-demo/zmiana-w-testach/1",
        "przed": PRZED,
        "po": PO,
        "roznica": roznica,
        "przebiegi": [{"wersja": wersja, **przebieg} for wersja, przebieg in przebiegi],
    })
    oddaj("zmiana_w_testach.py", "wynik przebiegu", tresc, "zmiana-w-testach.txt", [plik_json])


if __name__ == "__main__":
    uruchom_narzedzie(main)
