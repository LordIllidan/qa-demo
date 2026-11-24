"""Wyszukuje zgłoszenia podobne do opisu, który tester chce zgłosić.

Użycie:  python narzedzia/podobne_zgloszenia.py "Link resetu ustawia hasło drugi raz"
         python narzedzia/podobne_zgloszenia.py "<opis>" --ile 3

Przeszukuje otwarte zgłoszenia (material/zgloszenia/otwarte.json, razem
z treścią pliku zgłoszenia, gdy lista go podaje) i archiwum zgłoszeń
zamkniętych, odrzuconych i duplikatów (material/zgloszenia/archiwum.json).
Nie rozstrzyga, czy opis jest powtórzeniem, regresją albo nowym defektem.
"""

from __future__ import annotations

import argparse

from wspolne import KATALOG, MATERIAL, czytaj_json, czytaj_tekst, oddaj, tabela, uruchom_narzedzie, wzgledna
from wyszukiwanie import OPIS_METODY, Fragment, szukaj

OTWARTE = MATERIAL / "zgloszenia" / "otwarte.json"
ARCHIWUM = MATERIAL / "zgloszenia" / "archiwum.json"
ILE_DOMYSLNIE = 5


def zgloszenia() -> list:
    """Każde zgłoszenie jako jeden fragment: tytuł w sekcji, opis w treści."""
    wynik = []
    for z in czytaj_json(OTWARTE)["zgloszenia"]:
        zrodlo = wzgledna(OTWARTE)
        if z.get("plik"):
            zrodlo += f" i {z['plik']}"
            opis = czytaj_tekst(KATALOG / z["plik"]).strip()
        else:
            opis = "lista otwartych zgłoszeń podaje tylko tytuł"
        dane = [f"stan: {z['stan']}", f"build: {z['build']}", f"dotkliwość: {z['dotkliwosc']}", f"priorytet: {z['priorytet']}"]
        wynik.append(Fragment(zrodlo, f"{z['id']}: {z['tytul']}", opis, dane))
    for z in czytaj_json(ARCHIWUM)["zgloszenia"]:
        dane = [f"stan: {z['stan']}", f"build: {z['build']}", f"obszar: {z['obszar']}", f"rozwiązanie: {z['rozwiazanie']}"]
        wynik.append(Fragment(wzgledna(ARCHIWUM), f"{z['id']}: {z['tytul']}", z["opis"], dane))
    return wynik


def main() -> None:
    parser = argparse.ArgumentParser(description="Zgłoszenia podobne do opisu testera.")
    parser.add_argument("opis", help="opis zachowania, które tester chce zgłosić")
    parser.add_argument("--ile", type=int, default=ILE_DOMYSLNIE, help="najwyżej tyle zgłoszeń")
    argumenty = parser.parse_args()

    wszystkie = zgloszenia()
    trafienia = szukaj(argumenty.opis, wszystkie, argumenty.ile)
    otwartych = len(czytaj_json(OTWARTE)["zgloszenia"])

    tresc = [
        "## Opis testera",
        argumenty.opis,
        "",
        "## Przeszukane zgłoszenia",
        f"otwarte: {otwartych} ({wzgledna(OTWARTE)})",
        f"archiwum: {len(wszystkie) - otwartych} ({wzgledna(ARCHIWUM)})",
        f"sposób wyszukiwania: {OPIS_METODY}",
        "",
        f"## Zgłoszenia z najwyższym wynikiem (najwyżej {argumenty.ile})",
        "",
    ]
    if not trafienia:
        tresc += ["Żadne zgłoszenie nie ma wspólnych słów z opisem.", ""]
    else:
        tresc += [*tabela(["zgłoszenie", "dane", "wynik wyszukiwania", "wspólne rdzenie słów"],
                          [[f.sekcja, "; ".join(f.opis_dokumentu), wynik, ", ".join(wspolne)]
                           for wynik, wspolne, f in trafienia]), ""]
    for wynik, wspolne, fragment in trafienia:
        tresc += [
            f"### {fragment.sekcja}",
            f"źródło: {fragment.zrodlo}",
            *fragment.opis_dokumentu,
            "",
            fragment.tekst,
            "",
        ]
    oddaj("podobne_zgloszenia.py", "podobne zgłoszenia", tresc, "podobne-zgloszenia.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
