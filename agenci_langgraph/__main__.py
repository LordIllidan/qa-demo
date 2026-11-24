"""Uruchamianie agentów LangGraph z konsoli.

Użycie:  python -m agenci_langgraph lista
         python -m agenci_langgraph zestaw
         python -m agenci_langgraph zgloszenie
         python -m agenci_langgraph karta
         python -m agenci_langgraph <nazwa zagadnienia>   (lista podaje nazwy)
"""

from __future__ import annotations

import argparse
import sys

from . import dwa_buildy_i_karta, jedno_zagadnienie, od_przebiegu_do_zgloszenia, od_wymagania_do_zestawu
from .model import model_ze_srodowiska, opis_modelu
from .rozmowa import przeprowadz
from .wspolne import KATALOG_ZAPISU, BladAgenta

AGENCI_Z_WLASNYM_GRAFEM = [
    ("zestaw", od_wymagania_do_zestawu.NAZWA, "1, 7, 8, P4", False),
    ("zgloszenie", od_przebiegu_do_zgloszenia.NAZWA, "2, P1", True),
    ("karta", dwa_buildy_i_karta.NAZWA, "4, 5, 6", True),
]


def lista_agentow() -> list:
    """Wiersze listy: polecenie, agent, zagadnienia i to, czego agent potrzebuje poza modelem."""
    wiersze = ["Agenty LangGraph. Uruchomienie: python -m agenci_langgraph <polecenie>", ""]
    pozycje = [(polecenie, f"{nazwa}: zagadnienia {numery}", aplikacja, ())
               for polecenie, nazwa, numery, aplikacja in AGENCI_Z_WLASNYM_GRAFEM]
    pozycje += [(polecenie, f"{jedno_zagadnienie.NAZWA}: zagadnienie {z.numer}. {z.tytul}", z.aplikacja, z.pliki)
                for polecenie, z in jedno_zagadnienie.ZAGADNIENIA.items()]
    szerokosc = max(len(polecenie) for polecenie, *_ in pozycje)
    for polecenie, opis, aplikacja, pliki in pozycje:
        wiersze.append(f"{polecenie.ljust(szerokosc)}  {opis}")
        if aplikacja:
            wiersze.append(f"{'':{szerokosc}}  potrzebuje aplikacji: python app/serwer.py w drugim oknie")
        if pliki:
            wiersze.append(f"{'':{szerokosc}}  pliki wymienione w skillu (--plik): {', '.join(pliki)}")
    wiersze += ["", "Opcje polecenia: python -m agenci_langgraph <polecenie> --help"]
    return wiersze


def main(argumenty_konsoli: list | None = None, pytaj=input, pisz=print, model=None,
         katalog_zapisu=KATALOG_ZAPISU) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m agenci_langgraph",
        description="Agenty LangGraph dla testerów: model mówi swoje zdanie, decyzję podejmuje człowiek.",
    )
    agenci = parser.add_subparsers(dest="agent", required=True, metavar="agent")
    agenci.add_parser("lista", help="lista agentów i zagadnień, które obsługują")
    agenci.add_parser("zestaw", help=od_wymagania_do_zestawu.NAZWA)
    zgloszenie = agenci.add_parser("zgloszenie", help=od_przebiegu_do_zgloszenia.NAZWA)
    zgloszenie.add_argument("--port", type=int, default=od_przebiegu_do_zgloszenia.PORT,
                            help="port builda, z którego przebiegu ma powstać szkic zgłoszenia")
    zgloszenie.add_argument("--port-odniesienia", type=int, default=od_przebiegu_do_zgloszenia.PORT_ODNIESIENIA,
                            help="port builda do porównania")
    agenci.add_parser("karta", help=dwa_buildy_i_karta.NAZWA)
    for nazwa, zagadnienie in jedno_zagadnienie.ZAGADNIENIA.items():
        jedno_zagadnienie.dodaj_opcje(
            agenci.add_parser(nazwa, help=f"{zagadnienie.numer}. {zagadnienie.tytul}"), zagadnienie)
    argumenty = parser.parse_args(argumenty_konsoli)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if argumenty.agent == "lista":
        for wiersz in lista_agentow():
            pisz(wiersz)
        return 0
    try:
        if model is None:
            model, opis = model_ze_srodowiska(), opis_modelu()
        else:
            opis = type(model).__name__
        if argumenty.agent == "zestaw":
            graf = od_wymagania_do_zestawu.zbuduj(model, katalog_zapisu, opis)
        elif argumenty.agent == "zgloszenie":
            graf = od_przebiegu_do_zgloszenia.zbuduj(model, argumenty.port, argumenty.port_odniesienia,
                                                     katalog_zapisu, opis)
        elif argumenty.agent == "karta":
            graf = dwa_buildy_i_karta.zbuduj(model, katalog_zapisu, opis)
        else:
            zagadnienie = jedno_zagadnienie.ZAGADNIENIA[argumenty.agent]
            graf = jedno_zagadnienie.zbuduj(model, argumenty.agent, zagadnienie.polecenia(argumenty),
                                            argumenty.prosba, tuple(argumenty.plik), katalog_zapisu, opis)
        przeprowadz(graf, pytaj, pisz)
    except BladAgenta as blad:
        pisz(f"Agent zatrzymany: {blad}")
        return 2
    except KeyboardInterrupt:
        pisz("")
        pisz("Przerwano. Graf nie doszedł do zapisu.")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
