"""Agent „Od wymagania do potwierdzonego zestawu” (zagadnienia 1, 7, 8, P4).

Graf: wejście ze skryptów, pięć kroków modelu, jedno zatrzymanie na decyzję
człowieka, zapis. Do zapisu trafiają wyłącznie pozycje, których numery
człowiek wpisał przy zatrzymaniu. Graf wybiera je po numerze i nie ocenia treści.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from .wspolne import (
    BEZ_ODPOWIEDZI,
    KATALOG_ZAPISU,
    Stan,
    krok_decyzji,
    krok_modelu,
    krok_wejscia,
    teraz,
    wzgledna,
    zapisz_protokol,
)

NAZWA = "Od wymagania do potwierdzonego zestawu"

WYMAGANIE = ("wymaganie.py", "reset-hasla")
DRUGA_HISTORYJKA = ("wymaganie.py", "filtr-zamowien")
LISTA_TESTOW = ("lista_testow.py",)

ZADANIE_DANE = (
    "Tester nie wskazał jednej reguły. Ułóż dane pod reguły wymagania, "
    "które dotyczą operacji z formatu pliku dla przebiegu."
)

KROKI_MODELU = ["luki", "uprawnienia_reset", "uprawnienia_filtr", "pokrycie", "dane"]
KROK_DANYCH = "dane"

PLIK_PROTOKOLU = "od-wymagania-do-zestawu.md"
PLIK_ZESTAWU = "zestaw-potwierdzony.md"
PLIK_DANYCH = "dane-potwierdzone.json"


def numery(odpowiedz: str) -> list:
    """Numery pozycji wpisane przez człowieka, na przykład M1 albo D3."""
    znalezione = []
    for numer in re.findall(r"(?<!\w)[^\W\d_]{1,4}\d{1,3}(?!\w)", odpowiedz):
        if numer.upper() not in znalezione:
            znalezione.append(numer.upper())
    return znalezione


def wiersze_tabel(tekst: str) -> dict:
    """Wiersze tabel Markdown ze zdania modelu: numer z pierwszej kolumny -> lista (nagłówek, wiersz)."""
    wynik: dict = {}
    naglowek = None
    poprzedni = ""
    for wiersz in (w.strip() for w in tekst.splitlines()):
        if not wiersz.startswith("|"):
            naglowek = None
        elif re.match(r"\|\s*:?-{3,}", wiersz):
            naglowek = poprzedni
        elif naglowek is not None:
            numer = wiersz.strip("|").split("|")[0].strip().upper()
            wynik.setdefault(numer, []).append((naglowek, wiersz))
        poprzedni = wiersz
    return wynik


def dane_dla_przebiegu(tekst: str, wskazane: list) -> tuple:
    """Z bloku JSON w zdaniu modelu zostawia tylko wejścia o wskazanych numerach."""
    blok = re.search(r"```json\s*\n(.*?)```", tekst, flags=re.DOTALL)
    if not blok:
        return None, "w zdaniu modelu nie ma bloku JSON z plikiem dla przebiegu"
    try:
        dane = json.loads(blok.group(1))
    except json.JSONDecodeError as blad:
        return None, f"blok JSON w zdaniu modelu nie jest poprawnym JSON-em ({blad})"
    wejscia = dane.get("wejscia") if isinstance(dane, dict) else None
    if not isinstance(wejscia, list):
        return None, "blok JSON w zdaniu modelu nie ma listy wejscia"
    wybrane = [w for w in wejscia if isinstance(w, dict) and str(w.get("id", "")).upper() in wskazane]
    if not wybrane:
        return None, "żaden wskazany numer nie występuje w bloku JSON ze zdania modelu"
    return {**dane, "wejscia": wybrane}, None


def wskazane_wiersze(tabele: dict, wskazane: list) -> list:
    """Wiersze o wskazanych numerach, przepisane ze zdania modelu razem z nagłówkiem tabeli."""
    wiersze = []
    ostatni_naglowek = None
    for numer in wskazane:
        for naglowek, wiersz in tabele.get(numer, []):
            if naglowek != ostatni_naglowek:
                kolumny = naglowek.strip("|").count("|") + 1
                wiersze += ["", naglowek, "| " + " | ".join(["---"] * kolumny) + " |"]
                ostatni_naglowek = naglowek
            wiersze.append(wiersz)
    nieznane = [numer for numer in wskazane if numer not in tabele]
    if nieznane:
        wiersze += ["", "Numery, których nie ma w tabelach zdania modelu: " + ", ".join(nieznane)]
    return wiersze[1:] + [""] if wiersze else []


def zapisz_zestaw(stan: Stan, katalog_zapisu: Path, protokol: str) -> list:
    """Zapisuje pozycje wskazane przez człowieka. Zwraca listę zapisanych plików."""
    zapisane = []
    wiersze = [
        "# Potwierdzony zestaw: pozycje wskazane przez człowieka",
        "",
        f"- utworzono: {teraz()}",
        "- do tego pliku trafiają wyłącznie pozycje, których numery człowiek wpisał przy zatrzymaniu grafu",
        f"- pełne zdanie modelu, razem z pozycjami niepotwierdzonymi, jest w pliku {protokol}",
        "",
    ]
    for krok in KROKI_MODELU:
        zdanie = stan["zdanie_modelu"][krok]
        tabele = wiersze_tabel(zdanie["tekst"])
        wiersze += [f"## Krok: {krok} (skill {zdanie['skill']})", ""]
        wskazane_w_kroku = []
        for pytanie, odpowiedz in stan["decyzja_czlowieka"].get(krok, {}).items():
            wskazane = numery(odpowiedz)
            wskazane_w_kroku += wskazane
            wiersze += [f"### {pytanie}", "", f"Odpowiedź człowieka: {odpowiedz or BEZ_ODPOWIEDZI}", ""]
            wiersze += wskazane_wiersze(tabele, wskazane)
        if krok == KROK_DANYCH and wskazane_w_kroku:
            dane, powod = dane_dla_przebiegu(zdanie["tekst"], wskazane_w_kroku)
            if dane is None:
                wiersze += [f"Pliku dla przebiegu nie zapisano: {powod}.", ""]
            else:
                plik_danych = katalog_zapisu / PLIK_DANYCH
                plik_danych.write_text(json.dumps(dane, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                zapisane.append(wzgledna(plik_danych))
                wiersze += [
                    f"Plik dla przebiegu, tylko ze wskazanymi wejściami: {zapisane[-1]}.",
                    "Przebieg uruchamia człowiek, na przykład:",
                    "",
                    "```powershell",
                    f"python narzedzia/przebieg_danych.py --port <port builda> --dane {zapisane[-1]}",
                    "```",
                    "",
                ]
    zestaw = katalog_zapisu / PLIK_ZESTAWU
    zestaw.write_text("\n".join(wiersze).rstrip("\n") + "\n", encoding="utf-8")
    return [wzgledna(zestaw), *zapisane]


def zbuduj(model, katalog_zapisu: Path = KATALOG_ZAPISU, opis_modelu: str = ""):
    def zapis(stan: Stan) -> dict:
        protokol = wzgledna(zapisz_protokol(katalog_zapisu / PLIK_PROTOKOLU, NAZWA, opis_modelu, stan))
        return {"zapisane": [*zapisz_zestaw(stan, katalog_zapisu, protokol), protokol]}

    graf = StateGraph(Stan)
    graf.add_node("wejscie", krok_wejscia(WYMAGANIE, DRUGA_HISTORYJKA, LISTA_TESTOW))
    graf.add_node("luki", krok_modelu(model, "luki", "luki-w-wymaganiu", [WYMAGANIE]))
    graf.add_node("uprawnienia_reset", krok_modelu(model, "uprawnienia_reset", "przypadki-uprawnien", [WYMAGANIE]))
    graf.add_node("uprawnienia_filtr",
                  krok_modelu(model, "uprawnienia_filtr", "przypadki-uprawnien", [DRUGA_HISTORYJKA]))
    graf.add_node("pokrycie", krok_modelu(model, "pokrycie", "pokrycie-wymagania", [WYMAGANIE, LISTA_TESTOW]))
    graf.add_node("dane", krok_modelu(model, "dane", "dane-pod-regule", [WYMAGANIE], zadanie=ZADANIE_DANE))
    graf.add_node("decyzja", krok_decyzji("decyzja", KROKI_MODELU))
    graf.add_node("zapis", zapis)

    kolejnosc = ["wejscie", *KROKI_MODELU, "decyzja", "zapis"]
    graf.add_edge(START, kolejnosc[0])
    for skad, dokad in zip(kolejnosc, kolejnosc[1:]):
        graf.add_edge(skad, dokad)
    graf.add_edge(kolejnosc[-1], END)
    return graf.compile(checkpointer=InMemorySaver())
