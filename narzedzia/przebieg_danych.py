"""Wysyła do builda dane z pliku i podaje odpowiedzi obok oczekiwań zapisanych w pliku.

Użycie:  python narzedzia/przebieg_danych.py --port 8766
         python narzedzia/przebieg_danych.py --port 8765 --dane material/dane/dane-resetu.json

Skrypt nie porównuje odpowiedzi z oczekiwaniem. Format pliku z danymi:
docs/narzedzie-przebieg-danych.md.
"""

from __future__ import annotations

import argparse
import time
import uuid
from pathlib import Path

from wspolne import (
    MATERIAL,
    WYNIKI,
    BladNarzedzia,
    build_na_porcie,
    czytaj_json,
    json_w_wierszu,
    oddaj,
    opisz_build,
    tabela,
    teraz,
    uruchom_narzedzie,
    wzgledna,
    zadanie_http,
    zapisz_json,
)

PLIK_DOMYSLNY = MATERIAL / "dane" / "dane-resetu.json"
NOWY_LINK = "{nowy-link}"
TEN_SAM_LINK = "{ten-sam-link}"
HASLO_STARTOWE = "StareHaslo-1"
CZEKANIE_NA_WIADOMOSC_S = 3.0


def nowy_token(port: int, email: str, wydane: set) -> str:
    """Prosi o reset i czeka, aż w skrzynce pojawi się wiadomość z nowym tokenem."""
    zadanie_http(port, "POST", "/reset/zamow", {"email": email})
    koniec = time.monotonic() + CZEKANIE_NA_WIADOMOSC_S
    while time.monotonic() < koniec:
        status, tresc = zadanie_http(port, "GET", f"/test/skrzynka?email={email}")
        if status == 200 and tresc["token"] not in wydane:
            wydane.add(tresc["token"])
            return tresc["token"]
        time.sleep(0.02)
    raise BladNarzedzia("wiadomość z linkiem resetu nie doszła do skrzynki testowej")


def main() -> None:
    parser = argparse.ArgumentParser(description="Przebieg na danych z pliku.")
    parser.add_argument("--port", type=int, required=True, help="port builda")
    parser.add_argument("--dane", type=Path, default=PLIK_DOMYSLNY, help="plik z danymi wejściowymi")
    argumenty = parser.parse_args()

    dane = czytaj_json(argumenty.dane)
    wejscia = dane.get("wejscia")
    if not isinstance(wejscia, list) or not wejscia:
        raise BladNarzedzia(f"plik {wzgledna(argumenty.dane)} nie ma listy wejscia")

    build = build_na_porcie(argumenty.port)
    email = f"dane-{uuid.uuid4().hex[:8]}@example.com"
    status, _ = zadanie_http(argumenty.port, "POST", "/test/konto", {"email": email, "haslo": HASLO_STARTOWE})
    if status != 201:
        raise BladNarzedzia("środowisko testowe nie założyło konta")

    wydane: set = set()
    ostatni_token = None
    wyniki = []
    for wejscie in wejscia:
        token = wejscie.get("token", "")
        if token == NOWY_LINK:
            ostatni_token = nowy_token(argumenty.port, email, wydane)
            wyslany = ostatni_token
        elif token == TEN_SAM_LINK:
            if ostatni_token is None:
                raise BladNarzedzia(f"wejście {wejscie.get('id')}: {TEN_SAM_LINK} wymaga wcześniejszego {NOWY_LINK}")
            wyslany = ostatni_token
        else:
            wyslany = token
        tresc_zadania = {"token": wyslany, "haslo": wejscie.get("haslo", "")}
        status, odpowiedz = zadanie_http(argumenty.port, "POST", "/reset/potwierdz", tresc_zadania)
        wyniki.append({
            "id": wejscie.get("id"),
            "opis": wejscie.get("opis"),
            "token_w_pliku": token,
            "zadanie": tresc_zadania,
            "oczekiwany_status": wejscie.get("oczekiwany_status"),
            "pytanie": wejscie.get("pytanie"),
            "zrodlo": wejscie.get("zrodlo"),
            "status": status,
            "odpowiedz": odpowiedz,
        })

    przebieg = {
        "format": "qa-demo/przebieg-danych/1",
        "pochodzenie": "uruchomienie",
        "build": build,
        "plik_danych": wzgledna(argumenty.dane),
        "operacja": "POST /reset/potwierdz",
        "konto": email,
        "start": teraz(),
        "wyniki": wyniki,
    }

    wiersze = []
    for w in wyniki:
        if w["oczekiwany_status"] is not None:
            oczekiwane = w["oczekiwany_status"]
        elif w["pytanie"]:
            oczekiwane = f"brak; pytanie: {w['pytanie']}"
        else:
            oczekiwane = "brak"
        wiersze.append([
            w["id"], w["opis"], json_w_wierszu(w["token_w_pliku"]), json_w_wierszu(w["zadanie"]["haslo"]),
            oczekiwane, w["status"], json_w_wierszu(w["odpowiedz"]), w["zrodlo"] or "brak",
        ])
    tresc = [
        "## Przebieg na danych z pliku",
        f"build: {opisz_build(build)}",
        "pochodzenie: uruchomienie",
        f"plik z danymi: {przebieg['plik_danych']}",
        f"operacja: {przebieg['operacja']}",
        f"konto założone na czas przebiegu: {email} (hasło startowe {HASLO_STARTOWE})",
        f"start: {przebieg['start']}",
        "kolejność: wejścia wysłane jedno po drugim, w kolejności z pliku",
        "",
        *tabela(
            ["id", "opis", "token w pliku", "hasło", "oczekiwany status (z pliku)",
             "status odpowiedzi", "treść odpowiedzi", "źródło oczekiwania (z pliku)"],
            wiersze,
        ),
        "",
    ]
    plik_json = WYNIKI / f"przebieg-danych-{argumenty.port}.json"
    zapisz_json(plik_json, przebieg)
    oddaj("przebieg_danych.py", "wynik przebiegu", tresc, f"przebieg-danych-{argumenty.port}.txt", [plik_json])


if __name__ == "__main__":
    uruchom_narzedzie(main)
