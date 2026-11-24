"""Agent „Od czerwonego przebiegu do zgłoszenia” (zagadnienia P1 i 2).

Graf ma dwa zatrzymania. Po pierwszym człowiek klasyfikuje grupy awarii
i decyduje, czy graf ma przygotować szkic zgłoszenia. Bez słowa „tak” graf
nie uruchamia przebiegów i nie prosi modelu o szkic. Po drugim człowiek
decyduje o samym zgłoszeniu. Graf niczego nie wysyła.
"""

from __future__ import annotations

from pathlib import Path

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from .wspolne import KATALOG_ZAPISU, Stan, krok_decyzji, krok_modelu, krok_wejscia, wzgledna, zapisz_protokol

NAZWA = "Od czerwonego przebiegu do zgłoszenia"

PRZEBIEG_NOCNY = ("przebieg_nocny.py",)
WYMAGANIE = ("wymaganie.py", "reset-hasla")
PORT = 8766
PORT_ODNIESIENIA = 8765

KROK_DECYZJI_O_SZKICU = "decyzja_klasyfikacja"
PLIK_PROTOKOLU = "od-przebiegu-do-zgloszenia.md"


def pytanie_o_szkic(port: int, port_odniesienia: int) -> str:
    return (
        f"Czy graf ma uruchomić testy na buildach pod portami {port} i {port_odniesienia} "
        "i poprosić model o szkic zgłoszenia (tak albo nie)"
    )


def zbuduj(model, port: int = PORT, port_odniesienia: int = PORT_ODNIESIENIA,
           katalog_zapisu: Path = KATALOG_ZAPISU, opis_modelu: str = ""):
    przebieg = ("przebieg.py", "--port", port)
    przebieg_odniesienia = ("przebieg.py", "--port", port_odniesienia)
    pytanie = pytanie_o_szkic(port, port_odniesienia)

    def po_decyzji(stan: Stan) -> str:
        odpowiedz = stan["decyzja_czlowieka"][KROK_DECYZJI_O_SZKICU][pytanie]
        return "szkic" if odpowiedz.lower().startswith("tak") else "bez_szkicu"

    def zapis(stan: Stan) -> dict:
        protokol = zapisz_protokol(katalog_zapisu / PLIK_PROTOKOLU, NAZWA, opis_modelu, stan)
        return {"zapisane": [wzgledna(protokol)]}

    graf = StateGraph(Stan)
    graf.add_node("wejscie_nocne", krok_wejscia(PRZEBIEG_NOCNY))
    graf.add_node("klasyfikacja", krok_modelu(model, "klasyfikacja", "klasyfikacja-awarii", [PRZEBIEG_NOCNY]))
    graf.add_node(KROK_DECYZJI_O_SZKICU,
                  krok_decyzji(KROK_DECYZJI_O_SZKICU, ["klasyfikacja"], pytania_grafu=(pytanie,)))
    graf.add_node("wejscie_przebiegi", krok_wejscia(przebieg, przebieg_odniesienia, WYMAGANIE))
    graf.add_node("szkic", krok_modelu(model, "szkic", "zgloszenie-defektu",
                                       [przebieg, przebieg_odniesienia, WYMAGANIE]))
    graf.add_node("decyzja_zgloszenie", krok_decyzji("decyzja_zgloszenie", ["szkic"]))
    graf.add_node("zapis", zapis)

    graf.add_edge(START, "wejscie_nocne")
    graf.add_edge("wejscie_nocne", "klasyfikacja")
    graf.add_edge("klasyfikacja", KROK_DECYZJI_O_SZKICU)
    graf.add_conditional_edges(KROK_DECYZJI_O_SZKICU, po_decyzji,
                               {"szkic": "wejscie_przebiegi", "bez_szkicu": "zapis"})
    graf.add_edge("wejscie_przebiegi", "szkic")
    graf.add_edge("szkic", "decyzja_zgloszenie")
    graf.add_edge("decyzja_zgloszenie", "zapis")
    graf.add_edge("zapis", END)
    return graf.compile(checkpointer=InMemorySaver())
