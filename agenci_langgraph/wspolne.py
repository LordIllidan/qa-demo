"""Wspólne części agentów LangGraph.

Podział ról w każdym grafie jest ten sam:
- wejście dla modelu przygotowują wyłącznie skrypty z katalogu narzedzia,
- instrukcją dla modelu jest skill wczytany z katalogu .github/skills,
- zdanie formułuje model, a graf go nie ocenia i nie poprawia,
- decyzję podejmuje człowiek przy zatrzymaniu grafu (interrupt),
- zapis powstaje dopiero po decyzji.
"""

from __future__ import annotations

import operator
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import interrupt

KATALOG = Path(__file__).resolve().parent.parent
NARZEDZIA = KATALOG / "narzedzia"
SKILLE = KATALOG / ".github" / "skills"
KATALOG_ZAPISU = KATALOG / "wyniki" / "agenci"

RAMA = """Jesteś krokiem grafu LangGraph w zestawie qa-demo dla testerów. Poniżej jest skill: instrukcja, według której formułujesz swoje zdanie.

Jak pracujesz w grafie:
- Nie masz terminala ani dostępu do plików. Polecenia wymienione w skillu wykonał już graf, a ich wynik dostajesz w wiadomości jako wejście. Innego wejścia nie ma.
- Gdy wejścia brakuje albo jest niepełne, napisz to w wyniku. Niczego nie zgaduj.
- Oddaj wynik w formacie ze skilla, z częściami „Zdanie modelu” i „Decyzja człowieka”. Decyzje zostaw bez odpowiedzi: graf zatrzyma się i zapyta o nie człowieka.
- Niczego nie zapisujesz i nie uruchamiasz. Zapis robi graf po decyzji człowieka i tylko dla pozycji, które człowiek wskazał."""

PYTANIE_OGOLNE = "Decyzja człowieka (model nie wypisał listy decyzji)"
BEZ_ODPOWIEDZI = "bez odpowiedzi"


class BladAgenta(Exception):
    """Agent nie mógł wykonać kroku; komunikat mówi, co zrobić."""


class Stan(TypedDict, total=False):
    """Stan grafu. Trzy pierwsze pola rosną z każdym krokiem i nigdy się nie mieszają."""

    wejscie: Annotated[dict, operator.or_]            # polecenie -> tekst oddany przez skrypt
    zdanie_modelu: Annotated[dict, operator.or_]      # krok -> skill, polecenia wejścia, tekst modelu
    decyzja_czlowieka: Annotated[dict, operator.or_]  # krok -> pytanie -> odpowiedź człowieka
    zapisane: list                                    # pliki zapisane po decyzji


def teraz() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def wzgledna(sciezka: Path) -> str:
    try:
        return sciezka.resolve().relative_to(KATALOG).as_posix()
    except ValueError:
        return sciezka.as_posix()


def opis_polecenia(polecenie: tuple) -> str:
    """Polecenie w postaci, w jakiej tester wpisuje je w PowerShell."""
    skrypt, *argumenty = polecenie
    return " ".join(["python", f"narzedzia/{skrypt}", *map(str, argumenty)])


def wejscie_ze_skryptu(polecenie: tuple) -> str:
    """Uruchamia skrypt z katalogu narzedzia i zwraca to, co wypisał."""
    skrypt, *argumenty = polecenie
    plik = NARZEDZIA / skrypt
    if not plik.is_file():
        raise BladAgenta(f"nie ma skryptu narzedzia/{skrypt}")
    srodowisko = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    proces = subprocess.run(
        [sys.executable, str(plik), *map(str, argumenty)],
        cwd=KATALOG, env=srodowisko, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proces.returncode != 0:
        raise BladAgenta(
            f"polecenie `{opis_polecenia(polecenie)}` nie przygotowało wejścia "
            f"(kod wyjścia {proces.returncode}).\n{proces.stdout}{proces.stderr}".rstrip()
        )
    return proces.stdout


def wczytaj_skill(nazwa: str) -> str:
    plik = SKILLE / nazwa / "SKILL.md"
    if not plik.is_file():
        raise BladAgenta(f"nie ma skilla {wzgledna(plik)}")
    return plik.read_text(encoding="utf-8")


def tekst_odpowiedzi(odpowiedz) -> str:
    tresc = getattr(odpowiedz, "content", odpowiedz)
    if isinstance(tresc, str):
        return tresc
    czesci = []
    for blok in tresc or []:
        if isinstance(blok, str):
            czesci.append(blok)
        elif isinstance(blok, dict) and blok.get("type") == "text":
            czesci.append(blok.get("text", ""))
    return "".join(czesci)


def zapytaj_model(model, skill: str, wejscia: dict, zadanie: str | None = None) -> str:
    """Model dostaje skill jako instrukcję i wynik skryptów jako wejście. Nic więcej."""
    czesci = [f"Zadanie: {zadanie}"] if zadanie else []
    for numer, (polecenie, tekst) in enumerate(wejscia.items(), start=1):
        czesci.append(f"Wejście {numer} z {len(wejscia)}, polecenie: {polecenie}\n\n{tekst.rstrip()}")
    wiadomosci = [
        SystemMessage(content=RAMA + "\n\n" + wczytaj_skill(skill)),
        HumanMessage(content="\n\n".join(czesci)),
    ]
    try:
        odpowiedz = model.invoke(wiadomosci)
    except Exception as blad:
        raise BladAgenta(f"model nie odpowiedział ({type(blad).__name__}): {blad}") from blad
    tekst = tekst_odpowiedzi(odpowiedz).strip()
    if not tekst:
        raise BladAgenta("model oddał pustą odpowiedź")
    return tekst


def pytania_do_czlowieka(tekst: str) -> list:
    """Wypisuje decyzje z części „Decyzja człowieka” w zdaniu modelu. Treści nie ocenia."""
    wiersze = [wiersz.strip() for wiersz in tekst.splitlines()]
    poczatki = [i for i, wiersz in enumerate(wiersze) if re.fullmatch(r"#{1,6}\s*Decyzja człowieka", wiersz)]
    pytania = []
    if poczatki:
        for wiersz in wiersze[poczatki[-1] + 1:]:
            if wiersz.startswith("#"):
                break
            pole = re.match(r"[-*]\s*\[\s?\]\s*(.+)", wiersz)
            if pole:
                pytanie = pole.group(1).rstrip(": ").strip()
                powtorzenia = sum(1 for p in pytania if p == pytanie or p.startswith(pytanie + " ("))
                pytania.append(pytanie if not powtorzenia else f"{pytanie} ({powtorzenia + 1})")
    return pytania or [PYTANIE_OGOLNE]


def krok_wejscia(*polecenia: tuple):
    """Krok grafu, który uruchamia skrypty i odkłada ich wynik w stanie."""
    def krok(stan: Stan) -> dict:
        return {"wejscie": {opis_polecenia(p): wejscie_ze_skryptu(p) for p in polecenia}}
    return krok


def krok_modelu(model, nazwa: str, skill: str, polecenia: list, zadanie: str | None = None):
    """Krok grafu, w którym model mówi swoje zdanie na podstawie wskazanych wejść."""
    opisy = [opis_polecenia(p) for p in polecenia]

    def krok(stan: Stan) -> dict:
        wejscia = {opis: stan["wejscie"][opis] for opis in opisy}
        tekst = zapytaj_model(model, skill, wejscia, zadanie)
        return {"zdanie_modelu": {nazwa: {"skill": skill, "wejscie": opisy, "tekst": tekst}}}
    return krok


def krok_decyzji(nazwa: str, kroki_modelu: list, pytania_grafu: tuple = (), pokaz_wczesniejsze: bool = False):
    """Krok grafu, który zatrzymuje graf i czeka na decyzję człowieka.

    Po wznowieniu LangGraph wykonuje ten krok od początku, dlatego krok niczego
    nie uruchamia i niczego nie zapisuje poza odpowiedzią człowieka.
    """
    def krok(stan: Stan) -> dict:
        pozycje = []
        for krok_m in kroki_modelu:
            zdanie = stan["zdanie_modelu"][krok_m]
            pozycje.append({
                "krok": krok_m,
                "skill": zdanie["skill"],
                "zdanie_modelu": zdanie["tekst"],
                "pytania": pytania_do_czlowieka(zdanie["tekst"]),
            })
        if pytania_grafu:
            pozycje.append({"krok": nazwa, "skill": None, "zdanie_modelu": None, "pytania": list(pytania_grafu)})
        zatrzymanie = {"zatrzymanie": nazwa, "pozycje": pozycje}
        if pokaz_wczesniejsze:
            zatrzymanie["wczesniejsze_decyzje"] = stan.get("decyzja_czlowieka", {})

        odpowiedzi = interrupt(zatrzymanie)

        if not isinstance(odpowiedzi, dict):
            raise BladAgenta("decyzja człowieka ma mieć postać: krok -> pytanie -> odpowiedź")
        decyzje = {}
        for pozycja in pozycje:
            udzielone = odpowiedzi.get(pozycja["krok"]) or {}
            decyzje[pozycja["krok"]] = {
                pytanie: str(udzielone.get(pytanie) or "").strip() for pytanie in pozycja["pytania"]
            }
        return {"decyzja_czlowieka": decyzje}
    return krok


def cytat(tekst: str) -> list:
    """Tekst modelu jako cytat Markdown, żeby jego nagłówki nie mieszały się z nagłówkami zapisu."""
    return [("> " + wiersz).rstrip() for wiersz in tekst.splitlines()]


def wiersze_decyzji(decyzje: dict) -> list:
    return [f"- {pytanie}: {odpowiedz or BEZ_ODPOWIEDZI}" for pytanie, odpowiedz in decyzje.items()]


def zapisz_protokol(plik: Path, tytul: str, opis_modelu: str, stan: Stan) -> Path:
    """Zapisuje przebieg grafu: przy każdym kroku osobno wejście, zdanie modelu i decyzję człowieka."""
    decyzje = stan.get("decyzja_czlowieka", {})
    wiersze = [
        f"# Protokół agenta: {tytul}",
        "",
        f"- utworzono: {teraz()}",
        f"- model: {opis_modelu or 'nie podano'}",
        "- zdanie modelu jest zapisane dosłownie, jako cytat; decyzje wpisał człowiek przy zatrzymaniu grafu",
        "",
    ]
    zdania = stan.get("zdanie_modelu", {})
    for krok in [*decyzje, *(k for k in zdania if k not in decyzje)]:
        if krok not in zdania:
            wiersze += [f"## Decyzja człowieka o dalszym kroku grafu: {krok}", "", *wiersze_decyzji(decyzje[krok]), ""]
            continue
        zdanie = zdania[krok]
        wiersze += [f"## Krok: {krok} (skill {zdanie['skill']})", "", "### Wejście ze skryptów", ""]
        wiersze += [f"- `{polecenie}`" for polecenie in zdanie["wejscie"]]
        wiersze += ["", "### Zdanie modelu", "", *cytat(zdanie["tekst"]), "", "### Decyzja człowieka", ""]
        wiersze += wiersze_decyzji(decyzje.get(krok, {})) or ["- graf nie pytał o decyzję w tym kroku"]
        wiersze.append("")
    plik.parent.mkdir(parents=True, exist_ok=True)
    plik.write_text("\n".join(wiersze).rstrip("\n") + "\n", encoding="utf-8")
    return plik
