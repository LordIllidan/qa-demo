"""Graf „Jedno zagadnienie”: wejście ze skryptów, jedno zatrzymanie, zapis dopiero po decyzji."""

from __future__ import annotations

import pytest
from langgraph.types import Command

from agenci_langgraph.__main__ import lista_agentow, main
from agenci_langgraph.jedno_zagadnienie import ETYKIETA_PLIKU, KROK_MODELU, ZAGADNIENIA, zbuduj
from agenci_langgraph.testy.pomoc import Przebieg
from agenci_langgraph.testy.test_uruchomienie import Konsola
from agenci_langgraph.wspolne import PYTANIE_OGOLNE, BladAgenta

NOTATKI = "material/sesja/notatki-z-sesji.md"

OPCJE_TESTOWE = {
    "test-potwierdzajacy": ["--port", "8766", "--test", "test_stan_zwraca_numer_builda"],
    "test-niestabilny": ["--powtorzenia", "2"],
    "wiedza-o-produkcie": ["--pytanie", "Czy po zmianie hasła klient zostaje zalogowany?", "--wymaganie", "reset-hasla"],
    "podobne-zgloszenia": ["--opis", "Ten sam link resetu ustawia hasło drugi raz"],
}

POLECENIA = {
    "ocena-asercji": ["python narzedzia/tabela_asercji.py", "python narzedzia/wymaganie.py reset-hasla"],
    "test-potwierdzajacy": ["python narzedzia/przebieg.py --port 8766 --test test_stan_zwraca_numer_builda"],
    "test-niestabilny": ["python narzedzia/historia.py --port 8765 --powtorzenia 2"],
    "sesja-eksploracyjna": ["python narzedzia/wymaganie.py reset-hasla"],
    "przeglad-zmiany-w-testach": ["python narzedzia/zmiana_w_testach.py", "python narzedzia/wymaganie.py reset-hasla"],
    "projektowanie-przypadkow": ["python narzedzia/wymaganie.py reset-hasla",
                                 "python narzedzia/wymaganie.py filtr-zamowien"],
    "zgloszenie-z-obserwacji": ["python narzedzia/wymaganie.py reset-hasla"],
    "kandydaci-do-automatyzacji": ["python narzedzia/lista_sprawdzen.py", "python narzedzia/lista_testow.py"],
    "szkic-testu-automatycznego": ["python narzedzia/wymaganie.py reset-hasla", "python narzedzia/lista_testow.py"],
    "testy-niefunkcjonalne": ["python narzedzia/wymaganie.py reset-hasla",
                              "python narzedzia/wymaganie.py filtr-zamowien"],
    "testy-po-zmianie-wymagania": ["python narzedzia/zmiana_wymagania.py"],
    "testy-z-opisu-interfejsu": ["python narzedzia/opis_interfejsu.py", "python narzedzia/wymaganie.py reset-hasla"],
    "plan-testow-iteracji": ["python narzedzia/plan_iteracji.py"],
    "wiedza-o-produkcie": ['python narzedzia/wiedza.py "Czy po zmianie hasła klient zostaje zalogowany?"',
                           "python narzedzia/wymaganie.py reset-hasla"],
    "podobne-zgloszenia": ['python narzedzia/podobne_zgloszenia.py "Ten sam link resetu ustawia hasło drugi raz"',
                           "python narzedzia/wymaganie.py reset-hasla"],
    "przeglad-przypadkow-recznych": ["python narzedzia/przypadki_reczne.py",
                                     "python narzedzia/wymaganie.py reset-hasla"],
}


def test_wspolny_graf_obejmuje_zagadnienia_bez_wlasnego_agenta():
    numery = [z.numer for z in ZAGADNIENIA.values()]
    assert numery == ["3", "P2", "P3", "P5", "P6", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11"]
    assert set(ZAGADNIENIA) == set(POLECENIA)


def test_lista_podaje_kazde_polecenie_z_zagadnieniem(model, tmp_path):
    konsola = Konsola()

    assert main(["lista"], pytaj=konsola.pytaj, pisz=konsola.pisz, model=model, katalog_zapisu=tmp_path) == 0

    assert konsola.wiersze == lista_agentow()
    for polecenie, numery in [("zestaw", "1, 7, 8, P4"), ("zgloszenie", "2, P1"), ("karta", "4, 5, 6")]:
        assert any(w.startswith(polecenie + " ") and w.endswith(numery) for w in konsola.wiersze)
    for nazwa, zagadnienie in ZAGADNIENIA.items():
        assert any(w.startswith(nazwa + " ") and f"zagadnienie {zagadnienie.numer}. " in w for w in konsola.wiersze)
    assert model.wywolania == [] and konsola.pytania == [] and list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("nazwa", list(ZAGADNIENIA))
def test_kazde_zagadnienie_w_konsoli_od_poczatku_do_konca(nazwa, model, tmp_path, aplikacja):
    konsola = Konsola(lambda pytanie: "decyzja testera")

    kod = main([nazwa, *OPCJE_TESTOWE.get(nazwa, [])], pytaj=konsola.pytaj, pisz=konsola.pisz,
               model=model, katalog_zapisu=tmp_path)

    assert kod == 0, konsola.tekst
    kroki = [wiersz.split("]")[0] for wiersz in konsola.wiersze if wiersz.startswith("[krok ")]
    assert kroki == ["[krok wejscie", f"[krok {KROK_MODELU}", "[krok decyzja", "[krok zapis"]
    assert konsola.tekst.count("ZATRZYMANIE GRAFU: decyzja") == 1
    assert f"ZDANIE MODELU (krok {KROK_MODELU}, skill {nazwa})" in konsola.tekst
    assert konsola.pytania and PYTANIE_OGOLNE not in konsola.pytania[0], "skill ma listę decyzji człowieka"
    assert len(model.wywolania) == 1
    assert f"name: {nazwa}\n" in model.wywolania[0]["instrukcja"]
    wejscie = model.wywolania[0]["wejscie"]
    polecenia = POLECENIA[nazwa]
    for numer, polecenie in enumerate(polecenia, start=1):
        assert f"Wejście {numer} z {len(polecenia)}, polecenie: {polecenie}\n" in wejscie
    assert "=== WEJŚCIE DLA MODELU ===" in wejscie
    assert "decyzja testera" not in wejscie
    protokol = (tmp_path / f"{nazwa}.md").read_text(encoding="utf-8")
    assert f"## Krok: {KROK_MODELU} (skill {nazwa})" in protokol
    assert ": decyzja testera" in protokol
    assert protokol.endswith("\n") and not protokol.endswith("\n\n")


def test_zatrzymanie_wznowienie_i_zapis_dopiero_po_decyzji(model, tmp_path):
    graf = zbuduj(model, "zgloszenie-z-obserwacji", [("wymaganie.py", "reset-hasla")],
                  "Zgłoszenie z obserwacji o wskazanej godzinie", (NOTATKI,), tmp_path, "zastępczy")
    przebieg = Przebieg(graf)

    zatrzymanie = przebieg.do_zatrzymania({})

    assert zatrzymanie["zatrzymanie"] == "decyzja"
    assert [(p["krok"], p["skill"]) for p in zatrzymanie["pozycje"]] == [(KROK_MODELU, "zgloszenie-z-obserwacji")]
    assert przebieg.nastepny_krok == ("decyzja",)
    assert list(tmp_path.iterdir()) == [], "przed decyzją graf niczego nie zapisuje"
    wejscie = model.wywolania[0]["wejscie"]
    assert wejscie.startswith("Zadanie: Zgłoszenie z obserwacji o wskazanej godzinie\n")
    assert f"Wejście 2 z 2, polecenie: {ETYKIETA_PLIKU}: {NOTATKI}\n" in wejscie
    assert przebieg.stan["zdanie_modelu"][KROK_MODELU]["wejscie"] == ["python narzedzia/wymaganie.py reset-hasla"]

    pytania = zatrzymanie["pozycje"][0]["pytania"]
    odpowiedzi = {KROK_MODELU: {pytanie: f"odpowiedź {i}" for i, pytanie in enumerate(pytania)}}
    assert przebieg.do_zatrzymania(Command(resume=odpowiedzi)) is None

    assert przebieg.nastepny_krok == ()
    assert len(model.wywolania) == 1, "po wznowieniu model nie jest pytany drugi raz"
    assert przebieg.stan["decyzja_czlowieka"] == odpowiedzi
    assert przebieg.stan["zapisane"] == [(tmp_path / "zgloszenie-z-obserwacji.md").as_posix()]
    protokol = (tmp_path / "zgloszenie-z-obserwacji.md").read_text(encoding="utf-8")
    assert "# Protokół agenta: R2. Zgłoszenie z obserwacji ręcznej" in protokol
    assert "- prośba: Zgłoszenie z obserwacji o wskazanej godzinie" in protokol
    assert f"- {ETYKIETA_PLIKU}: `{NOTATKI}`" in protokol
    for pytanie, odpowiedz in odpowiedzi[KROK_MODELU].items():
        assert f"- {pytanie}: {odpowiedz}" in protokol


def test_agent_nie_czyta_katalogu_prowadzacego(model, tmp_path):
    konsola = Konsola(lambda pytanie: "")

    kod = main(["sesja-eksploracyjna", "--plik", "prowadzacy/odpowiedzi-pokazu.md"], pytaj=konsola.pytaj,
               pisz=konsola.pisz, model=model, katalog_zapisu=tmp_path)

    assert kod == 2
    assert konsola.wiersze[-1] == "Agent zatrzymany: agent nie czyta katalogu prowadzacy"
    assert model.wywolania == [] and list(tmp_path.iterdir()) == []
    with pytest.raises(BladAgenta, match="katalogu prowadzacy"):
        zbuduj(model, "sesja-eksploracyjna", [], pliki=("material/../prowadzacy/odpowiedzi-pokazu.md",))


def test_brak_wskazanego_pliku_zatrzymuje_agenta_przed_modelem(model, tmp_path):
    with pytest.raises(BladAgenta, match="nie ma pliku material/sesja/nie-ma-takich-notatek.md"):
        zbuduj(model, "sesja-eksploracyjna", [], pliki=("material/sesja/nie-ma-takich-notatek.md",))
    assert model.wywolania == []


def test_parametry_czlowieka_trafiaja_do_polecen_skryptow():
    class Argumenty:
        porty = [8765, 8767]
        port = 8767
        test = ["test_a", "test_b"]
        powtorzenia = None
        zmiana_wymagania = True

    a = Argumenty()
    assert ZAGADNIENIA["ocena-asercji"].polecenia(a)[0] == ("tabela_asercji.py", "--porty", 8765, 8767)
    assert ZAGADNIENIA["test-potwierdzajacy"].polecenia(a) == [
        ("przebieg.py", "--port", 8767, "--test", "test_a", "--test", "test_b")]
    assert ZAGADNIENIA["test-niestabilny"].polecenia(a) == [("historia.py", "--port", 8767)]
    assert ZAGADNIENIA["plan-testow-iteracji"].polecenia(a) == [("plan_iteracji.py",), ("zmiana_wymagania.py",)]


def test_ponowny_test_wymaga_portu_i_testu_od_czlowieka(model, tmp_path):
    with pytest.raises(SystemExit):
        main(["test-potwierdzajacy"], model=model, katalog_zapisu=tmp_path)
    assert model.wywolania == []
