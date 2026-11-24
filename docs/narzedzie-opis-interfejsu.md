# Narzędzie: opis_interfejsu.py

Podaje opis interfejsu w formacie OpenAPI jako tabelę operacji, pól żądania i odpowiedzi.

- Zagadnienia: R7
- Rodzaj wejścia: opis interfejsu
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/opis_interfejsu.py
python narzedzia/opis_interfejsu.py --plik material/interfejs/reset-hasla.json
```

| Opcja | Znaczenie |
| --- | --- |
| `--plik` | plik z opisem interfejsu w JSON; domyślnie `material/interfejs/reset-hasla.json` |

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| plik z opisem interfejsu | `wyniki/opis-interfejsu.txt` |

Skrypt czyta część `paths` i schematy z `components.schemas`. Odwołania `$ref` rozwija tylko do schematów z `components.schemas`.

## Co podaje

1. Tytuł, wersję i opis z części `info`.
2. Tabelę operacji: metoda i ścieżka, nazwa, pola żądania z typem, informacją, czy pole jest wymagane, i ograniczeniami, parametry nagłówka albo adresu.
3. Tabelę odpowiedzi: operacja, kod, opis i pola odpowiedzi.

Plik bez części `paths` kończy pracę kodem wyjścia 2.

## Czego nie robi

Nie porównuje opisu z wymaganiem ani z aplikacją i nie wysyła żądań.
