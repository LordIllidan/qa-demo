"""Podaje opis interfejsu w formacie OpenAPI jako tabelę operacji.

Użycie:  python narzedzia/opis_interfejsu.py
         python narzedzia/opis_interfejsu.py --plik material/interfejs/reset-hasla.json

Skrypt nie porównuje opisu z wymaganiem ani z aplikacją.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from wspolne import MATERIAL, BladNarzedzia, czytaj_json, json_w_wierszu, oddaj, tabela, uruchom_narzedzie, wzgledna

PLIK_DOMYSLNY = MATERIAL / "interfejs" / "reset-hasla.json"


def schemat(wezel: dict, komponenty: dict) -> dict:
    if "$ref" in wezel:
        return komponenty.get(wezel["$ref"].rsplit("/", 1)[-1], {})
    return wezel


def pola(wezel: dict, komponenty: dict) -> str:
    wezel = schemat(wezel, komponenty)
    wymagane = set(wezel.get("required", []))
    opisy = []
    for nazwa, cechy in wezel.get("properties", {}).items():
        reszta = {k: v for k, v in cechy.items() if k != "type"}
        opis = f"{nazwa}: {cechy.get('type', '?')}"
        opis += ", wymagane" if nazwa in wymagane else ", opcjonalne"
        if reszta:
            opis += ", " + json_w_wierszu(reszta)
        opisy.append(opis)
    return "; ".join(opisy) or "brak"


def main() -> None:
    parser = argparse.ArgumentParser(description="Opis interfejsu jako tabela operacji.")
    parser.add_argument("--plik", type=Path, default=PLIK_DOMYSLNY, help="plik z opisem interfejsu w JSON")
    argumenty = parser.parse_args()

    opis = czytaj_json(argumenty.plik)
    if "paths" not in opis:
        raise BladNarzedzia(f"plik {wzgledna(argumenty.plik)} nie ma części paths")
    komponenty = opis.get("components", {}).get("schemas", {})

    operacje, odpowiedzi = [], []
    for sciezka, metody in opis["paths"].items():
        for metoda, operacja in metody.items():
            nazwa = f"{metoda.upper()} {sciezka}"
            cialo = operacja.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
            parametry = "; ".join(
                f"{p['name']} ({p['in']}{', wymagany' if p.get('required') else ''})"
                for p in operacja.get("parameters", [])
            )
            operacje.append([nazwa, operacja.get("summary", ""), pola(cialo, komponenty) if cialo else "brak", parametry or "brak"])
            for kod, odpowiedz in operacja.get("responses", {}).items():
                tresc = odpowiedz.get("content", {}).get("application/json", {}).get("schema", {})
                odpowiedzi.append([nazwa, kod, odpowiedz.get("description", ""), pola(tresc, komponenty) if tresc else "brak"])

    info = opis.get("info", {})
    tresc = [
        "## Opis interfejsu",
        f"plik: {wzgledna(argumenty.plik)}",
        f"tytuł: {info.get('title', '')}",
        f"wersja opisu: {info.get('version', '')}",
        f"opis: {info.get('description', '')}",
        "",
        "## Operacje i pola żądania",
        "",
        *tabela(["operacja", "nazwa", "pola żądania", "parametry"], operacje),
        "",
        "## Odpowiedzi",
        "",
        *tabela(["operacja", "kod", "opis", "pola odpowiedzi"], odpowiedzi),
        "",
    ]
    oddaj("opis_interfejsu.py", "opis interfejsu", tresc, "opis-interfejsu.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
