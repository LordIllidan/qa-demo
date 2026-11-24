"""Graf „Od czerwonego przebiegu do zgłoszenia”: dwa zatrzymania i droga zależna od decyzji człowieka."""

from __future__ import annotations

import pytest
from langgraph.types import Command

from agenci_langgraph.od_przebiegu_do_zgloszenia import (
    KROK_DECYZJI_O_SZKICU,
    PLIK_PROTOKOLU,
    pytanie_o_szkic,
    zbuduj,
)
from agenci_langgraph.testy.pomoc import Przebieg, bez_odpowiedzi

PYTANIE_O_SZKIC = pytanie_o_szkic(8766, 8765)
POLECENIA_SZKICU = [
    "python narzedzia/przebieg.py --port 8766",
    "python narzedzia/przebieg.py --port 8765",
    "python narzedzia/wymaganie.py reset-hasla",
]


def test_pierwsze_zatrzymanie_pokazuje_klasyfikacje_i_pyta_o_dalszy_krok(model, tmp_path):
    przebieg = Przebieg(zbuduj(model, katalog_zapisu=tmp_path))

    zatrzymanie = przebieg.do_zatrzymania({})

    assert zatrzymanie["zatrzymanie"] == KROK_DECYZJI_O_SZKICU
    klasyfikacja, dalszy_krok = zatrzymanie["pozycje"]
    assert (klasyfikacja["krok"], klasyfikacja["skill"]) == ("klasyfikacja", "klasyfikacja-awarii")
    assert klasyfikacja["pytania"]
    assert dalszy_krok == {
        "krok": KROK_DECYZJI_O_SZKICU, "skill": None, "zdanie_modelu": None, "pytania": [PYTANIE_O_SZKIC],
    }
    assert list(przebieg.stan["wejscie"]) == ["python narzedzia/przebieg_nocny.py"]
    assert "narzędzie: przebieg_nocny.py" in model.wywolania[0]["wejscie"]
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("odpowiedz", ["nie", "", "może później"])
def test_bez_slowa_tak_graf_nie_uruchamia_przebiegow_i_nie_prosi_o_szkic(model, tmp_path, odpowiedz):
    przebieg = Przebieg(zbuduj(model, katalog_zapisu=tmp_path))
    zatrzymanie = przebieg.do_zatrzymania({})
    decyzja = bez_odpowiedzi(zatrzymanie)
    decyzja["klasyfikacja"][zatrzymanie["pozycje"][0]["pytania"][0]] = "produkt, zgłoszenie"
    decyzja[KROK_DECYZJI_O_SZKICU][PYTANIE_O_SZKIC] = odpowiedz

    assert przebieg.do_zatrzymania(Command(resume=decyzja)) is None

    stan = przebieg.stan
    assert przebieg.nastepny_krok == ()
    assert len(model.wywolania) == 1
    assert list(stan["wejscie"]) == ["python narzedzia/przebieg_nocny.py"]
    assert list(stan["zdanie_modelu"]) == ["klasyfikacja"]
    protokol = (tmp_path / PLIK_PROTOKOLU).read_text(encoding="utf-8")
    assert "## Krok: klasyfikacja (skill klasyfikacja-awarii)" in protokol
    assert "produkt, zgłoszenie" in protokol
    assert f"- {PYTANIE_O_SZKIC}: {odpowiedz or 'bez odpowiedzi'}" in protokol
    assert "## Krok: szkic" not in protokol


def test_po_slowie_tak_graf_bierze_przebiegi_i_zatrzymuje_sie_na_decyzji_o_zgloszeniu(model, tmp_path, aplikacja):
    przebieg = Przebieg(zbuduj(model, katalog_zapisu=tmp_path))
    pierwsze = przebieg.do_zatrzymania({})
    decyzja = bez_odpowiedzi(pierwsze)
    decyzja[KROK_DECYZJI_O_SZKICU][PYTANIE_O_SZKIC] = "Tak"

    drugie = przebieg.do_zatrzymania(Command(resume=decyzja))

    assert drugie["zatrzymanie"] == "decyzja_zgloszenie"
    assert [(p["krok"], p["skill"]) for p in drugie["pozycje"]] == [("szkic", "zgloszenie-defektu")]
    assert przebieg.nastepny_krok == ("decyzja_zgloszenie",)
    assert list(tmp_path.iterdir()) == [], "przed decyzją o zgłoszeniu graf niczego nie zapisuje"
    stan = przebieg.stan
    assert stan["zdanie_modelu"]["szkic"]["wejscie"] == POLECENIA_SZKICU
    assert len(model.wywolania) == 2
    wejscie_szkicu = model.wywolania[1]["wejscie"]
    assert wejscie_szkicu.count("=== WEJŚCIE DLA MODELU ===") == 3
    for numer, polecenie in enumerate(POLECENIA_SZKICU, start=1):
        assert f"Wejście {numer} z 3, polecenie: {polecenie}\n" in wejscie_szkicu
        assert stan["wejscie"][polecenie].rstrip() in wejscie_szkicu
    for port in aplikacja:
        assert f"(port {port})" in stan["wejscie"][f"python narzedzia/przebieg.py --port {port}"]

    decyzja_o_zgloszeniu = {"szkic": {pytanie: f"odpowiedź {numer}"
                                      for numer, pytanie in enumerate(drugie["pozycje"][0]["pytania"], start=1)}}
    assert przebieg.do_zatrzymania(Command(resume=decyzja_o_zgloszeniu)) is None

    assert przebieg.nastepny_krok == ()
    assert len(model.wywolania) == 2
    assert przebieg.stan["decyzja_czlowieka"]["szkic"] == decyzja_o_zgloszeniu["szkic"]
    protokol = (tmp_path / PLIK_PROTOKOLU).read_text(encoding="utf-8")
    kolejnosc = [protokol.index(fragment) for fragment in (
        "## Krok: klasyfikacja (skill klasyfikacja-awarii)",
        f"- {PYTANIE_O_SZKIC}: Tak",
        "## Krok: szkic (skill zgloszenie-defektu)",
    )]
    assert kolejnosc == sorted(kolejnosc)
    for pytanie, odpowiedz in decyzja_o_zgloszeniu["szkic"].items():
        assert f"- {pytanie}: {odpowiedz}" in protokol
    assert protokol.endswith("\n")


def test_porty_buildow_mozna_wskazac(model, tmp_path, aplikacja):
    przebieg = Przebieg(zbuduj(model, port=8765, port_odniesienia=8766, katalog_zapisu=tmp_path))
    pierwsze = przebieg.do_zatrzymania({})
    pytanie = pytanie_o_szkic(8765, 8766)
    assert pierwsze["pozycje"][-1]["pytania"] == [pytanie]
    decyzja = bez_odpowiedzi(pierwsze)
    decyzja[KROK_DECYZJI_O_SZKICU][pytanie] = "tak"

    przebieg.do_zatrzymania(Command(resume=decyzja))

    assert przebieg.stan["zdanie_modelu"]["szkic"]["wejscie"] == [
        "python narzedzia/przebieg.py --port 8765",
        "python narzedzia/przebieg.py --port 8766",
        "python narzedzia/wymaganie.py reset-hasla",
    ]
