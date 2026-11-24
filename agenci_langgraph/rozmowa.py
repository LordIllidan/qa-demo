"""Przebieg grafu w konsoli: kroki, zatrzymanie na decyzję człowieka i wznowienie."""

from __future__ import annotations

import uuid

from langgraph.types import Command

from .wspolne import BEZ_ODPOWIEDZI, BladAgenta

KRESKA = "=" * 72


def opis_kroku(krok: str, zmiana: dict) -> str:
    if "wejscie" in zmiana:
        return f"[krok {krok}] wejście ze skryptów: " + "; ".join(zmiana["wejscie"])
    if "zdanie_modelu" in zmiana:
        skille = ", ".join(zdanie["skill"] for zdanie in zmiana["zdanie_modelu"].values())
        return f"[krok {krok}] model powiedział swoje zdanie według skilla {skille}"
    if "decyzja_czlowieka" in zmiana:
        return f"[krok {krok}] decyzja człowieka zapisana w stanie grafu"
    if "zapisane" in zmiana:
        return f"[krok {krok}] zapisano: " + ", ".join(zmiana["zapisane"])
    return f"[krok {krok}]"


def zbierz_decyzje(zatrzymanie: dict, pytaj, pisz) -> dict:
    """Pokazuje zdanie modelu i pyta człowieka o każdą decyzję z listy."""
    pisz("")
    pisz(KRESKA)
    pisz(f"ZATRZYMANIE GRAFU: {zatrzymanie['zatrzymanie']}")
    pisz("Graf czeka na decyzję człowieka i bez niej nie pójdzie dalej.")
    pisz(KRESKA)

    wczesniejsze = zatrzymanie.get("wczesniejsze_decyzje") or {}
    if wczesniejsze:
        pisz("")
        pisz("WCZEŚNIEJSZE DECYZJE CZŁOWIEKA (ze stanu grafu)")
        for krok, odpowiedzi in wczesniejsze.items():
            for pytanie, odpowiedz in odpowiedzi.items():
                pisz(f"- [{krok}] {pytanie}: {odpowiedz or BEZ_ODPOWIEDZI}")

    decyzje = {}
    for pozycja in zatrzymanie["pozycje"]:
        pisz("")
        if pozycja["zdanie_modelu"] is not None:
            pisz(f"ZDANIE MODELU (krok {pozycja['krok']}, skill {pozycja['skill']})")
            pisz("")
            pisz(pozycja["zdanie_modelu"])
            pisz("")
        pisz(f"DECYZJA CZŁOWIEKA (krok {pozycja['krok']}); sam Enter zostawia pozycję bez odpowiedzi")
        odpowiedzi = {}
        for pytanie in pozycja["pytania"]:
            try:
                odpowiedzi[pytanie] = pytaj(f"  {pytanie}: ").strip()
            except EOFError as blad:
                raise BladAgenta("nie ma odpowiedzi człowieka; graf zostaje zatrzymany i niczego nie zapisał") from blad
        decyzje[pozycja["krok"]] = odpowiedzi
    pisz("")
    return decyzje


def przeprowadz(graf, pytaj=input, pisz=print, watek: str | None = None) -> dict:
    """Prowadzi graf od początku do końca. Zwraca stan końcowy."""
    konfiguracja = {"configurable": {"thread_id": watek or uuid.uuid4().hex}}
    polecenie = {}
    while True:
        zatrzymanie = None
        for porcja in graf.stream(polecenie, konfiguracja, stream_mode="updates"):
            for krok, zmiana in porcja.items():
                if krok == "__interrupt__":
                    zatrzymanie = zmiana[0].value
                else:
                    pisz(opis_kroku(krok, zmiana or {}))
        if zatrzymanie is None:
            return graf.get_state(konfiguracja).values
        polecenie = Command(resume=zbierz_decyzje(zatrzymanie, pytaj, pisz))
