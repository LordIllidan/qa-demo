"""Pomocnicze części testów: prowadzenie grafu i odpowiedzi człowieka."""

from __future__ import annotations


class Przebieg:
    """Prowadzi graf krok po kroku: do zatrzymania, a po decyzji dalej."""

    def __init__(self, graf) -> None:
        self.graf = graf
        self.konfiguracja = {"configurable": {"thread_id": "test"}}

    def do_zatrzymania(self, polecenie) -> dict | None:
        wynik = self.graf.invoke(polecenie, self.konfiguracja)
        przerwania = wynik.get("__interrupt__")
        return przerwania[0].value if przerwania else None

    @property
    def stan(self) -> dict:
        return self.graf.get_state(self.konfiguracja).values

    @property
    def nastepny_krok(self) -> tuple:
        return self.graf.get_state(self.konfiguracja).next


def bez_odpowiedzi(zatrzymanie: dict) -> dict:
    """Decyzja, w której człowiek zostawił wszystkie pozycje puste."""
    return {pozycja["krok"]: {pytanie: "" for pytanie in pozycja["pytania"]} for pozycja in zatrzymanie["pozycje"]}
