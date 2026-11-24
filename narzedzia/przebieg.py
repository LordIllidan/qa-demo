"""Uruchamia testy na buildzie pod wskazanym portem i podaje wynik przebiegu.

Użycie:  python narzedzia/przebieg.py --port 8766
         python narzedzia/przebieg.py --port 8767 --test test_link_dziala_jeden_raz

Czerwony wynik testu nie jest błędem narzędzia: skrypt kończy się kodem 0,
gdy wynik został zapisany.
"""

from __future__ import annotations

import argparse

from wspolne import WYNIKI, ZESTAW_DOMYSLNY, oddaj, opisz_przebieg, uruchom_narzedzie, uruchom_testy, zapisz_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Uruchamia testy na wskazanym porcie i podaje wynik.")
    parser.add_argument("--port", type=int, required=True, help="port builda, na przykład 8765 albo 8766")
    parser.add_argument("--zestaw", default=ZESTAW_DOMYSLNY,
                        help=f"plik albo katalog z testami (domyślnie {ZESTAW_DOMYSLNY})")
    parser.add_argument("--test", action="append", default=[],
                        help="nazwa testu z zestawu; opcję można powtórzyć")
    argumenty = parser.parse_args()

    przebieg = uruchom_testy(argumenty.port, argumenty.zestaw, argumenty.test)
    plik_json = WYNIKI / f"przebieg-{argumenty.port}.json"
    zapisz_json(plik_json, przebieg)
    oddaj("przebieg.py", "wynik przebiegu", opisz_przebieg(przebieg),
          f"przebieg-{argumenty.port}.txt", [plik_json])


if __name__ == "__main__":
    uruchom_narzedzie(main)
