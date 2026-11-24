"""Graf „Dwa buildy i karta”: trzy zatrzymania i wcześniejsze kroki trzymane w stanie grafu."""

from __future__ import annotations

from langgraph.types import Command

from agenci_langgraph.dwa_buildy_i_karta import PLIK_PROTOKOLU, zbuduj
from agenci_langgraph.testy.pomoc import Przebieg

ZBIOR = "python narzedzia/zbierz_wyniki.py --porty 8765 8766"


def odpowiedz_na_wszystko(zatrzymanie: dict, tekst: str) -> dict:
    return {pozycja["krok"]: {pytanie: tekst for pytanie in pozycja["pytania"]} for pozycja in zatrzymanie["pozycje"]}


def test_graf_zatrzymuje_sie_trzy_razy_i_po_kazdej_decyzji_idzie_dalej(model, tmp_path, aplikacja):
    przebieg = Przebieg(zbuduj(model, tmp_path))

    zakres = przebieg.do_zatrzymania({})

    assert zakres["zatrzymanie"] == "decyzja_zakres"
    assert [(p["krok"], p["skill"]) for p in zakres["pozycje"]] == [("zakres", "zakres-po-zmianie")]
    assert "wczesniejsze_decyzje" not in zakres
    assert przebieg.nastepny_krok == ("decyzja_zakres",)
    assert len(model.wywolania) == 1
    assert przebieg.stan["zdanie_modelu"]["zakres"]["wejscie"] == [
        "python narzedzia/lista_sprawdzen.py", "python narzedzia/wymaganie.py reset-hasla",
    ]

    liczby = przebieg.do_zatrzymania(Command(resume=odpowiedz_na_wszystko(zakres, "decyzja o zakresie")))

    assert liczby["zatrzymanie"] == "decyzja_liczby"
    assert [(p["krok"], p["skill"]) for p in liczby["pozycje"]] == [("liczby", "dwa-buildy-w-liczbach")]
    assert len(model.wywolania) == 2
    assert przebieg.stan["zdanie_modelu"]["liczby"]["wejscie"] == ["python narzedzia/liczby.py"]
    assert "narzędzie: liczby.py" in model.wywolania[1]["wejscie"]

    wydanie = przebieg.do_zatrzymania(Command(resume=odpowiedz_na_wszystko(liczby, "decyzja o liczbach")))

    assert wydanie["zatrzymanie"] == "decyzja_wydanie"
    assert [(p["krok"], p["skill"]) for p in wydanie["pozycje"]] == [("karta", "karta-przed-wgraniem")]
    assert wydanie["wczesniejsze_decyzje"] == {
        "zakres": odpowiedz_na_wszystko(zakres, "decyzja o zakresie")["zakres"],
        "liczby": odpowiedz_na_wszystko(liczby, "decyzja o liczbach")["liczby"],
    }
    stan = przebieg.stan
    assert list(stan["zdanie_modelu"]) == ["zakres", "liczby", "karta"]
    for port in aplikacja:
        assert f"python narzedzia/przebieg.py --port {port}" in stan["wejscie"]
        assert f"wyniki/przebieg-{port}.json" in stan["wejscie"][ZBIOR]
        assert f"brak pliku wyniki/przebieg-{port}.json" not in stan["wejscie"][ZBIOR]
    assert stan["zdanie_modelu"]["karta"]["wejscie"] == [ZBIOR]
    assert len(model.wywolania) == 3
    wejscie_karty = model.wywolania[2]["wejscie"]
    assert wejscie_karty == f"Wejście 1 z 1, polecenie: {ZBIOR}\n\n{stan['wejscie'][ZBIOR].rstrip()}"
    assert "decyzja o zakresie" not in wejscie_karty and "decyzja o liczbach" not in wejscie_karty
    assert list(tmp_path.iterdir()) == [], "przed ostatnią decyzją graf niczego nie zapisuje"

    assert przebieg.do_zatrzymania(Command(resume=odpowiedz_na_wszystko(wydanie, "decyzja o wydaniu"))) is None

    assert przebieg.nastepny_krok == ()
    assert len(model.wywolania) == 3
    protokol = (tmp_path / PLIK_PROTOKOLU).read_text(encoding="utf-8")
    for krok, skill, decyzja in [
        ("zakres", "zakres-po-zmianie", "decyzja o zakresie"),
        ("liczby", "dwa-buildy-w-liczbach", "decyzja o liczbach"),
        ("karta", "karta-przed-wgraniem", "decyzja o wydaniu"),
    ]:
        assert f"## Krok: {krok} (skill {skill})" in protokol
        assert f": {decyzja}" in protokol
    assert protokol.count("### Zdanie modelu") == protokol.count("### Decyzja człowieka") == 3
    assert protokol.endswith("\n")
