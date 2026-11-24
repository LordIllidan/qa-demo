"""Wypisuje z HTML strony to, co da się policzyć bez oceniania dostępności.

Użycie:  python narzedzia/dostepnosc.py --port 8765

Dla każdej strony: język, nagłówki, obrazki i to, czy mają atrybut alt,
pola formularza i etykiety, przyciski i ich tekst. Nie mówi, czy strona
jest dostępna.
"""

from __future__ import annotations

import argparse
import re
import urllib.request

from wspolne import ADRES, BladNarzedzia, build_na_porcie, oddaj, uruchom_narzedzie

SCIEZKI = ("/", "/reset")


def atrybut(znacznik: str, nazwa: str) -> str:
    znaleziony = re.search(rf'{nazwa}="([^"]*)"', znacznik)
    return znaleziony.group(1) if znaleziony else ""


def opisz(html: str) -> list:
    jezyk = re.search(r'<html[^>]* lang="([^"]*)"', html)
    naglowki = re.findall(r"<h([1-6])[^>]*>(.*?)</h\1>", html, flags=re.S)
    obrazki = re.findall(r"<img\b[^>]*>", html)
    pola = re.findall(r"<input\b[^>]*>", html)
    etykiety = re.findall(r'<label\b[^>]* for="([^"]*)"', html)
    przyciski = re.findall(r"<button\b[^>]*>(.*?)</button>", html, flags=re.S)
    wiersze = [
        f"język: {jezyk.group(1) if jezyk else 'brak'}",
        "nagłówki: " + (", ".join(f"h{poziom}: {tekst.strip()}" for poziom, tekst in naglowki) or "brak"),
        f"obrazki: {len(obrazki)}; bez atrybutu alt: {sum(1 for o in obrazki if ' alt=' not in o)}",
    ]
    for pole in pola:
        identyfikator = atrybut(pole, "id")
        wiersze.append(
            f"pole: id={identyfikator or 'brak'}, type={atrybut(pole, 'type') or 'brak'}, "
            f"etykieta: {'tak' if identyfikator and identyfikator in etykiety else 'nie'}"
        )
    if not pola:
        wiersze.append("pola: brak")
    wiersze.append("przyciski: " + (", ".join(p.strip() for p in przyciski) or "brak"))
    return wiersze


def pobierz(port: int, sciezka: str) -> str:
    try:
        with urllib.request.urlopen(f"http://{ADRES}:{port}{sciezka}", timeout=5) as odpowiedz:
            return odpowiedz.read().decode("utf-8")
    except OSError as blad:
        raise BladNarzedzia(f"aplikacja nie odpowiada na porcie {port} ({blad})") from blad


def main() -> None:
    parser = argparse.ArgumentParser(description="Inwentarz HTML stron resetu hasła.")
    parser.add_argument("--port", type=int, required=True, help="port builda")
    argumenty = parser.parse_args()
    build = build_na_porcie(argumenty.port)
    tresc = [
        "## Inwentarz stron",
        f"build: {build['numer']} (port {build['port']})",
        "uwaga: to jest spis znaczników, nie wynik audytu dostępności",
        "",
    ]
    for sciezka in SCIEZKI:
        tresc += [f"### {sciezka}", *opisz(pobierz(argumenty.port, sciezka)), ""]
    oddaj("dostepnosc.py", "inwentarz HTML", tresc, f"dostepnosc-{argumenty.port}.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
