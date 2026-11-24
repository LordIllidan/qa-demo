"""Wspólne zaplecze testów: klient aplikacji i zapis przebiegu.

Testy rozmawiają z aplikacją demonstracyjną przez HTTP. Port wybiera opcja --port.
Opcja --wynik-json zapisuje do pliku wynik każdego testu razem z wymianą żądań
i odpowiedzi. Z tego pliku korzystają skrypty z katalogu narzedzia.
"""

from __future__ import annotations

import http.client
import json
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

import pytest

ADRES = "127.0.0.1"
CZEKANIE_NA_WIADOMOSC_S = 3.0
ODSTEP_ODCZYTU_S = 0.02

_WYNIKI: list = []


@dataclass
class Odpowiedz:
    status: int
    tresc: dict


@dataclass
class Konto:
    email: str
    haslo: str


class Aplikacja:
    """Klient jednego builda. Każde żądanie i odpowiedź trafia do zapisu przebiegu."""

    def __init__(self, port: int, wymiana: list) -> None:
        self.port = port
        self.wymiana = wymiana

    def wyslij(self, metoda: str, sciezka: str, dane: dict | None = None,
               sesja: str | None = None, zapisz: bool = True) -> Odpowiedz:
        naglowki = {}
        tresc = None
        if dane is not None:
            tresc = json.dumps(dane, ensure_ascii=False).encode("utf-8")
            naglowki["Content-Type"] = "application/json; charset=utf-8"
        if sesja is not None:
            naglowki["Authorization"] = f"Bearer {sesja}"
        polaczenie = http.client.HTTPConnection(ADRES, self.port, timeout=5)
        try:
            polaczenie.request(metoda, sciezka, body=tresc, headers=naglowki)
            surowa = polaczenie.getresponse()
            tekst = surowa.read().decode("utf-8")
        finally:
            polaczenie.close()
        try:
            odczytana = json.loads(tekst) if tekst else {}
        except json.JSONDecodeError:
            odczytana = {"tekst": tekst}
        odpowiedz = Odpowiedz(status=surowa.status, tresc=odczytana)
        if zapisz:
            self._zapisz(metoda, sciezka, dane, odpowiedz)
        return odpowiedz

    def _zapisz(self, metoda: str, sciezka: str, dane: dict | None,
                odpowiedz: Odpowiedz, uwaga: str | None = None) -> None:
        wpis = {
            "nr": len(self.wymiana) + 1,
            "zadanie": f"{metoda} {sciezka}",
            "dane": dane,
            "status": odpowiedz.status,
            "odpowiedz": odpowiedz.tresc,
        }
        if uwaga:
            wpis["uwaga"] = uwaga
        self.wymiana.append(wpis)

    def zaloz_konto(self) -> Konto:
        konto = Konto(email=f"test-{uuid.uuid4().hex[:8]}@example.com", haslo="StareHaslo-1")
        odpowiedz = self.wyslij("POST", "/test/konto", {"email": konto.email, "haslo": konto.haslo})
        assert odpowiedz.status == 201, "środowisko testowe nie założyło konta"
        return konto

    def popros_o_reset(self, email: str) -> Odpowiedz:
        return self.wyslij("POST", "/reset/zamow", {"email": email})

    def czytaj_skrzynke(self, email: str) -> Odpowiedz:
        return self.wyslij("GET", f"/test/skrzynka?email={email}")

    def zamow_link_resetu(self, email: str) -> str:
        """Prosi o reset, czeka na wiadomość i zwraca token z linku."""
        self.popros_o_reset(email)
        sciezka = f"/test/skrzynka?email={email}"
        koniec = time.monotonic() + CZEKANIE_NA_WIADOMOSC_S
        proby = 0
        while True:
            proby += 1
            odpowiedz = self.wyslij("GET", sciezka, zapisz=False)
            if odpowiedz.status == 200 or time.monotonic() >= koniec:
                break
            time.sleep(ODSTEP_ODCZYTU_S)
        self._zapisz("GET", sciezka, None, odpowiedz,
                     uwaga=f"odczyt skrzynki ponawiany do skutku, liczba odczytów: {proby}")
        assert odpowiedz.status == 200, "wiadomość z linkiem resetu nie doszła"
        return odpowiedz.tresc["token"]

    def ustaw_haslo(self, token: str, haslo: str) -> Odpowiedz:
        return self.wyslij("POST", "/reset/potwierdz", {"token": token, "haslo": haslo})

    def zaloguj(self, email: str, haslo: str) -> Odpowiedz:
        return self.wyslij("POST", "/logowanie", {"email": email, "haslo": haslo})

    def stan(self) -> Odpowiedz:
        return self.wyslij("GET", "/stan")


def pytest_addoption(parser) -> None:
    parser.addoption("--port", type=int, default=8765,
                     help="port builda aplikacji demonstracyjnej (8765, 8766 albo 8767)")
    parser.addoption("--wynik-json", default=None,
                     help="plik, do którego trafi zapis przebiegu")


@pytest.fixture
def aplikacja(request) -> Aplikacja:
    request.node.wymiana = []
    return Aplikacja(request.config.getoption("--port"), request.node.wymiana)


@pytest.fixture
def konto(aplikacja) -> Konto:
    return aplikacja.zaloz_konto()


def _opis(item) -> str:
    funkcja = getattr(item, "function", None)
    return " ".join((getattr(funkcja, "__doc__", None) or "").split())


def _miejsce_i_asercja(item, raport) -> tuple:
    awaria = getattr(raport.longrepr, "reprcrash", None)
    if awaria is None:
        return None, None
    sciezka = Path(awaria.path)
    try:
        wiersz = sciezka.read_text(encoding="utf-8").splitlines()[awaria.lineno - 1].strip()
    except (OSError, IndexError):
        wiersz = None
    try:
        wzgledna = sciezka.resolve().relative_to(Path(item.config.rootpath).resolve()).as_posix()
    except ValueError:
        wzgledna = sciezka.as_posix()
    return f"{wzgledna}:{awaria.lineno}", wiersz


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    raport = yield
    if raport.when == "call":
        wynik = {"passed": "zaliczony", "failed": "niezaliczony", "skipped": "pominięty"}[raport.outcome]
    elif raport.when == "setup" and raport.outcome == "skipped":
        wynik = "pominięty"
    elif raport.outcome == "failed":
        wynik = "błąd"
    else:
        return raport

    wpis = {
        "nazwa": item.name,
        "plik": item.nodeid.split("::")[0],
        "opis": _opis(item),
        "wynik": wynik,
        "czas_ms": round(call.duration * 1000),
        "komunikat": None,
        "miejsce": None,
        "asercja": None,
        "wymiana": list(getattr(item, "wymiana", [])),
    }
    if wynik == "pominięty":
        powod = raport.longrepr[2] if isinstance(raport.longrepr, tuple) else str(raport.longrepr)
        wpis["komunikat"] = powod
    elif wynik in ("niezaliczony", "błąd") and call.excinfo is not None:
        wpis["komunikat"] = call.excinfo.exconly()
        wpis["miejsce"], wpis["asercja"] = _miejsce_i_asercja(item, raport)
    _WYNIKI.append(wpis)
    return raport


def pytest_sessionfinish(session) -> None:
    cel = session.config.getoption("--wynik-json")
    if not cel:
        return
    sciezka = Path(cel)
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    sciezka.write_text(json.dumps({"testy": _WYNIKI}, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
