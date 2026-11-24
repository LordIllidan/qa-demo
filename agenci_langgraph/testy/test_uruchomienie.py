"""Uruchomienie z konsoli: rozmowa z człowiekiem przy zatrzymaniu i model ze zmiennych środowiskowych."""

from __future__ import annotations

import pytest

from agenci_langgraph.__main__ import main
from agenci_langgraph.model import ZMIENNA_DOSTAWCY, ZMIENNA_NAZWY, model_ze_srodowiska, opis_modelu
from agenci_langgraph.od_wymagania_do_zestawu import PLIK_PROTOKOLU, PLIK_ZESTAWU
from agenci_langgraph.wspolne import BladAgenta


class Konsola:
    """Zastępuje okno PowerShell: zbiera to, co agent wypisał, i podaje odpowiedzi człowieka."""

    def __init__(self, odpowiedzi=None) -> None:
        self.wiersze: list = []
        self.pytania: list = []
        self.odpowiedzi = odpowiedzi

    def pisz(self, tekst: str = "") -> None:
        self.wiersze.append(tekst)

    def pytaj(self, pytanie: str) -> str:
        self.pytania.append(pytanie)
        if self.odpowiedzi is None:
            raise EOFError
        return self.odpowiedzi(pytanie)

    @property
    def tekst(self) -> str:
        return "\n".join(self.wiersze)


def test_agent_zestaw_w_konsoli_od_poczatku_do_konca(model, tmp_path):
    konsola = Konsola(lambda pytanie: "M1" if "zestawu testów" in pytanie else "")

    kod = main(["zestaw"], pytaj=konsola.pytaj, pisz=konsola.pisz, model=model, katalog_zapisu=tmp_path)

    assert kod == 0
    kroki = [wiersz.split("]")[0] for wiersz in konsola.wiersze if wiersz.startswith("[krok ")]
    assert kroki == ["[krok wejscie", "[krok luki", "[krok uprawnienia_reset", "[krok uprawnienia_filtr",
                     "[krok pokrycie", "[krok dane", "[krok decyzja", "[krok zapis"]
    assert konsola.tekst.count("ZATRZYMANIE GRAFU: decyzja") == 1
    assert konsola.tekst.count("ZDANIE MODELU (krok ") == konsola.tekst.count("DECYZJA CZŁOWIEKA (krok ") == 5
    assert konsola.tekst.index("ZDANIE MODELU (krok luki") < konsola.tekst.index("DECYZJA CZŁOWIEKA (krok luki")
    assert konsola.tekst.index("ZATRZYMANIE GRAFU") < konsola.tekst.index("[krok decyzja]")
    assert len(konsola.pytania) >= 5
    zestaw = (tmp_path / PLIK_ZESTAWU).read_text(encoding="utf-8")
    assert "Odpowiedź człowieka: M1" in zestaw and "| M1 |" in zestaw
    assert (tmp_path / PLIK_PROTOKOLU).is_file()


def test_bez_odpowiedzi_czlowieka_agent_niczego_nie_zapisuje(model, tmp_path):
    konsola = Konsola()

    kod = main(["zestaw"], pytaj=konsola.pytaj, pisz=konsola.pisz, model=model, katalog_zapisu=tmp_path)

    assert kod == 2
    assert konsola.wiersze[-1].startswith("Agent zatrzymany: nie ma odpowiedzi człowieka")
    assert list(tmp_path.iterdir()) == []


def test_bez_zmiennych_srodowiskowych_agent_mowi_jak_ustawic_model(monkeypatch, tmp_path):
    monkeypatch.delenv(ZMIENNA_DOSTAWCY, raising=False)
    monkeypatch.delenv(ZMIENNA_NAZWY, raising=False)
    konsola = Konsola()

    kod = main(["zestaw"], pytaj=konsola.pytaj, pisz=konsola.pisz, katalog_zapisu=tmp_path)

    assert kod == 2
    assert ZMIENNA_DOSTAWCY in konsola.tekst and ZMIENNA_NAZWY in konsola.tekst
    assert konsola.pytania == [] and list(tmp_path.iterdir()) == []


def test_model_bierze_dostawce_i_nazwe_ze_zmiennych_srodowiskowych(monkeypatch):
    monkeypatch.setenv(ZMIENNA_DOSTAWCY, "openai")
    monkeypatch.setenv(ZMIENNA_NAZWY, "nazwa-modelu")
    monkeypatch.setenv("OPENAI_API_KEY", "klucz-tylko-do-testu-bez-polaczenia")

    model = model_ze_srodowiska()

    assert opis_modelu() == "openai/nazwa-modelu"
    assert type(model).__name__ == "ChatOpenAI"
    assert model.model_name == "nazwa-modelu"


def test_nieznany_dostawca_zatrzymuje_agenta(monkeypatch):
    monkeypatch.setenv(ZMIENNA_DOSTAWCY, "nie-ma-takiego-dostawcy")
    monkeypatch.setenv(ZMIENNA_NAZWY, "nazwa-modelu")

    with pytest.raises(BladAgenta, match="nie udało się przygotować modelu"):
        model_ze_srodowiska()
