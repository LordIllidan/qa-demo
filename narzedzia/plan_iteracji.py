"""Podaje dane iteracji, historie, listę ryzyk i otwarte zgłoszenia.

Użycie:  python narzedzia/plan_iteracji.py

Skrypt nie szacuje pracy, nie przypisuje zadań i nie ustala zakresu.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from wspolne import KATALOG, MATERIAL, czytaj_json, czytaj_tekst, oddaj, tabela, uruchom_narzedzie, wzgledna

PLIK_DOMYSLNY = MATERIAL / "plan" / "iteracja.json"
RYZYKA = MATERIAL / "sesja" / "ryzyka.md"
ZGLOSZENIA = MATERIAL / "zgloszenia" / "otwarte.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Dane iteracji, ryzyka i otwarte zgłoszenia.")
    parser.add_argument("--plik", type=Path, default=PLIK_DOMYSLNY, help="plik z danymi iteracji")
    argumenty = parser.parse_args()

    iteracja = czytaj_json(argumenty.plik)
    zgloszenia = czytaj_json(ZGLOSZENIA)

    tresc = [
        "## Iteracja",
        f"plik: {wzgledna(argumenty.plik)}",
        f"nazwa: {iteracja['iteracja']}",
        f"od: {iteracja['od']}",
        f"do: {iteracja['do']}",
        f"wydanie: {iteracja['wydanie']}",
        "",
        "## Historie",
        "",
        *tabela(["id", "tytuł", "plik", "uwagi"], [[h["id"], h["tytul"], h["plik"], h["uwagi"]] for h in iteracja["historie"]]),
        "",
        "## Zespół",
        "",
        *tabela(["osoba", "rola", "godziny na testy w iteracji"],
                [[z["osoba"], z["rola"], z["godziny_na_testy"]] for z in iteracja["zespol"]]),
        "",
        "## Środowisko",
        "",
        *[f"- {wpis}" for wpis in iteracja["srodowisko"]],
        "",
        "## Ustalenia zespołu",
        "",
        *[f"- {wpis}" for wpis in iteracja["ustalenia_zespolu"]],
        "",
        "## Lista ryzyk",
        f"plik: {wzgledna(RYZYKA)}",
        "",
        czytaj_tekst(RYZYKA).rstrip("\n"),
        "",
        "## Otwarte zgłoszenia",
        f"plik: {wzgledna(ZGLOSZENIA)}, stan na {zgloszenia['stan_na']}",
        "",
        *tabela(["id", "tytuł", "build", "dotkliwość", "priorytet"],
                [[z["id"], z["tytul"], z["build"], z["dotkliwosc"], z["priorytet"]] for z in zgloszenia["zgloszenia"]]),
        "",
        "## Treść historii",
        "",
    ]
    for historia in iteracja["historie"]:
        tresc += [f"### {historia['id']}", f"plik: {historia['plik']}", "", czytaj_tekst(KATALOG / historia["plik"]).rstrip("\n"), ""]
    oddaj("plan_iteracji.py", "dane iteracji", tresc, "plan-iteracji.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
