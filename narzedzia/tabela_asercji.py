"""Podaje kod dwóch testów i tabelę ich wyników na dwóch buildach.

Użycie:  python narzedzia/tabela_asercji.py
         python narzedzia/tabela_asercji.py --porty 8765 8766 --testy test_link_dziala_jeden_raz test_wystarczy_kod_200
"""

from __future__ import annotations

import argparse
import ast

from wspolne import (
    KATALOG,
    WYNIKI,
    ZESTAW_DOMYSLNY,
    BladNarzedzia,
    czytaj_tekst,
    oddaj,
    opisz_build,
    opisz_test,
    tabela,
    uruchom_narzedzie,
    uruchom_testy,
    zapisz_json,
)

TESTY_DOMYSLNE = ["test_link_dziala_jeden_raz", "test_wystarczy_kod_200"]
PORTY_DOMYSLNE = [8765, 8766]


def kod_testow(zestaw: str, nazwy: list) -> dict:
    zrodlo = czytaj_tekst(KATALOG / zestaw)
    funkcje = {
        wezel.name: ast.get_source_segment(zrodlo, wezel)
        for wezel in ast.parse(zrodlo).body
        if isinstance(wezel, ast.FunctionDef)
    }
    brakujace = [nazwa for nazwa in nazwy if nazwa not in funkcje]
    if brakujace:
        raise BladNarzedzia(f"w pliku {zestaw} nie ma testów: {', '.join(brakujace)}")
    return {nazwa: funkcje[nazwa] for nazwa in nazwy}


def main() -> None:
    parser = argparse.ArgumentParser(description="Tabela wyników wybranych testów na wybranych buildach.")
    parser.add_argument("--porty", type=int, nargs="+", default=PORTY_DOMYSLNE)
    parser.add_argument("--testy", nargs="+", default=TESTY_DOMYSLNE)
    parser.add_argument("--zestaw", default=ZESTAW_DOMYSLNY)
    argumenty = parser.parse_args()

    kod = kod_testow(argumenty.zestaw, argumenty.testy)
    przebiegi = [uruchom_testy(port, argumenty.zestaw, argumenty.testy) for port in argumenty.porty]

    tresc = ["## Kod testów", f"plik: {argumenty.zestaw}", ""]
    for nazwa in argumenty.testy:
        tresc += ["```python", kod[nazwa], "```", ""]

    tresc += ["## Wyniki testów na buildach", ""]
    naglowki = ["test"] + [f"build {opisz_build(p['build'])}" for p in przebiegi]
    wiersze = []
    for nazwa in argumenty.testy:
        wyniki = [next(t["wynik"] for t in p["testy"] if t["nazwa"] == nazwa) for p in przebiegi]
        wiersze.append([nazwa] + wyniki)
    tresc += tabela(naglowki, wiersze) + [""]

    tresc += ["## Szczegóły każdego uruchomienia", ""]
    for przebieg in przebiegi:
        tresc += [f"### Build {opisz_build(przebieg['build'])}", ""]
        for test in przebieg["testy"]:
            tresc += opisz_test(test, poziom="####")

    plik_json = WYNIKI / "tabela-asercji.json"
    zapisz_json(plik_json, {"format": "qa-demo/tabela-asercji/1", "kod_testow": kod, "przebiegi": przebiegi})
    oddaj("tabela_asercji.py", "wynik przebiegu", tresc, "tabela-asercji.txt", [plik_json])


if __name__ == "__main__":
    uruchom_narzedzie(main)
