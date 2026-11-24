# Narzędzie: wiedza.py

Wyszukuje w bazie wiedzy o produkcie fragmenty do pytania testera i wypisuje je dosłownie, każdy ze źródłem.

- Zagadnienia: R9
- Rodzaj wejścia: fragmenty bazy wiedzy
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/wiedza.py "Czy po zmianie hasła klient zostaje zalogowany?"
python narzedzia/wiedza.py "<pytanie>" --ile 3 --katalog material/wiedza
```

| Opcja | Znaczenie |
| --- | --- |
| pytanie | pytanie testera, w cudzysłowie |
| `--ile` | najwyżej tyle fragmentów; domyślnie 5 |
| `--katalog` | katalog z dokumentami `.md`; domyślnie `material/wiedza` |

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| dokumenty `.md` ze wskazanego katalogu | `wyniki/wiedza.txt` |

Każdy dokument dzieli na fragmenty po nagłówkach drugiego poziomu. Nad fragmentem stoi plik, sekcja i opis dokumentu z wierszy pod tytułem: rodzaj, właściciel, data aktualizacji.

## Jak wyszukuje

Wyszukiwanie jest lokalne, w module `narzedzia/wyszukiwanie.py`. Nie używa sieci, klucza ani dodatkowych pakietów.

1. Tekst pytania i tekst fragmentu zamienia na słowa. Pomija słowa pospolite (na przykład „czy”, „po”, „z”) i liczby.
2. Ze słowa bierze rdzeń: pierwsze pięć liter, małe litery, bez polskich znaków. Dzięki temu „hasło”, „hasła” i „haseł” trafiają do jednego rdzenia.
3. Liczy wynik BM25 (k1 = 1.5, b = 0.75). Fragment bez wspólnego rdzenia z pytaniem odpada. Zostaje najwyżej tyle fragmentów, ile podaje `--ile`, od najwyższego wyniku.

Wynik mówi, ile wspólnych słów ma fragment z pytaniem. Nie mówi, czy fragment odpowiada na pytanie. Pytanie zadane innymi słowami może nie trafić we właściwy fragment.

Katalog `prowadzacy` skrypt odmawia przeszukiwać. Pytanie bez słów, po których da się szukać, i katalog bez dokumentów `.md` kończą pracę kodem wyjścia 2.

## Czego nie robi

Nie odpowiada na pytanie, nie wybiera fragmentu „właściwego” i nie ocenia, czy dokumenty są ze sobą zgodne.
