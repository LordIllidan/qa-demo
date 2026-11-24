"""Agent „Jedno zagadnienie” (zagadnienia 3, P2, P3, P5, P6 i R1–R8).

Jeden wspólny graf dla zagadnień, których nie obejmują trzy pozostałe agenty:
wejście ze skryptów wskazanych przez skill, zdanie modelu według skilla,
zatrzymanie na decyzję człowieka i zapis protokołu dopiero po decyzji.

Człowiek może dołożyć do wejścia prośbę (`--prosba`) i pliki, które skill
wymienia jako wejście bez skryptu, na przykład notatki z sesji (`--plik`).
Graf wczytuje tylko pliki wskazane przez człowieka i odmawia plików
z katalogu prowadzacy.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from .wspolne import (
    KATALOG, KATALOG_ZAPISU, BladAgenta, Stan, krok_decyzji, opis_polecenia, wejscie_ze_skryptu, wzgledna,
    zapisz_protokol, zapytaj_model,
)

NAZWA = "Jedno zagadnienie"
PROWADZACY = KATALOG / "prowadzacy"
KROK_MODELU = "model"
ETYKIETA_PLIKU = "plik wskazany przez człowieka"

RESET = ("wymaganie.py", "reset-hasla")
FILTR = ("wymaganie.py", "filtr-zamowien")
LISTA_TESTOW = ("lista_testow.py",)


def z_portami(skrypt: str):
    return lambda a: [(skrypt, "--porty", *a.porty) if a.porty else (skrypt,), RESET]


def przebieg_po_poprawce(a) -> list:
    testy = [argument for nazwa in a.test for argument in ("--test", nazwa)]
    return [("przebieg.py", "--port", a.port, *testy)]


def historia(a) -> list:
    powtorzenia = ("--powtorzenia", a.powtorzenia) if a.powtorzenia else ()
    return [("historia.py", "--port", a.port, *powtorzenia)]


def plan_iteracji(a) -> list:
    return [("plan_iteracji.py",), *([("zmiana_wymagania.py",)] if a.zmiana_wymagania else [])]


@dataclass(frozen=True)
class Zagadnienie:
    numer: str
    tytul: str
    polecenia: object                       # argumenty z wiersza poleceń -> lista poleceń skryptów
    opcje: tuple = ()                       # opcje wiersza poleceń, z których korzysta zagadnienie
    aplikacja: bool = False                 # czy skrypty potrzebują działającej aplikacji
    pliki: tuple = ()                       # pliki, które skill wymienia jako wejście bez skryptu


ZAGADNIENIA = {
    "ocena-asercji": Zagadnienie("3", "Ocena asercji", z_portami("tabela_asercji.py"), ("porty",), True),
    "test-potwierdzajacy": Zagadnienie(
        "P2", "Ponowny test po poprawce", przebieg_po_poprawce, ("port_wymagany", "test"), True,
        ("material/zgloszenia/ZGL-101.md",)),
    "test-niestabilny": Zagadnienie("P3", "Test niestabilny", historia, ("port", "powtorzenia"), True),
    "sesja-eksploracyjna": Zagadnienie(
        "P5", "Karta sesji eksploracyjnej", lambda a: [RESET], (), False,
        ("material/sesja/ryzyka.md", "material/sesja/notatki-z-sesji.md")),
    "przeglad-zmiany-w-testach": Zagadnienie(
        "P6", "Przegląd zmiany w testach", z_portami("zmiana_w_testach.py"), ("porty",), True),
    "projektowanie-przypadkow": Zagadnienie("R1", "Przypadki testowe techniką", lambda a: [RESET, FILTR]),
    "zgloszenie-z-obserwacji": Zagadnienie(
        "R2", "Zgłoszenie z obserwacji ręcznej", lambda a: [RESET], (), False,
        ("material/sesja/notatki-z-sesji.md", "material/zgloszenia/otwarte.json")),
    "kandydaci-do-automatyzacji": Zagadnienie(
        "R3", "Kandydaci do automatyzacji", lambda a: [("lista_sprawdzen.py",), LISTA_TESTOW]),
    "szkic-testu-automatycznego": Zagadnienie(
        "R4", "Szkic testu automatycznego", lambda a: [RESET, LISTA_TESTOW], (), False, ("testy/conftest.py",)),
    "testy-niefunkcjonalne": Zagadnienie("R5", "Testy niefunkcjonalne", lambda a: [RESET, FILTR]),
    "testy-po-zmianie-wymagania": Zagadnienie(
        "R6", "Testy po zmianie wymagania", lambda a: [("zmiana_wymagania.py",)], (), False, ("testy/conftest.py",)),
    "testy-z-opisu-interfejsu": Zagadnienie(
        "R7", "Testy z opisu interfejsu", lambda a: [("opis_interfejsu.py",), RESET]),
    "plan-testow-iteracji": Zagadnienie("R8", "Plan testów iteracji", plan_iteracji, ("zmiana_wymagania",)),
}


def dodaj_opcje(parser, zagadnienie: Zagadnienie) -> None:
    """Opcje wiersza poleceń: to, co człowiek podaje w prośbie."""
    parser.add_argument("--prosba", default="", help="prośba człowieka przekazana modelowi jako zadanie")
    parser.add_argument("--plik", action="append", default=[], help="plik wskazany przez człowieka jako wejście; można powtórzyć")
    if "porty" in zagadnienie.opcje:
        parser.add_argument("--porty", type=int, nargs="+", help="porty buildów, jeśli inne niż domyślne w skrypcie")
    if "port" in zagadnienie.opcje:
        parser.add_argument("--port", type=int, default=8765, help="port builda (domyślnie 8765)")
    if "port_wymagany" in zagadnienie.opcje:
        parser.add_argument("--port", type=int, required=True, help="port builda z poprawką")
    if "test" in zagadnienie.opcje:
        parser.add_argument("--test", action="append", required=True, help="nazwa testu ze zgłoszenia; można powtórzyć")
    if "powtorzenia" in zagadnienie.opcje:
        parser.add_argument("--powtorzenia", type=int, help="liczba uruchomień zestawu, jeśli inna niż w skrypcie")
    if "zmiana_wymagania" in zagadnienie.opcje:
        parser.add_argument("--zmiana-wymagania", action="store_true",
                            help="dołóż do wejścia szczegóły zmiany wymagania (narzedzia/zmiana_wymagania.py)")


def plik_czlowieka(wskazany: str) -> Path:
    sciezka = Path(wskazany)
    if not sciezka.is_absolute():
        sciezka = sciezka if sciezka.exists() else KATALOG / sciezka
    sciezka = sciezka.resolve()
    if sciezka.is_relative_to(PROWADZACY.resolve()):
        raise BladAgenta("agent nie czyta katalogu prowadzacy")
    if not sciezka.is_file():
        raise BladAgenta(f"nie ma pliku {wskazany}")
    return sciezka


def zbuduj(model, nazwa: str, polecenia: list, prosba: str = "", pliki: tuple = (),
           katalog_zapisu: Path = KATALOG_ZAPISU, opis_modelu: str = ""):
    zagadnienie = ZAGADNIENIA[nazwa]
    sciezki = [plik_czlowieka(plik) for plik in pliki]
    opisy = [opis_polecenia(p) for p in polecenia]
    tytul = f"{zagadnienie.numer}. {zagadnienie.tytul}"

    def wejscie(stan: Stan) -> dict:
        return {"wejscie": {opis_polecenia(p): wejscie_ze_skryptu(p) for p in polecenia}}

    def zdanie(stan: Stan) -> dict:
        wejscia = {opis: stan["wejscie"][opis] for opis in opisy}
        for sciezka in sciezki:
            wejscia[f"{ETYKIETA_PLIKU}: {wzgledna(sciezka)}"] = sciezka.read_text(encoding="utf-8")
        tekst = zapytaj_model(model, nazwa, wejscia, prosba or None)
        return {"zdanie_modelu": {KROK_MODELU: {"skill": nazwa, "wejscie": opisy, "tekst": tekst}}}

    def zapis(stan: Stan) -> dict:
        wstep = ["## Prośba i pliki od człowieka", "", f"- prośba: {prosba or 'nie podano'}"]
        wstep += [f"- {ETYKIETA_PLIKU}: `{wzgledna(sciezka)}`" for sciezka in sciezki] or [f"- {ETYKIETA_PLIKU}: brak"]
        protokol = zapisz_protokol(katalog_zapisu / f"{nazwa}.md", tytul, opis_modelu, stan, wstep + [""])
        return {"zapisane": [wzgledna(protokol)]}

    graf = StateGraph(Stan)
    graf.add_node("wejscie", wejscie)
    graf.add_node(KROK_MODELU, zdanie)
    graf.add_node("decyzja", krok_decyzji("decyzja", [KROK_MODELU]))
    graf.add_node("zapis", zapis)
    kolejnosc = ["wejscie", KROK_MODELU, "decyzja", "zapis"]
    graf.add_edge(START, kolejnosc[0])
    for skad, dokad in zip(kolejnosc, kolejnosc[1:]):
        graf.add_edge(skad, dokad)
    graf.add_edge(kolejnosc[-1], END)
    return graf.compile(checkpointer=InMemorySaver())
