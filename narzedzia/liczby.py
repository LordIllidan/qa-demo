"""Podaje liczby dwóch buildów z gotowych plików wyników.

Użycie:  python narzedzia/liczby.py
         python narzedzia/liczby.py --pliki material/liczby/build-8765.json material/liczby/build-8766.json

Skrypt niczego nie mierzy i niczego nie porównuje. Czyta dwa pliki i zestawia
ich zawartość obok siebie.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from wspolne import MATERIAL, BladNarzedzia, czytaj_json, oddaj, opisz_build, tabela, uruchom_narzedzie, wzgledna

PLIKI_DOMYSLNE = [MATERIAL / "liczby" / "build-8765.json", MATERIAL / "liczby" / "build-8766.json"]

NAZWY_PROFILU = {
    "uzytkownicy": "liczba użytkowników",
    "narastanie_s": "narastanie [s]",
    "czas_trwania_s": "czas trwania [s]",
    "przerwa_miedzy_zadaniami_s": "przerwa między żądaniami [s]",
}
NAZWY_PROGOW = {
    "p95_ms_ponizej": "próg: p95 poniżej [ms]",
    "bledy_proc_ponizej": "próg: błędy poniżej [%]",
}
NAZWY_METRYK = {
    "liczba_zadan": "liczba żądań",
    "mediana_ms": "mediana [ms]",
    "srednia_ms": "średnia [ms]",
    "p95_ms": "p95 [ms]",
    "max_ms": "maksimum [ms]",
    "bledy_proc": "błędy [%]",
}


def klucze(slowniki: list) -> list:
    wynik = []
    for slownik in slowniki:
        for klucz in slownik:
            if klucz not in wynik:
                wynik.append(klucz)
    return wynik


def zestaw(slowniki: list, nazwy: dict) -> list:
    return [[nazwy.get(k, k)] + [s.get(k, "brak") for s in slowniki] for k in klucze(slowniki)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Podaje liczby dwóch buildów z gotowych plików.")
    parser.add_argument("--pliki", type=Path, nargs=2, default=PLIKI_DOMYSLNE,
                        help="dwa pliki z liczbami, w kolejności: wcześniejszy build, późniejszy build")
    argumenty = parser.parse_args()

    zbiory = [czytaj_json(plik) for plik in argumenty.pliki]
    for plik, zbior in zip(argumenty.pliki, zbiory):
        if not {"build", "profil", "progi", "sciezki"} <= set(zbior):
            raise BladNarzedzia(f"plik {wzgledna(plik)} nie ma pól build, profil, progi i sciezki")
    kolumny = [f"build {opisz_build(z['build'])}" for z in zbiory]

    tresc = ["## Pliki z liczbami", ""]
    for plik, zbior in zip(argumenty.pliki, zbiory):
        tresc.append(f"- build {opisz_build(zbior['build'])}: {wzgledna(plik)}; pochodzenie: {zbior.get('pochodzenie', 'brak')}")
    tresc += ["", "## Profil obciążenia", ""]
    tresc += tabela(["parametr"] + kolumny, zestaw([z["profil"] for z in zbiory], NAZWY_PROFILU))

    for sciezka in klucze([z["sciezki"] for z in zbiory]):
        tresc += ["", f"## Ścieżka {sciezka}", ""]
        progi = zestaw([z["progi"].get(sciezka, {}) for z in zbiory], NAZWY_PROGOW)
        metryki = zestaw([z["sciezki"].get(sciezka, {}) for z in zbiory], NAZWY_METRYK)
        tresc += tabela(["pozycja"] + kolumny, progi + metryki)
    tresc.append("")

    oddaj("liczby.py", "liczby", tresc, "liczby.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
