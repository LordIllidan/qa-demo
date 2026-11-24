"""Aplikacja demonstracyjna: reset hasła w trzech buildach.

Uruchomienie wszystkich buildów:   python app/serwer.py
Uruchomienie jednego builda:       python app/serwer.py --port 8766

Port wyznacza build. Opis buildów i punktów końcowych: docs/aplikacja.md.
"""

from __future__ import annotations

import argparse
import json
import random
import secrets
import sys
import threading
import time
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ADRES = "127.0.0.1"

# Wiadomość z linkiem trafia do skrzynki z opóźnieniem z tego zakresu (sekundy),
# tak jak w systemie, w którym pocztę wysyła osobna usługa.
OPOZNIENIE_POCZTY_S = (0.0, 0.12)

KONTO_STARTOWE = ("anna@example.com", "StareHaslo-1")


@dataclass(frozen=True)
class Build:
    numer: str
    link_jednorazowy: bool


BUILDY = {
    8765: Build(numer="1.4.0", link_jednorazowy=True),
    8766: Build(numer="1.5.0", link_jednorazowy=False),
    8767: Build(numer="1.5.1", link_jednorazowy=True),
}


@dataclass
class Stan:
    """Dane jednego builda. Każdy build ma własne konta, tokeny i sesje."""

    build: Build
    port: int
    blokada: threading.Lock = field(default_factory=threading.Lock)
    hasla: dict = field(default_factory=dict)
    tokeny: dict = field(default_factory=dict)
    uzyte_tokeny: set = field(default_factory=set)
    sesje: dict = field(default_factory=dict)
    skrzynki: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        email, haslo = KONTO_STARTOWE
        self.hasla[email] = haslo

    def zaloz_konto(self, email: str, haslo: str) -> None:
        with self.blokada:
            self.hasla[email] = haslo

    def zamow_reset(self, email: str) -> None:
        with self.blokada:
            if email not in self.hasla:
                return
            token = secrets.token_urlsafe(16)
            self.tokeny[token] = email
            wiadomosc = {
                "temat": "Reset hasła",
                "link": f"http://{ADRES}:{self.port}/reset?token={token}",
                "token": token,
                "dostepna_od": time.monotonic() + random.uniform(*OPOZNIENIE_POCZTY_S),
            }
            self.skrzynki.setdefault(email, []).append(wiadomosc)

    def ustaw_haslo(self, token: str, haslo: str) -> tuple[int, dict]:
        with self.blokada:
            if not token or token not in self.tokeny:
                return 400, {"blad": "Brak tokenu albo token nie został wydany przez system."}
            if not haslo:
                return 400, {"blad": "Brak nowego hasła."}
            if token in self.uzyte_tokeny:
                return 410, {"blad": "Link resetu był już użyty."}
            email = self.tokeny[token]
            self.hasla[email] = haslo
            self.sesje = {s: e for s, e in self.sesje.items() if e != email}
            if self.build.link_jednorazowy:
                self.uzyte_tokeny.add(token)
            return 200, {"komunikat": "Hasło zostało zmienione."}

    def zaloguj(self, email: str, haslo: str) -> tuple[int, dict]:
        with self.blokada:
            if not haslo or self.hasla.get(email) != haslo:
                return 401, {"blad": "Błędny adres e-mail albo hasło."}
            sesja = secrets.token_urlsafe(16)
            self.sesje[sesja] = email
            return 200, {"sesja": sesja}

    def konto(self, sesja: str) -> tuple[int, dict]:
        with self.blokada:
            email = self.sesje.get(sesja)
            if email is None:
                return 401, {"blad": "Brak działającej sesji."}
            return 200, {"email": email}

    def skrzynka(self, email: str) -> tuple[int, dict]:
        with self.blokada:
            teraz = time.monotonic()
            wiadomosci = self.skrzynki.get(email, [])
            dostarczone = [w for w in wiadomosci if w["dostepna_od"] <= teraz]
            if not dostarczone:
                w_drodze = len(wiadomosci) - len(dostarczone)
                return 404, {"blad": "Brak wiadomości w skrzynce.", "w_drodze": w_drodze}
            ostatnia = dostarczone[-1]
            return 200, {
                "email": email,
                "temat": ostatnia["temat"],
                "link": ostatnia["link"],
                "token": ostatnia["token"],
            }


class Obsluga(BaseHTTPRequestHandler):
    stan: Stan

    def do_GET(self) -> None:
        adres = urlparse(self.path)
        parametry = parse_qs(adres.query)
        if adres.path == "/stan":
            self._odpowiedz(200, {"build": self.stan.build.numer, "port": self.stan.port})
        elif adres.path == "/konto":
            naglowek = self.headers.get("Authorization", "")
            sesja = naglowek[len("Bearer "):] if naglowek.startswith("Bearer ") else ""
            self._odpowiedz(*self.stan.konto(sesja))
        elif adres.path == "/test/skrzynka":
            email = parametry.get("email", [""])[0]
            self._odpowiedz(*self.stan.skrzynka(email))
        else:
            self._odpowiedz(404, {"blad": "Nie ma takiego adresu."})

    def do_POST(self) -> None:
        adres = urlparse(self.path)
        dane = self._czytaj_json()
        if dane is None:
            self._odpowiedz(400, {"blad": "Treść żądania nie jest obiektem JSON."})
            return
        email = str(dane.get("email") or "")
        haslo = str(dane.get("haslo") or "")
        if adres.path == "/reset/zamow":
            self.stan.zamow_reset(email)
            self._odpowiedz(202, {"komunikat": "Jeśli konto istnieje, wysłaliśmy wiadomość z linkiem resetu."})
        elif adres.path == "/reset/potwierdz":
            self._odpowiedz(*self.stan.ustaw_haslo(str(dane.get("token") or ""), haslo))
        elif adres.path == "/logowanie":
            self._odpowiedz(*self.stan.zaloguj(email, haslo))
        elif adres.path == "/test/konto":
            if not email or not haslo:
                self._odpowiedz(400, {"blad": "Podaj pola email i haslo."})
                return
            self.stan.zaloz_konto(email, haslo)
            self._odpowiedz(201, {"email": email})
        else:
            self._odpowiedz(404, {"blad": "Nie ma takiego adresu."})

    def _czytaj_json(self) -> dict | None:
        dlugosc = int(self.headers.get("Content-Length") or 0)
        surowe = self.rfile.read(dlugosc) if dlugosc else b"{}"
        try:
            dane = json.loads(surowe.decode("utf-8") or "{}")
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        return dane if isinstance(dane, dict) else None

    def _odpowiedz(self, status: int, tresc: dict) -> None:
        surowe = json.dumps(tresc, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(surowe)))
        self.end_headers()
        self.wfile.write(surowe)

    def log_message(self, format: str, *args) -> None:
        sys.stdout.write(f"[{self.stan.port} build {self.stan.build.numer}] {format % args}\n")
        sys.stdout.flush()


def uruchom(port: int) -> ThreadingHTTPServer:
    stan = Stan(build=BUILDY[port], port=port)
    obsluga = type("ObslugaBuilda", (Obsluga,), {"stan": stan})
    serwer = ThreadingHTTPServer((ADRES, port), obsluga)
    serwer.daemon_threads = True
    threading.Thread(target=serwer.serve_forever, daemon=True).start()
    return serwer


def main() -> int:
    parser = argparse.ArgumentParser(description="Aplikacja demonstracyjna: reset hasła.")
    parser.add_argument(
        "--port",
        type=int,
        choices=sorted(BUILDY),
        help="uruchom tylko build z tego portu; bez tej opcji startują wszystkie buildy",
    )
    argumenty = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    porty = [argumenty.port] if argumenty.port else sorted(BUILDY)
    serwery = []
    for port in porty:
        try:
            serwery.append(uruchom(port))
        except OSError as blad:
            print(f"Nie mogę zająć portu {port}: {blad}")
            return 1
        print(f"Build {BUILDY[port].numer} działa pod adresem http://{ADRES}:{port}")
    print("Zatrzymanie: Ctrl+C")
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Zatrzymuję.")
    for serwer in serwery:
        serwer.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
