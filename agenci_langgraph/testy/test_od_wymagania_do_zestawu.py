"""Graf „Od wymagania do potwierdzonego zestawu”: kroki, zatrzymanie, wznowienie, zapis."""

from __future__ import annotations

import json

from langgraph.types import Command

from agenci_langgraph.od_wymagania_do_zestawu import (
    KROKI_MODELU,
    PLIK_DANYCH,
    PLIK_PROTOKOLU,
    PLIK_ZESTAWU,
    dane_dla_przebiegu,
    numery,
    wiersze_tabel,
    zbuduj,
)
from agenci_langgraph.testy.pomoc import Przebieg, bez_odpowiedzi
from agenci_langgraph.wspolne import RAMA, wczytaj_skill

SKILLE = ["luki-w-wymaganiu", "przypadki-uprawnien", "przypadki-uprawnien", "pokrycie-wymagania", "dane-pod-regule"]


def numery_wierszy(zatrzymanie: dict, krok: str) -> list:
    pozycja = next(p for p in zatrzymanie["pozycje"] if p["krok"] == krok)
    return list(wiersze_tabel(pozycja["zdanie_modelu"]))


def pytania(zatrzymanie: dict, krok: str) -> list:
    return next(p for p in zatrzymanie["pozycje"] if p["krok"] == krok)["pytania"]


def test_graf_zatrzymuje_sie_na_decyzji_i_niczego_nie_zapisuje(model, tmp_path):
    przebieg = Przebieg(zbuduj(model, tmp_path))

    zatrzymanie = przebieg.do_zatrzymania({})

    assert zatrzymanie["zatrzymanie"] == "decyzja"
    assert [pozycja["krok"] for pozycja in zatrzymanie["pozycje"]] == KROKI_MODELU
    assert all(pozycja["zdanie_modelu"] and pozycja["pytania"] for pozycja in zatrzymanie["pozycje"])
    assert przebieg.nastepny_krok == ("decyzja",)
    assert not przebieg.stan.get("decyzja_czlowieka") and not przebieg.stan.get("zapisane")
    assert list(tmp_path.iterdir()) == []


def test_kazdy_krok_modelu_dostaje_swoj_skill_i_tylko_wejscie_ze_skryptow(model, tmp_path):
    przebieg = Przebieg(zbuduj(model, tmp_path))
    przebieg.do_zatrzymania({})
    stan = przebieg.stan

    assert set(stan["wejscie"]) == {
        "python narzedzia/wymaganie.py reset-hasla",
        "python narzedzia/wymaganie.py filtr-zamowien",
        "python narzedzia/lista_testow.py",
    }
    assert len(model.wywolania) == len(KROKI_MODELU)
    for krok, skill, wywolanie in zip(KROKI_MODELU, SKILLE, model.wywolania):
        zdanie = stan["zdanie_modelu"][krok]
        assert zdanie["skill"] == skill
        assert wywolanie["instrukcja"] == RAMA + "\n\n" + wczytaj_skill(skill)
        assert wywolanie["wejscie"].count("=== WEJŚCIE DLA MODELU ===") == len(zdanie["wejscie"])
        for polecenie in zdanie["wejscie"]:
            assert stan["wejscie"][polecenie].rstrip() in wywolanie["wejscie"]
    assert stan["zdanie_modelu"]["uprawnienia_filtr"]["wejscie"] == ["python narzedzia/wymaganie.py filtr-zamowien"]
    assert stan["zdanie_modelu"]["pokrycie"]["wejscie"] == [
        "python narzedzia/wymaganie.py reset-hasla", "python narzedzia/lista_testow.py",
    ]


def test_po_decyzji_do_zestawu_wchodzi_tylko_to_co_wskazal_czlowiek(model, tmp_path):
    przebieg = Przebieg(zbuduj(model, tmp_path, "model zastępczy"))
    zatrzymanie = przebieg.do_zatrzymania({})
    potwierdzony, pominiety = numery_wierszy(zatrzymanie, "luki")[:2]
    wejscie_do_przebiegu = numery_wierszy(zatrzymanie, "dane")[0]
    decyzja = bez_odpowiedzi(zatrzymanie)
    decyzja["luki"][pytania(zatrzymanie, "luki")[-1]] = f"{potwierdzony} i X99"
    decyzja["dane"][pytania(zatrzymanie, "dane")[0]] = wejscie_do_przebiegu

    assert przebieg.do_zatrzymania(Command(resume=decyzja)) is None

    assert przebieg.nastepny_krok == ()
    stan = przebieg.stan
    assert stan["decyzja_czlowieka"]["luki"][pytania(zatrzymanie, "luki")[-1]] == f"{potwierdzony} i X99"
    assert len(model.wywolania) == len(KROKI_MODELU), "po decyzji graf nie pyta modelu ponownie"
    assert sorted(plik.name for plik in tmp_path.iterdir()) == sorted([PLIK_PROTOKOLU, PLIK_ZESTAWU, PLIK_DANYCH])
    assert len(stan["zapisane"]) == 3

    zestaw = (tmp_path / PLIK_ZESTAWU).read_text(encoding="utf-8")
    assert f"| {potwierdzony} |" in zestaw
    assert f"| {pominiety} |" not in zestaw
    assert "Numery, których nie ma w tabelach zdania modelu: X99" in zestaw
    assert zestaw.count("Odpowiedź człowieka: bez odpowiedzi") == sum(len(d) for d in decyzja.values()) - 2

    dane = json.loads((tmp_path / PLIK_DANYCH).read_text(encoding="utf-8"))
    assert [wejscie["id"] for wejscie in dane["wejscia"]] == [wejscie_do_przebiegu]

    protokol = (tmp_path / PLIK_PROTOKOLU).read_text(encoding="utf-8")
    assert "- model: model zastępczy" in protokol
    for krok in KROKI_MODELU:
        assert f"## Krok: {krok} (skill " in protokol
    assert protokol.count("### Zdanie modelu") == protokol.count("### Decyzja człowieka") == len(KROKI_MODELU)
    assert f"- {pytania(zatrzymanie, 'luki')[-1]}: {potwierdzony} i X99" in protokol
    assert all(plik.read_text(encoding="utf-8").endswith("\n") for plik in tmp_path.iterdir())


def test_bez_potwierdzenia_nic_nie_wchodzi_do_zestawu(model, tmp_path):
    przebieg = Przebieg(zbuduj(model, tmp_path))
    zatrzymanie = przebieg.do_zatrzymania({})

    przebieg.do_zatrzymania(Command(resume=bez_odpowiedzi(zatrzymanie)))

    zestaw = (tmp_path / PLIK_ZESTAWU).read_text(encoding="utf-8")
    assert not [wiersz for wiersz in zestaw.splitlines() if wiersz.startswith("|")]
    assert not (tmp_path / PLIK_DANYCH).exists()


def test_numery_z_odpowiedzi_czlowieka():
    assert numery("m1, M3 oraz D12; nie: ZGL-101, 8766, wersja2, wszystkie") == ["M1", "M3", "D12"]


def test_zakres_numerow_nie_jest_rozwijany():
    assert numery("U1-U3") == numery("U1–U3") == ["U1", "U3"]


def test_wiersze_tabel_sa_wybierane_po_numerze_z_pierwszej_kolumny():
    tekst = "\n".join([
        "| Nr | Przypadek |",
        "| --- | --- |",
        "| M1 | pierwszy, odsyła do P1 |",
        "| M2 | drugi |",
        "",
        "| Nr | Pytanie |",
        "| --- | --- |",
        "| P1 | pytanie |",
    ])

    tabele = wiersze_tabel(tekst)

    assert list(tabele) == ["M1", "M2", "P1"]
    assert tabele["M1"] == [("| Nr | Przypadek |", "| M1 | pierwszy, odsyła do P1 |")]
    assert tabele["P1"] == [("| Nr | Pytanie |", "| P1 | pytanie |")]


def test_plik_dla_przebiegu_zawiera_tylko_wskazane_wejscia():
    tekst = '```json\n{"format": "f", "wejscia": [{"id": "D1"}, {"id": "D2"}, {"id": "D3"}]}\n```'

    dane, powod = dane_dla_przebiegu(tekst, ["D3", "D1"])

    assert powod is None
    assert dane == {"format": "f", "wejscia": [{"id": "D1"}, {"id": "D3"}]}


def test_plik_dla_przebiegu_nie_powstaje_bez_poprawnego_bloku():
    assert dane_dla_przebiegu("zdanie bez bloku", ["D1"])[0] is None
    assert dane_dla_przebiegu("```json\n{nie json}\n```", ["D1"])[0] is None
    assert dane_dla_przebiegu('```json\n{"wejscia": [{"id": "D1"}]}\n```', ["D7"])[0] is None
