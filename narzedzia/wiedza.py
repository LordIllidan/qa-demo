"""Wyszukuje w bazie wiedzy o produkcie fragmenty do pytania testera.

Użycie:  python narzedzia/wiedza.py "Czy po resecie hasła klient zostaje zalogowany?"
         python narzedzia/wiedza.py "<pytanie>" --ile 3 --katalog material/wiedza

Skrypt dzieli dokumenty Markdown na fragmenty po nagłówkach drugiego
poziomu i wypisuje najlepiej pasujące fragmenty dosłownie, każdy ze
źródłem. Nie odpowiada na pytanie i nie ocenia, czy fragment je rozstrzyga.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from wspolne import MATERIAL, BladNarzedzia, oddaj, uruchom_narzedzie, wzgledna
from wyszukiwanie import OPIS_METODY, fragmenty_markdown, sprawdz_katalog, szukaj

KATALOG_DOMYSLNY = MATERIAL / "wiedza"
ILE_DOMYSLNIE = 5


def main() -> None:
    parser = argparse.ArgumentParser(description="Fragmenty bazy wiedzy o produkcie do pytania testera.")
    parser.add_argument("pytanie", help="pytanie testera")
    parser.add_argument("--ile", type=int, default=ILE_DOMYSLNIE, help="najwyżej tyle fragmentów")
    parser.add_argument("--katalog", type=Path, default=KATALOG_DOMYSLNY, help="katalog z dokumentami .md")
    argumenty = parser.parse_args()

    katalog = sprawdz_katalog(argumenty.katalog)
    pliki = sorted(katalog.glob("*.md")) if katalog.is_dir() else []
    if not pliki:
        raise BladNarzedzia(f"w katalogu {wzgledna(katalog)} nie ma dokumentów .md")
    fragmenty = [f for plik in pliki for f in fragmenty_markdown(plik)]
    trafienia = szukaj(argumenty.pytanie, fragmenty, argumenty.ile)

    tresc = [
        "## Pytanie testera",
        argumenty.pytanie,
        "",
        "## Baza wiedzy",
        f"katalog: {wzgledna(katalog)}",
        f"dokumenty: {', '.join(wzgledna(p) for p in pliki)}",
        f"liczba fragmentów: {len(fragmenty)}",
        f"sposób wyszukiwania: {OPIS_METODY}",
        "",
        f"## Fragmenty (najwyżej {argumenty.ile}, od najwyższego wyniku)",
        "",
    ]
    if not trafienia:
        tresc += ["Żaden fragment nie ma wspólnych słów z pytaniem.", ""]
    for numer, (wynik, wspolne, fragment) in enumerate(trafienia, start=1):
        tresc += [
            f"### Fragment {numer}",
            f"źródło: {fragment.zrodlo}, sekcja „{fragment.sekcja}”",
            f"opis dokumentu: {'; '.join(fragment.opis_dokumentu) or 'brak'}",
            f"wynik wyszukiwania: {wynik}",
            f"wspólne rdzenie słów: {', '.join(wspolne)}",
            "",
            fragment.tekst,
            "",
        ]
    oddaj("wiedza.py", "fragmenty bazy wiedzy", tresc, "wiedza.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
