"""Agent „Dwa buildy i karta” (zagadnienia 4, 5, 6).

Graf ma trzy zatrzymania: decyzja o zakresie, decyzja o liczbach, decyzja
o wydaniu. Zdania modelu i decyzje z dwóch pierwszych części zostają w stanie
grafu; przy ostatnim zatrzymaniu człowiek widzi je obok karty. Model w każdym
kroku dostaje tylko wynik skryptów.
"""

from __future__ import annotations

from pathlib import Path

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from .wspolne import KATALOG_ZAPISU, Stan, krok_decyzji, krok_modelu, krok_wejscia, wzgledna, zapisz_protokol

NAZWA = "Dwa buildy i karta"

LISTA_SPRAWDZEN = ("lista_sprawdzen.py",)
WYMAGANIE = ("wymaganie.py", "reset-hasla")
LICZBY = ("liczby.py",)
PORTY = (8765, 8766)
PRZEBIEGI = [("przebieg.py", "--port", port) for port in PORTY]
ZBIOR_WYNIKOW = ("zbierz_wyniki.py", "--porty", *PORTY)

PLIK_PROTOKOLU = "dwa-buildy-i-karta.md"


def zbuduj(model, katalog_zapisu: Path = KATALOG_ZAPISU, opis_modelu: str = ""):
    def zapis(stan: Stan) -> dict:
        protokol = zapisz_protokol(katalog_zapisu / PLIK_PROTOKOLU, NAZWA, opis_modelu, stan)
        return {"zapisane": [wzgledna(protokol)]}

    graf = StateGraph(Stan)
    graf.add_node("wejscie_zakres", krok_wejscia(LISTA_SPRAWDZEN, WYMAGANIE))
    graf.add_node("zakres", krok_modelu(model, "zakres", "zakres-po-zmianie", [LISTA_SPRAWDZEN, WYMAGANIE]))
    graf.add_node("decyzja_zakres", krok_decyzji("decyzja_zakres", ["zakres"]))
    graf.add_node("wejscie_liczby", krok_wejscia(LICZBY))
    graf.add_node("liczby", krok_modelu(model, "liczby", "dwa-buildy-w-liczbach", [LICZBY]))
    graf.add_node("decyzja_liczby", krok_decyzji("decyzja_liczby", ["liczby"]))
    graf.add_node("wejscie_karta", krok_wejscia(*PRZEBIEGI, ZBIOR_WYNIKOW))
    graf.add_node("karta", krok_modelu(model, "karta", "karta-przed-wgraniem", [ZBIOR_WYNIKOW]))
    graf.add_node("decyzja_wydanie", krok_decyzji("decyzja_wydanie", ["karta"], pokaz_wczesniejsze=True))
    graf.add_node("zapis", zapis)

    kolejnosc = [
        "wejscie_zakres", "zakres", "decyzja_zakres",
        "wejscie_liczby", "liczby", "decyzja_liczby",
        "wejscie_karta", "karta", "decyzja_wydanie",
        "zapis",
    ]
    graf.add_edge(START, kolejnosc[0])
    for skad, dokad in zip(kolejnosc, kolejnosc[1:]):
        graf.add_edge(skad, dokad)
    graf.add_edge(kolejnosc[-1], END)
    return graf.compile(checkpointer=InMemorySaver())
