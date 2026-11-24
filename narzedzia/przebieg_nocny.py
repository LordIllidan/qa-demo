"""Podaje zapisany nocny przebieg: wynik, przebieg referencyjny i log.

Użycie:  python narzedzia/przebieg_nocny.py

Skrypt niczego nie uruchamia. Czyta trzy pliki z material/przebieg-nocny.
"""

from __future__ import annotations

from wspolne import MATERIAL, czytaj_json, czytaj_tekst, oddaj, opisz_przebieg, uruchom_narzedzie, wzgledna

KATALOG_NOCNY = MATERIAL / "przebieg-nocny"
WYNIK = KATALOG_NOCNY / "wynik-8766.json"
REFERENCYJNY = KATALOG_NOCNY / "wynik-8765.json"
LOG = KATALOG_NOCNY / "log-8766.txt"


def main() -> None:
    tresc = [
        "## Pliki",
        f"- wynik nocnego przebiegu: {wzgledna(WYNIK)}",
        f"- przebieg referencyjny: {wzgledna(REFERENCYJNY)}",
        f"- log nocnego przebiegu: {wzgledna(LOG)}",
        "",
        *opisz_przebieg(czytaj_json(WYNIK), "Nocny przebieg"),
        *opisz_przebieg(czytaj_json(REFERENCYJNY), "Przebieg referencyjny"),
        "## Log nocnego przebiegu",
        "",
        "```text",
        czytaj_tekst(LOG).rstrip("\n"),
        "```",
        "",
    ]
    oddaj("przebieg_nocny.py", "wynik przebiegu", tresc, "przebieg-nocny.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
