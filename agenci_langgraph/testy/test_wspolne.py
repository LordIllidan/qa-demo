"""Części wspólne: wejście ze skryptów, skille, rozmowa z modelem, lista decyzji."""

from __future__ import annotations

import pytest

from agenci_langgraph.wspolne import (
    PYTANIE_OGOLNE,
    RAMA,
    BladAgenta,
    opis_polecenia,
    pytania_do_czlowieka,
    wczytaj_skill,
    wejscie_ze_skryptu,
    zapytaj_model,
)

WYMAGANIE = ("wymaganie.py", "reset-hasla")


def test_wejscie_pochodzi_ze_skryptu_w_stalej_ramce():
    wejscie = wejscie_ze_skryptu(WYMAGANIE)

    assert wejscie.startswith("=== WEJŚCIE DLA MODELU ===")
    assert "narzędzie: wymaganie.py" in wejscie
    assert "=== KONIEC WEJŚCIA ===" in wejscie


def test_polecenie_ma_postac_wpisywana_w_konsoli():
    assert opis_polecenia(("przebieg.py", "--port", 8765)) == "python narzedzia/przebieg.py --port 8765"


def test_skrypt_ktory_nie_przygotowal_wejscia_zatrzymuje_agenta():
    with pytest.raises(BladAgenta, match="nie przygotowało wejścia"):
        wejscie_ze_skryptu(("wymaganie.py", "nie-ma-takiego-wymagania"))


def test_brak_skryptu_zatrzymuje_agenta():
    with pytest.raises(BladAgenta, match="nie ma skryptu"):
        wejscie_ze_skryptu(("nie_ma_takiego_skryptu.py",))


def test_brak_skilla_zatrzymuje_agenta():
    with pytest.raises(BladAgenta, match="nie ma skilla"):
        wczytaj_skill("nie-ma-takiego-skilla")


def test_model_dostaje_skill_jako_instrukcje_i_wynik_skryptu_jako_wejscie(model):
    wejscie = wejscie_ze_skryptu(WYMAGANIE)

    zdanie = zapytaj_model(model, "luki-w-wymaganiu", {opis_polecenia(WYMAGANIE): wejscie})

    wywolanie = model.wywolania[0]
    assert wywolanie["instrukcja"] == RAMA + "\n\n" + wczytaj_skill("luki-w-wymaganiu")
    assert wywolanie["wejscie"] == f"Wejście 1 z 1, polecenie: {opis_polecenia(WYMAGANIE)}\n\n{wejscie.rstrip()}"
    assert "Zdanie modelu" in zdanie and "Decyzja człowieka" in zdanie


def test_blad_modelu_zatrzymuje_agenta():
    class ModelBezPolaczenia:
        def invoke(self, wiadomosci):
            raise ConnectionError("brak sieci")

    with pytest.raises(BladAgenta, match="model nie odpowiedział"):
        zapytaj_model(ModelBezPolaczenia(), "luki-w-wymaganiu", {"polecenie": "wejście"})


def test_pusta_odpowiedz_modelu_zatrzymuje_agenta():
    class ModelMilczacy:
        def invoke(self, wiadomosci):
            return ""

    with pytest.raises(BladAgenta, match="pustą odpowiedź"):
        zapytaj_model(ModelMilczacy(), "luki-w-wymaganiu", {"polecenie": "wejście"})


def test_lista_decyzji_pochodzi_z_czesci_decyzja_czlowieka():
    zdanie = "\n".join([
        "# Tytuł",
        "## Zdanie modelu",
        "- [ ] to nie jest decyzja, bo stoi w zdaniu modelu",
        "## Decyzja człowieka",
        "",
        "- [ ] Pierwsza decyzja:",
        "- [ ] Druga decyzja (z dopiskiem):",
        "- [ ] Pierwsza decyzja:",
    ])

    assert pytania_do_czlowieka(zdanie) == ["Pierwsza decyzja", "Druga decyzja (z dopiskiem)", "Pierwsza decyzja (2)"]


def test_gdy_model_nie_wypisal_decyzji_graf_pyta_ogolnie():
    assert pytania_do_czlowieka("Zdanie bez części z decyzjami.") == [PYTANIE_OGOLNE]
