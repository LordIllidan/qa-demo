"""Wspólne funkcje skryptów z katalogu narzedzia.

Skrypty dostarczają modelowi wejście (wymaganie, wynik przebiegu, liczby)
w stałym formacie. Niczego nie oceniają: nie porównują wyniku z oczekiwanym,
nie wskazują przyczyn i nie podpowiadają decyzji.
"""

from __future__ import annotations

import http.client
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path

KATALOG = Path(__file__).resolve().parent.parent
MATERIAL = KATALOG / "material"
WYNIKI = KATALOG / "wyniki"
TESTY = KATALOG / "testy"
ZESTAW_DOMYSLNY = "testy/test_reset_hasla.py"
ADRES = "127.0.0.1"

RAMKA_START = "=== WEJŚCIE DLA MODELU ==="
RAMKA_KONIEC = "=== KONIEC WEJŚCIA ==="


class BladNarzedzia(Exception):
    """Narzędzie nie mogło przygotować wejścia; komunikat mówi, co zrobić."""


def uruchom_narzedzie(funkcja) -> None:
    """Uruchamia funkcję główną skryptu i zamienia błąd narzędzia na czytelny komunikat."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        funkcja()
    except BladNarzedzia as blad:
        print(f"Narzędzie nie przygotowało wejścia: {blad}")
        sys.exit(2)


def teraz() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def wzgledna(sciezka: Path) -> str:
    try:
        return sciezka.resolve().relative_to(KATALOG).as_posix()
    except ValueError:
        return sciezka.as_posix()


def czytaj_tekst(sciezka: Path) -> str:
    if not sciezka.is_file():
        raise BladNarzedzia(f"nie ma pliku {wzgledna(sciezka)}")
    return sciezka.read_text(encoding="utf-8")


def czytaj_json(sciezka: Path) -> dict:
    try:
        return json.loads(czytaj_tekst(sciezka))
    except json.JSONDecodeError as blad:
        raise BladNarzedzia(f"plik {wzgledna(sciezka)} nie jest poprawnym JSON-em: {blad}") from blad


def zapisz_json(sciezka: Path, dane: dict) -> None:
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    sciezka.write_text(json.dumps(dane, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def json_w_wierszu(dane) -> str:
    return json.dumps(dane, ensure_ascii=False)


def tabela(naglowki: list, wiersze: list) -> list:
    """Tabela w składni Markdown; zwraca listę wierszy tekstu."""
    def wiersz(komorki) -> str:
        return "| " + " | ".join(str(k).replace("|", "\\|").replace("\n", " ") for k in komorki) + " |"

    return [wiersz(naglowki), wiersz(["---"] * len(naglowki))] + [wiersz(w) for w in wiersze]


def oddaj(narzedzie: str, rodzaj: str, tresc: list, nazwa_pliku: str, dodatkowe_pliki: list | None = None) -> None:
    """Wypisuje wejście w stałej ramce i zapisuje ten sam tekst w katalogu wyniki."""
    wiersze = [
        RAMKA_START,
        f"narzędzie: {narzedzie}",
        f"rodzaj wejścia: {rodzaj}",
        f"utworzono: {teraz()}",
        "uwaga: narzędzie podaje wejście i niczego nie ocenia",
        "",
        *tresc,
        RAMKA_KONIEC,
    ]
    tekst = "\n".join(wiersze) + "\n"
    cel = WYNIKI / nazwa_pliku
    cel.parent.mkdir(parents=True, exist_ok=True)
    cel.write_text(tekst, encoding="utf-8")
    sys.stdout.write(tekst)
    zapisane = [wzgledna(cel)] + [wzgledna(p) for p in (dodatkowe_pliki or [])]
    print("Zapisano: " + ", ".join(zapisane))


def zadanie_http(port: int, metoda: str, sciezka: str, dane: dict | None = None) -> tuple:
    """Wysyła żądanie do builda i zwraca parę: status, treść odpowiedzi."""
    naglowki = {}
    tresc = None
    if dane is not None:
        tresc = json.dumps(dane, ensure_ascii=False).encode("utf-8")
        naglowki["Content-Type"] = "application/json; charset=utf-8"
    polaczenie = http.client.HTTPConnection(ADRES, port, timeout=5)
    try:
        polaczenie.request(metoda, sciezka, body=tresc, headers=naglowki)
        odpowiedz = polaczenie.getresponse()
        tekst = odpowiedz.read().decode("utf-8")
    except OSError as blad:
        raise BladNarzedzia(
            f"aplikacja nie odpowiada na porcie {port} ({blad}). "
            "Uruchom ją w osobnym oknie poleceniem: python app/serwer.py"
        ) from blad
    finally:
        polaczenie.close()
    try:
        return odpowiedz.status, (json.loads(tekst) if tekst else {})
    except json.JSONDecodeError:
        return odpowiedz.status, {"tekst": tekst}


def build_na_porcie(port: int) -> dict:
    """Pyta build o numer. Zwraca słownik z polami port i numer."""
    status, tresc = zadanie_http(port, "GET", "/stan")
    if status != 200 or "build" not in tresc:
        raise BladNarzedzia(f"pod portem {port} nie odpowiada aplikacja demonstracyjna")
    return {"port": port, "numer": tresc["build"]}


def uruchom_testy(port: int, zestaw: str, nazwy: list | None = None) -> dict:
    """Uruchamia pytest na wskazanym porcie i zwraca przebieg w stałym formacie."""
    build = build_na_porcie(port)
    plik_zestawu = KATALOG / zestaw
    if not plik_zestawu.exists():
        raise BladNarzedzia(f"nie ma zestawu testów {zestaw}")
    cele = [f"{zestaw}::{nazwa}" for nazwa in nazwy] if nazwy else [zestaw]
    katalog_zestawu = plik_zestawu if plik_zestawu.is_dir() else plik_zestawu.parent
    wtyczka = [] if (katalog_zestawu / "conftest.py").exists() else ["-p", "testy.conftest"]

    WYNIKI.mkdir(parents=True, exist_ok=True)
    plik_wyniku = WYNIKI / f".przebieg-{uuid.uuid4().hex}.json"
    polecenie = [
        sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *wtyczka,
        "--port", str(port), "--wynik-json", str(plik_wyniku), *cele,
    ]
    srodowisko = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    start = teraz()
    proces = subprocess.run(polecenie, cwd=KATALOG, env=srodowisko, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    try:
        if proces.returncode not in (0, 1) or not plik_wyniku.is_file():
            raise BladNarzedzia(
                "pytest nie wykonał testów (kod wyjścia "
                f"{proces.returncode}).\n{proces.stdout}\n{proces.stderr}"
            )
        testy = czytaj_json(plik_wyniku)["testy"]
    finally:
        if plik_wyniku.exists():
            plik_wyniku.unlink()
    return {
        "format": "qa-demo/przebieg/1",
        "pochodzenie": "uruchomienie",
        "build": build,
        "zestaw": zestaw,
        "start": start,
        "podsumowanie": policz(testy),
        "testy": testy,
    }


def policz(testy: list) -> dict:
    liczby = {"zaliczony": 0, "niezaliczony": 0, "pominięty": 0, "błąd": 0}
    for test in testy:
        liczby[test["wynik"]] = liczby.get(test["wynik"], 0) + 1
    return {"liczba_testow": len(testy), **liczby}


def opisz_build(build: dict) -> str:
    return f"{build['numer']} (port {build['port']})"


def opisz_wymiane(wymiana: list) -> list:
    wiersze = []
    for wpis in wymiana:
        dane = "" if wpis.get("dane") is None else " " + json_w_wierszu(wpis["dane"])
        uwaga = f" [{wpis['uwaga']}]" if wpis.get("uwaga") else ""
        wiersze.append(
            f"  {wpis['nr']}. {wpis['zadanie']}{dane} -> {wpis['status']} "
            f"{json_w_wierszu(wpis['odpowiedz'])}{uwaga}"
        )
    return wiersze


def opisz_test(test: dict, poziom: str = "###") -> list:
    wiersze = [
        f"{poziom} {test['nazwa']}",
        f"plik: {test['plik']}",
        f"opis: {test['opis'] or 'brak'}",
        f"wynik: {test['wynik']}",
        f"czas: {test['czas_ms']} ms",
    ]
    if test.get("miejsce"):
        wiersze.append(f"miejsce: {test['miejsce']}")
    if test.get("asercja"):
        wiersze.append(f"wiersz, na którym test się zatrzymał: {test['asercja']}")
    if test.get("komunikat"):
        wiersze.append("komunikat:")
        wiersze.extend("  " + wiersz for wiersz in str(test["komunikat"]).splitlines())
    if test.get("wymiana"):
        wiersze.append("wymiana z aplikacją:")
        wiersze.extend(opisz_wymiane(test["wymiana"]))
    wiersze.append("")
    return wiersze


def opisz_przebieg(przebieg: dict, tytul: str = "Przebieg") -> list:
    liczby = przebieg["podsumowanie"]
    wiersze = [
        f"## {tytul}",
        f"build: {opisz_build(przebieg['build'])}",
        f"pochodzenie: {przebieg['pochodzenie']}",
        f"zestaw: {przebieg['zestaw']}",
        f"start: {przebieg['start']}",
        (
            f"liczba testów: {liczby['liczba_testow']}; zaliczone: {liczby['zaliczony']}; "
            f"niezaliczone: {liczby['niezaliczony']}; pominięte: {liczby['pominięty']}; "
            f"błędy: {liczby['błąd']}"
        ),
        "",
    ]
    for test in przebieg["testy"]:
        wiersze.extend(opisz_test(test))
    return wiersze
