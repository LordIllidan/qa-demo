# Narzędzie: liczby.py

Podaje liczby dwóch buildów z gotowych plików wyników, zestawione obok siebie.

- Zagadnienia: 5
- Rodzaj wejścia: liczby
- Aplikacja nie musi działać

## Użycie

```powershell
python narzedzia/liczby.py
python narzedzia/liczby.py --pliki material/liczby/build-8765.json material/liczby/build-8766.json
```

Opcja `--pliki` przyjmuje dwa pliki w kolejności: wcześniejszy build, późniejszy build.

## Co podaje

1. Listę plików z informacją o pochodzeniu liczb.
2. Profil obciążenia obu buildów, parametr po parametrze.
3. Dla każdej ścieżki progi i metryki obu buildów: liczbę żądań, medianę, średnią, p95, maksimum i odsetek błędów.

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| `material/liczby/build-8765.json`, `material/liczby/build-8766.json` | `wyniki/liczby.txt` |

## Format pliku z liczbami

```json
{
  "format": "qa-demo/liczby/1",
  "pochodzenie": "gotowy plik wyników; narzędzia pokazu niczego nie mierzą",
  "build": {"port": 8765, "numer": "1.4.0"},
  "profil": {"uzytkownicy": 20, "narastanie_s": 30, "czas_trwania_s": 300, "przerwa_miedzy_zadaniami_s": 1.0},
  "progi": {"orders": {"p95_ms_ponizej": 500, "bledy_proc_ponizej": 1.0}},
  "sciezki": {"orders": {"liczba_zadan": 2742, "mediana_ms": 31.6, "srednia_ms": 33.2, "p95_ms": 42.1, "max_ms": 96.4, "bledy_proc": 0.0}}
}
```

## Czego nie robi

Niczego nie mierzy i nie uruchamia żadnego obciążenia. Nie liczy różnic, nie sprawdza zgodności profilu i nie mówi, czy próg jest przekroczony. Progów nie zmienia.
