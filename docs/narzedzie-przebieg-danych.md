# Narzędzie: przebieg_danych.py

Wysyła do builda dane z pliku i podaje odpowiedzi obok oczekiwań zapisanych w pliku.

- Zagadnienia: 7
- Rodzaj wejścia: wynik przebiegu
- Wymaga działającej aplikacji

## Użycie

```powershell
python narzedzia/przebieg_danych.py --port 8765
python narzedzia/przebieg_danych.py --port 8766 --dane material/dane/dane-resetu.json
```

| Opcja | Znaczenie |
| --- | --- |
| `--port` | port builda; wymagana |
| `--dane` | plik z danymi; domyślnie `material/dane/dane-resetu.json` |

## Jak działa

Skrypt zakłada nowe konto i wysyła wejścia z pliku jedno po drugim, w kolejności z pliku, do operacji `POST /reset/potwierdz`. Dla każdego wejścia zapisuje kod i treść odpowiedzi.

## Format pliku z danymi

```json
{
  "format": "qa-demo/dane/1",
  "wymaganie": "reset-hasla",
  "operacja": "POST /reset/potwierdz",
  "wejscia": [
    {
      "id": "D1",
      "opis": "pierwszy link",
      "token": "{nowy-link}",
      "haslo": "NoweHaslo-1",
      "oczekiwany_status": 200,
      "zrodlo": "zdanie z wymagania, R3: „Użytkownik, który otworzy link, ustawia nowe hasło.”"
    }
  ]
}
```

| Pole | Znaczenie |
| --- | --- |
| `token` | `{nowy-link}`: skrypt prosi o reset i wstawia token z nowej wiadomości; `{ten-sam-link}`: token z poprzedniego `{nowy-link}`; każda inna wartość, także pusta, jest wysyłana dosłownie |
| `haslo` | hasło wysyłane w żądaniu |
| `oczekiwany_status` | oczekiwany kod odpowiedzi albo `null`, gdy wymaganie go nie podaje |
| `pytanie` | pytanie do autora wymagania, gdy `oczekiwany_status` ma wartość `null` |
| `zrodlo` | skąd pochodzi oczekiwany wynik: zdanie z wymagania z cytatem albo reguła własna modelu |

Plik `material/dane/dane-resetu.json` jest przykładem. W pokazie tabelę wejść układa model, a do pliku trafiają wejścia wybrane przez człowieka.

## Co zapisuje

`wyniki/przebieg-danych-<port>.txt` i `wyniki/przebieg-danych-<port>.json`.

## Czego nie robi

Nie porównuje odpowiedzi z oczekiwaniem i nie stawia przy wejściu oceny. Oczekiwany status i status odpowiedzi stoją w sąsiednich kolumnach, a różnicę ma zauważyć model.
