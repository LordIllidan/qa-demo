# Narzędzie: wymaganie.py

Podaje tekst wymagania w stałej ramce.

- Zagadnienia: 1, 2, 3, 4, 7, 8, P4, P5, P6, R1, R2, R4, R5
- Rodzaj wejścia: wymaganie
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/wymaganie.py reset-hasla
python narzedzia/wymaganie.py filtr-zamowien
```

Bez nazwy albo z nieznaną nazwą skrypt wypisuje dostępne wymagania i kończy się kodem 2.

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| `material/wymagania/<nazwa>.md` | `wyniki/wymaganie-<nazwa>.txt` |

Nowe wymaganie dodaje się jako kolejny plik `.md` w katalogu `material/wymagania`. Nazwa pliku bez rozszerzenia jest nazwą wymagania.

## Czego nie robi

Nie skraca tekstu, nie numeruje zdań i niczego do wymagania nie dopisuje. Oddaje plik w takiej postaci, w jakiej jest zapisany.
