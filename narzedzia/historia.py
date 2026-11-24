"""Uruchamia ten sam zestaw testów wiele razy na jednym buildzie i podaje historię wyników.

Użycie:  python narzedzia/historia.py --port 8765
         python narzedzia/historia.py --port 8765 --powtorzenia 20
"""

from __future__ import annotations

import argparse

from wspolne import (
    WYNIKI,
    BladNarzedzia,
    oddaj,
    opisz_build,
    opisz_test,
    tabela,
    uruchom_narzedzie,
    uruchom_testy,
    zapisz_json,
)

ZESTAW_DOMYSLNY = "testy"
POWTORZENIA_DOMYSLNE = 12


def main() -> None:
    parser = argparse.ArgumentParser(description="Historia wyników tego samego zestawu na jednym buildzie.")
    parser.add_argument("--port", type=int, required=True, help="port builda")
    parser.add_argument("--powtorzenia", type=int, default=POWTORZENIA_DOMYSLNE,
                        help=f"liczba przebiegów (domyślnie {POWTORZENIA_DOMYSLNE})")
    parser.add_argument("--zestaw", default=ZESTAW_DOMYSLNY,
                        help=f"plik albo katalog z testami (domyślnie {ZESTAW_DOMYSLNY})")
    argumenty = parser.parse_args()
    if argumenty.powtorzenia < 1:
        raise BladNarzedzia("liczba powtórzeń musi być dodatnia")

    przebiegi = [uruchom_testy(argumenty.port, argumenty.zestaw) for _ in range(argumenty.powtorzenia)]
    build = przebiegi[0]["build"]
    numery = list(range(1, len(przebiegi) + 1))
    nazwy = []
    for przebieg in przebiegi:
        for test in przebieg["testy"]:
            if test["nazwa"] not in nazwy:
                nazwy.append(test["nazwa"])

    def komorka(przebieg: dict, nazwa: str, pole: str):
        for test in przebieg["testy"]:
            if test["nazwa"] == nazwa:
                return test[pole]
        return "brak"

    naglowki = ["test"] + [f"przebieg {n}" for n in numery]
    tresc = [
        "## Historia przebiegów",
        f"build: {opisz_build(build)}",
        "pochodzenie: uruchomienie",
        f"zestaw: {argumenty.zestaw}",
        f"liczba przebiegów: {len(przebiegi)}",
        f"pierwszy start: {przebiegi[0]['start']}",
        f"ostatni start: {przebiegi[-1]['start']}",
        "",
        "## Wyniki testów w kolejnych przebiegach",
        "",
        *tabela(naglowki, [[nazwa] + [komorka(p, nazwa, "wynik") for p in przebiegi] for nazwa in nazwy]),
        "",
        "## Czasy testów w kolejnych przebiegach [ms]",
        "",
        *tabela(naglowki, [[nazwa] + [komorka(p, nazwa, "czas_ms") for p in przebiegi] for nazwa in nazwy]),
        "",
        "## Szczegóły uruchomień z wynikiem innym niż zaliczony",
        "",
    ]
    szczegoly = 0
    for numer, przebieg in zip(numery, przebiegi):
        for test in przebieg["testy"]:
            if test["wynik"] != "zaliczony":
                szczegoly += 1
                tresc.append(f"### Przebieg {numer}")
                tresc += opisz_test(test, poziom="####")
    if not szczegoly:
        tresc += ["brak takich uruchomień", ""]
    tresc += [
        "Pełny zapis wszystkich uruchomień, także zaliczonych, razem z wymianą z aplikacją:",
        f"wyniki/historia-{argumenty.port}.json",
        "",
    ]

    plik_json = WYNIKI / f"historia-{argumenty.port}.json"
    zapisz_json(plik_json, {
        "format": "qa-demo/historia/1",
        "pochodzenie": "uruchomienie",
        "build": build,
        "zestaw": argumenty.zestaw,
        "przebiegi": przebiegi,
    })
    oddaj("historia.py", "wynik przebiegu", tresc, f"historia-{argumenty.port}.txt", [plik_json])


if __name__ == "__main__":
    uruchom_narzedzie(main)
