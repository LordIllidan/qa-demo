"""Zbiera w jeden plik wyniki przebiegów, liczby, otwarte zgłoszenia i zakres.

Użycie:  python narzedzia/zbierz_wyniki.py

Skrypt niczego nie uruchamia i niczego nie podsumowuje. Wyniki przebiegów
bierze z plików wyniki/przebieg-<port>.json, które zapisuje przebieg.py.
"""

from __future__ import annotations

import argparse

from wspolne import (
    MATERIAL,
    WYNIKI,
    czytaj_json,
    oddaj,
    opisz_build,
    opisz_test,
    tabela,
    uruchom_narzedzie,
    wzgledna,
    zapisz_json,
)

PORTY_DOMYSLNE = [8765, 8766]
PLIKI_LICZB = [MATERIAL / "liczby" / "build-8765.json", MATERIAL / "liczby" / "build-8766.json"]
PLIK_ZGLOSZEN = MATERIAL / "zgloszenia" / "otwarte.json"
PLIK_ZAKRESU = MATERIAL / "zakres" / "zakres-wydania.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Zbiera wyniki w jeden plik.")
    parser.add_argument("--porty", type=int, nargs="+", default=PORTY_DOMYSLNE,
                        help="porty buildów, których zapisane przebiegi mają trafić do zbioru")
    argumenty = parser.parse_args()

    tresc = ["## Wyniki przebiegów testów", ""]
    przebiegi = []
    for port in argumenty.porty:
        plik = WYNIKI / f"przebieg-{port}.json"
        if not plik.is_file():
            przebiegi.append({"port": port, "plik": wzgledna(plik), "przebieg": None})
            tresc += [
                f"### Port {port}",
                f"brak pliku {wzgledna(plik)}; przebieg na tym porcie nie został zapisany",
                f"(zapisuje go polecenie: python narzedzia/przebieg.py --port {port})",
                "",
            ]
            continue
        przebieg = czytaj_json(plik)
        przebiegi.append({"port": port, "plik": wzgledna(plik), "przebieg": przebieg})
        liczby = przebieg["podsumowanie"]
        tresc += [
            f"### Build {opisz_build(przebieg['build'])}",
            f"plik: {wzgledna(plik)}",
            f"zestaw: {przebieg['zestaw']}",
            f"start: {przebieg['start']}",
            (
                f"liczba testów: {liczby['liczba_testow']}; zaliczone: {liczby['zaliczony']}; "
                f"niezaliczone: {liczby['niezaliczony']}; pominięte: {liczby['pominięty']}; "
                f"błędy: {liczby['błąd']}"
            ),
            "",
            *tabela(["test", "opis", "wynik"], [[t["nazwa"], t["opis"] or "brak", t["wynik"]] for t in przebieg["testy"]]),
            "",
        ]
        for test in przebieg["testy"]:
            if test["wynik"] != "zaliczony":
                tresc += opisz_test(test, poziom="####")

    liczby_buildow = [czytaj_json(plik) for plik in PLIKI_LICZB]
    tresc += ["## Liczby z gotowych plików wyników", ""]
    for plik, zbior in zip(PLIKI_LICZB, liczby_buildow):
        profil = zbior["profil"]
        tresc += [
            f"### Build {opisz_build(zbior['build'])}",
            f"plik: {wzgledna(plik)}",
            (
                f"profil: {profil['uzytkownicy']} użytkowników, narastanie {profil['narastanie_s']} s, "
                f"czas trwania {profil['czas_trwania_s']} s, przerwa między żądaniami "
                f"{profil['przerwa_miedzy_zadaniami_s']} s"
            ),
            "",
        ]
        wiersze = []
        for sciezka, metryki in zbior["sciezki"].items():
            progi = zbior["progi"].get(sciezka, {})
            wiersze.append([
                sciezka, metryki["liczba_zadan"], metryki["mediana_ms"], metryki["srednia_ms"],
                metryki["p95_ms"], progi.get("p95_ms_ponizej", "brak"), metryki["max_ms"],
                metryki["bledy_proc"], progi.get("bledy_proc_ponizej", "brak"),
            ])
        tresc += tabela(
            ["ścieżka", "liczba żądań", "mediana [ms]", "średnia [ms]", "p95 [ms]", "próg: p95 poniżej [ms]",
             "maksimum [ms]", "błędy [%]", "próg: błędy poniżej [%]"],
            wiersze,
        ) + [""]

    zgloszenia = czytaj_json(PLIK_ZGLOSZEN)
    tresc += [
        "## Otwarte zgłoszenia",
        f"plik: {wzgledna(PLIK_ZGLOSZEN)}; stan na: {zgloszenia['stan_na']}",
        "",
        *tabela(
            ["id", "tytuł", "build", "stan", "dotkliwość", "priorytet"],
            [[z["id"], z["tytul"], z["build"], z["stan"], z["dotkliwosc"], z["priorytet"]]
             for z in zgloszenia["zgloszenia"]],
        ),
        "",
    ]

    zakres = czytaj_json(PLIK_ZAKRESU)
    tresc += [
        "## Zakres planowany i wykonany",
        f"plik: {wzgledna(PLIK_ZAKRESU)}; wydanie: {zakres['wydanie']}",
        "",
        *tabela(["id", "pozycja planu", "stan", "uwagi"],
                [[p["id"], p["pozycja"], p["stan"], p["uwagi"]] for p in zakres["pozycje"]]),
        "",
    ]

    plik_json = WYNIKI / "zbior-wynikow.json"
    zapisz_json(plik_json, {
        "format": "qa-demo/zbior-wynikow/1",
        "przebiegi": przebiegi,
        "liczby": liczby_buildow,
        "zgloszenia": zgloszenia,
        "zakres": zakres,
    })
    oddaj("zbierz_wyniki.py", "wynik przebiegu i liczby", tresc, "zbior-wynikow.txt", [plik_json])


if __name__ == "__main__":
    uruchom_narzedzie(main)
