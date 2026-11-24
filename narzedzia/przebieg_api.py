"""Wykonuje wywołania API z pliku i podaje żądanie oraz odpowiedź.

Użycie:  python narzedzia/przebieg_api.py --port 8765

Skrypt nie porównuje odpowiedzi z opisem interfejsu ani z wymaganiem.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from wspolne import MATERIAL, build_na_porcie, czytaj_json, json_w_wierszu, oddaj, tabela, uruchom_narzedzie, wzgledna, zadanie_http

PLIK_DOMYSLNY = MATERIAL / "api" / "wywolania-reset.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Przebieg wywołań API z pliku.")
    parser.add_argument("--port", type=int, required=True, help="port builda")
    parser.add_argument("--plik", type=Path, default=PLIK_DOMYSLNY, help="plik z listą wywołań")
    argumenty = parser.parse_args()
    build = build_na_porcie(argumenty.port)
    dane = czytaj_json(argumenty.plik)
    wiersze = []
    for wywolanie in dane["wywolania"]:
        status, tresc = zadanie_http(argumenty.port, wywolanie["metoda"], wywolanie["sciezka"], wywolanie.get("dane"))
        wiersze.append([
            wywolanie["id"], wywolanie["opis"], f"{wywolanie['metoda']} {wywolanie['sciezka']}",
            json_w_wierszu(wywolanie.get("dane")), status, json_w_wierszu(tresc),
        ])
    tresc = [
        "## Przebieg API",
        f"plik: {wzgledna(argumenty.plik)}",
        f"build: {build['numer']} (port {build['port']})",
        "",
        *tabela(["id", "opis", "żądanie", "dane", "status", "odpowiedź"], wiersze),
        "",
    ]
    oddaj("przebieg_api.py", "wynik przebiegu API", tresc, f"przebieg-api-{argumenty.port}.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
