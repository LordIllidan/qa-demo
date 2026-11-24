"""Prosi o reset i podaje nagłówki oraz treść wiadomości ze skrzynki.

Użycie:  python narzedzia/wiadomosc.py --port 8765 --email anna@example.com

Skrypt nie ocenia nadawcy, treści, linku ani tokenu.
"""

from __future__ import annotations

import argparse
import time

from wspolne import BladNarzedzia, build_na_porcie, oddaj, uruchom_narzedzie, zadanie_http

CZEKANIE_S = 2.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Wiadomość z linkiem resetu ze skrzynki builda.")
    parser.add_argument("--port", type=int, required=True, help="port builda")
    parser.add_argument("--email", default="anna@example.com", help="adres skrzynki")
    argumenty = parser.parse_args()
    build = build_na_porcie(argumenty.port)
    zadanie_http(argumenty.port, "POST", "/reset/zamow", {"email": argumenty.email})
    koniec = time.monotonic() + CZEKANIE_S
    while True:
        status, tresc = zadanie_http(argumenty.port, "GET", f"/test/skrzynka?email={argumenty.email}")
        if status == 200:
            break
        if time.monotonic() > koniec:
            raise BladNarzedzia(f"skrzynka {argumenty.email} na porcie {argumenty.port} nie dostała wiadomości")
        time.sleep(0.05)
    wiersze = [
        "## Wiadomość ze skrzynki",
        f"build: {build['numer']} (port {build['port']})",
        f"adres skrzynki: {argumenty.email}",
        "",
        f"od: {tresc.get('od', '')}",
        f"do: {tresc.get('do', '')}",
        f"temat: {tresc.get('temat', '')}",
        f"link: {tresc.get('link', '')}",
        f"token: {tresc.get('token', '')}",
        "",
        "treść:",
        tresc.get("tresc", ""),
        "",
    ]
    oddaj("wiadomosc.py", "wiadomość przychodząca", wiersze, f"wiadomosc-{argumenty.port}.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
