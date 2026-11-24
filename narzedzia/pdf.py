"""Pobiera PDF z builda i wyciąga z niego tekst oraz tytuł.

Użycie:  python narzedzia/pdf.py --port 8765

Tekst bierze z napisów UTF-16 w strumieniu treści. Nie ocenia treści
względem wymagania i nie renderuje strony.
"""

from __future__ import annotations

import argparse
import re
import urllib.request

from wspolne import ADRES, BladNarzedzia, build_na_porcie, oddaj, uruchom_narzedzie


def wyciagnij(pdf: bytes) -> tuple:
    if not pdf.startswith(b"%PDF-"):
        raise BladNarzedzia("odpowiedź nie jest plikiem PDF")
    tytul = re.search(rb"/Title \(([^)]*)\)", pdf)
    linie = [
        bytes.fromhex(surowe.decode("ascii")).decode("utf-16-be")
        for surowe in re.findall(rb"<FEFF([0-9A-Fa-f]+)>", pdf)
    ]
    return (tytul.group(1).decode("latin-1") if tytul else ""), linie


def main() -> None:
    parser = argparse.ArgumentParser(description="Tekst i metadane PDF z builda.")
    parser.add_argument("--port", type=int, required=True, help="port builda")
    argumenty = parser.parse_args()
    build = build_na_porcie(argumenty.port)
    adres = f"http://{ADRES}:{argumenty.port}/test/potwierdzenie.pdf"
    try:
        with urllib.request.urlopen(adres, timeout=5) as odpowiedz:
            pdf = odpowiedz.read()
            typ = odpowiedz.headers.get("Content-Type", "")
    except OSError as blad:
        raise BladNarzedzia(f"aplikacja nie odpowiada na porcie {argumenty.port} ({blad})") from blad
    tytul, linie = wyciagnij(pdf)
    tresc = [
        "## PDF",
        f"build: {build['numer']} (port {build['port']})",
        f"adres: {adres}",
        f"typ odpowiedzi: {typ}",
        f"rozmiar: {len(pdf)} bajtów",
        f"tytuł z metadanych: {tytul or 'brak'}",
        "liczba wierszy tekstu: " + str(len(linie)),
        "",
        "tekst wyciągnięty ze strumienia:",
        *(linie or ["(brak napisów UTF-16 w strumieniu)"]),
        "",
    ]
    oddaj("pdf.py", "tekst i metadane PDF", tresc, f"pdf-{argumenty.port}.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
