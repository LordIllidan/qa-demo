# Narzędzie: lista_sprawdzen.py

Podaje zdanie o zmianie z oknem czasu i listę sprawdzeń z czasami wykonania.

- Zagadnienia: 4, R3
- Rodzaj wejścia: lista sprawdzeń z czasami
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/lista_sprawdzen.py
python narzedzia/lista_sprawdzen.py --plik material/zakres/lista-sprawdzen.json
```

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| `material/zakres/lista-sprawdzen.json` | `wyniki/lista-sprawdzen.txt` |

## Format pliku z listą

```json
{
  "format": "qa-demo/lista-sprawdzen/1",
  "zmiana": "zmiana w resecie, 40 minut",
  "wymaganie": "reset-hasla",
  "sprawdzenia": [
    {"id": "S1", "obszar": "reset hasła", "sprawdzenie": "Pierwszy link z wiadomości ustawia nowe hasło", "czas_min": 5}
  ]
}
```

## Czego nie robi

Nie układa kolejności, nie sumuje czasów, nie nadaje poziomów ryzyka i nie mówi, co mieści się w oknie. Podaje listę w kolejności z pliku.
