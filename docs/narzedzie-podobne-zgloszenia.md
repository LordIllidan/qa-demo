# Narzędzie: podobne_zgloszenia.py

Wyszukuje zgłoszenia podobne do opisu, który tester chce zgłosić, w otwartych zgłoszeniach i w archiwum.

- Zagadnienia: R10
- Rodzaj wejścia: podobne zgłoszenia
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/podobne_zgloszenia.py "Ten sam link resetu ustawia hasło drugi raz"
python narzedzia/podobne_zgloszenia.py "<opis>" --ile 3
```

| Opcja | Znaczenie |
| --- | --- |
| opis | opis zachowania, w cudzysłowie |
| `--ile` | najwyżej tyle zgłoszeń; domyślnie 5 |

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| `material/zgloszenia/otwarte.json` i plik treści zgłoszenia, gdy lista go podaje | `wyniki/podobne-zgloszenia.txt` |
| `material/zgloszenia/archiwum.json` | |

Każde zgłoszenie jest jednym fragmentem: identyfikator i tytuł, stan, build, a dla archiwum także obszar i rozwiązanie. Treść to plik zgłoszenia albo opis z archiwum. Gdy lista otwartych podaje tylko tytuł, skrypt tak to zapisuje.

## Jak wyszukuje

Tak samo jak `wiedza.py`: BM25 na rdzeniach słów, opis w [narzedzie-wiedza.md](narzedzie-wiedza.md). Wysoki wynik znaczy wspólne słowa z opisem, a nie to, że zgłoszenie opisuje to samo zachowanie.

Opis bez słów, po których da się szukać, kończy pracę kodem wyjścia 2.

## Czego nie robi

Nie rozstrzyga, czy opis jest powtórzeniem, regresją albo nowym defektem. Nie zmienia zgłoszeń.
