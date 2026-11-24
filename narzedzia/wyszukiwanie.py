"""Lokalne wyszukiwanie fragmentów tekstu dla skryptów wiedza.py i podobne_zgloszenia.py.

Wyszukiwanie jest leksykalne: BM25 na rdzeniach słów. Rdzeń to pierwsze
pięć liter słowa po zamianie na małe litery i usunięciu polskich znaków,
co w przybliżeniu łączy odmiany tego samego słowa („hasło”, „hasła”,
„haseł” mają rdzeń „hasl”, „hasel” osobno). Wynik mówi, ile wspólnych słów
ma fragment z zapytaniem, a nie, czy fragment odpowiada na pytanie.
Działa bez sieci, bez klucza i bez dodatkowych pakietów.
"""

from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from wspolne import KATALOG, BladNarzedzia, czytaj_tekst, wzgledna

DLUGOSC_RDZENIA = 5
K1 = 1.5
B = 0.75
OPIS_METODY = (
    f"BM25 (k1={K1}, b={B}) na rdzeniach słów: pierwsze {DLUGOSC_RDZENIA} liter, małe litery, "
    "bez polskich znaków, bez słów pomijanych; wynik mówi o wspólnych słowach z zapytaniem, "
    "a nie o tym, czy fragment odpowiada na pytanie"
)
PROWADZACY = KATALOG / "prowadzacy"

SLOWA_POMIJANE = {
    "ale", "albo", "ani", "bez", "być", "był", "była", "było", "były", "będzie", "czy", "dla", "do", "gdy",
    "jak", "jaki", "jaka", "jakie", "jest", "jeśli", "już", "lub", "ma", "mają", "może", "na", "nad", "nie",
    "niż", "od", "oraz", "po", "pod", "przez", "przy", "się", "są", "tak", "też", "to", "tylko", "tym", "w",
    "we", "z", "za", "ze", "że", "co", "kto", "który", "która", "które", "których", "tego", "ten", "ta",
    "te", "ich", "jego", "jej", "o", "i", "a", "u",
}
ZAMIANY = str.maketrans({"ł": "l", "Ł": "l"})


@dataclass
class Fragment:
    zrodlo: str
    sekcja: str
    tekst: str
    opis_dokumentu: list = field(default_factory=list)


def bez_znakow(slowo: str) -> str:
    rozlozone = unicodedata.normalize("NFKD", slowo.translate(ZAMIANY))
    return "".join(znak for znak in rozlozone if not unicodedata.combining(znak))


def rdzenie(tekst: str) -> list:
    slowa = re.findall(r"\w+", tekst.lower())
    return [bez_znakow(s)[:DLUGOSC_RDZENIA] for s in slowa if s not in SLOWA_POMIJANE and not s.isdigit() and len(s) > 1]


def sprawdz_katalog(sciezka: Path) -> Path:
    sciezka = sciezka.resolve()
    if sciezka == PROWADZACY.resolve() or PROWADZACY.resolve() in sciezka.parents:
        raise BladNarzedzia("narzędzie nie przeszukuje katalogu prowadzacy")
    return sciezka


def fragmenty_markdown(plik: Path) -> list:
    """Dzieli dokument Markdown na fragmenty po nagłówkach drugiego poziomu."""
    wiersze = czytaj_tekst(plik).splitlines()
    tytul = next((w[2:].strip() for w in wiersze if w.startswith("# ")), plik.stem)
    opis, fragmenty, sekcja, tresc = [], [], None, []
    for wiersz in wiersze:
        if wiersz.startswith("## "):
            if sekcja is not None:
                fragmenty.append((sekcja, tresc))
            sekcja, tresc = wiersz[3:].strip(), []
        elif sekcja is None:
            if wiersz.startswith("- "):
                opis.append(wiersz[2:].strip())
        else:
            tresc.append(wiersz)
    if sekcja is not None:
        fragmenty.append((sekcja, tresc))
    zrodlo = wzgledna(plik)
    return [Fragment(zrodlo, f"{tytul} / {s}", "\n".join(t).strip(), opis) for s, t in fragmenty if "\n".join(t).strip()]


def szukaj(zapytanie: str, fragmenty: list, ile: int) -> list:
    """Zwraca najwyżej `ile` par (wynik, wspólne rdzenie, fragment) z wynikiem większym od zera."""
    pytanie = set(rdzenie(zapytanie))
    if not pytanie:
        raise BladNarzedzia("zapytanie nie ma słów, po których da się szukać")
    dokumenty = [rdzenie(f.sekcja + "\n" + f.tekst) for f in fragmenty]
    if not dokumenty:
        return []
    srednia = sum(map(len, dokumenty)) / len(dokumenty)
    ile_z_rdzeniem = {r: sum(1 for d in dokumenty if r in d) for r in pytanie}
    wyniki = []
    for fragment, dokument in zip(fragmenty, dokumenty):
        wynik, wspolne = 0.0, []
        for rdzen in sorted(pytanie):
            czestosc = dokument.count(rdzen)
            if not czestosc:
                continue
            wspolne.append(rdzen)
            idf = math.log(1 + (len(dokumenty) - ile_z_rdzeniem[rdzen] + 0.5) / (ile_z_rdzeniem[rdzen] + 0.5))
            wynik += idf * czestosc * (K1 + 1) / (czestosc + K1 * (1 - B + B * len(dokument) / srednia))
        if wynik > 0:
            wyniki.append((round(wynik, 2), wspolne, fragment))
    wyniki.sort(key=lambda w: -w[0])
    return wyniki[:ile]
