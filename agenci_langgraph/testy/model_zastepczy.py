"""Model zastępczy do testów przepływu grafów. Nie potrzebuje klucza ani sieci.

Niczego nie ocenia i nie zawiera gotowych odpowiedzi: oddaje niewypełniony
szablon wyniku wycięty ze skilla, który dostał jako instrukcję. Dzięki temu
odpowiedź ma te same części i tabele co odpowiedź prawdziwego modelu, a testy
sprawdzają kroki, zatrzymanie i wznowienie grafu, a nie treść zdania.
"""

from __future__ import annotations

import re

from langchain_core.messages import AIMessage

MIEJSCE_NA_PLIK = "<dane w formacie pliku"


def blok(instrukcja: str, jezyk: str) -> str | None:
    znaleziony = re.search(rf"```{jezyk}\s*\n(.*?)\n```", instrukcja, flags=re.DOTALL)
    return znaleziony.group(1) if znaleziony else None


def szablon_ze_skilla(instrukcja: str) -> str:
    szablon = blok(instrukcja, "markdown")
    if szablon is None:
        return "Model zastępczy: w instrukcji nie ma szablonu wyniku."
    plik = blok(instrukcja, "json")
    if plik is None:
        return szablon
    wstawka = f"```json\n{plik}\n```"
    wiersze = [wstawka if wiersz.startswith(MIEJSCE_NA_PLIK) else wiersz for wiersz in szablon.splitlines()]
    return "\n".join(wiersze)


class ModelZastepczy:
    """Ma tę samą metodę invoke co model czatu z LangChain i zapisuje, co dostał."""

    def __init__(self) -> None:
        self.wywolania: list = []

    def invoke(self, wiadomosci: list) -> AIMessage:
        instrukcja, wejscie = (wiadomosc.content for wiadomosc in wiadomosci)
        self.wywolania.append({"instrukcja": instrukcja, "wejscie": wejscie})
        return AIMessage(content=szablon_ze_skilla(instrukcja))
