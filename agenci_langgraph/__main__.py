"""Uruchamianie agentów LangGraph z konsoli.

Użycie:  python -m agenci_langgraph zestaw
         python -m agenci_langgraph zgloszenie
         python -m agenci_langgraph karta
"""

from __future__ import annotations

import argparse
import sys

from . import dwa_buildy_i_karta, od_przebiegu_do_zgloszenia, od_wymagania_do_zestawu
from .model import model_ze_srodowiska, opis_modelu
from .rozmowa import przeprowadz
from .wspolne import KATALOG_ZAPISU, BladAgenta


def main(argumenty_konsoli: list | None = None, pytaj=input, pisz=print, model=None,
         katalog_zapisu=KATALOG_ZAPISU) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m agenci_langgraph",
        description="Agenty LangGraph dla testerów: model mówi swoje zdanie, decyzję podejmuje człowiek.",
    )
    agenci = parser.add_subparsers(dest="agent", required=True, metavar="agent")
    agenci.add_parser("zestaw", help=od_wymagania_do_zestawu.NAZWA)
    zgloszenie = agenci.add_parser("zgloszenie", help=od_przebiegu_do_zgloszenia.NAZWA)
    zgloszenie.add_argument("--port", type=int, default=od_przebiegu_do_zgloszenia.PORT,
                            help="port builda, z którego przebiegu ma powstać szkic zgłoszenia")
    zgloszenie.add_argument("--port-odniesienia", type=int, default=od_przebiegu_do_zgloszenia.PORT_ODNIESIENIA,
                            help="port builda do porównania")
    agenci.add_parser("karta", help=dwa_buildy_i_karta.NAZWA)
    argumenty = parser.parse_args(argumenty_konsoli)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
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
        else:
            graf = dwa_buildy_i_karta.zbuduj(model, katalog_zapisu, opis)
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
