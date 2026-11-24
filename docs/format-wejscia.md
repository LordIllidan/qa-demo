# Stały format wejścia

Każdy skrypt z katalogu `narzedzia` oddaje wejście dla modelu w tej samej ramce. Dzięki temu model dostaje za każdym razem tekst o znanym układzie, a człowiek może go przeczytać, zapisać i przekazać ponownie.

## Zasada

Skrypty dostarczają wejście: wymaganie, wynik przebiegu albo liczby. Niczego nie oceniają. Nie porównują odpowiedzi z oczekiwaniem, nie wskazują przyczyn, nie liczą różnic między buildami i nie podpowiadają decyzji. Wynik „zaliczony” albo „niezaliczony” pochodzi z asercji testu, a nie ze skryptu.

## Ramka tekstowa

```text
=== WEJŚCIE DLA MODELU ===
narzędzie: <nazwa skryptu>
rodzaj wejścia: <wymaganie | wynik przebiegu | liczby | ...>
utworzono: <data i godzina ze strefą>
uwaga: narzędzie podaje wejście i niczego nie ocenia

## <sekcja>
...
=== KONIEC WEJŚCIA ===
Zapisano: <pliki w katalogu wyniki>
```

Treść między znacznikami jest w Markdownie: nagłówki, wiersze `pole: wartość` i tabele.

## Pliki w katalogu wyniki

Każdy skrypt zapisuje ten sam tekst do pliku `.txt` w katalogu `wyniki`. Skrypty, które uruchamiają testy, zapisują obok plik `.json` z pełnymi danymi. Katalog `wyniki` powstaje przy pierwszym uruchomieniu i nie trafia do repozytorium.

Do rozmowy z modelem można wkleić tekst z okna albo wskazać plik z katalogu `wyniki`. Kopiowanie do schowka w PowerShell:

```powershell
Get-Content wyniki/przebieg-8766.txt -Encoding UTF8 | Set-Clipboard
```

## Polskie znaki w PowerShell

Skrypty piszą w UTF-8. W oknie PowerShell tekst wyświetla się poprawnie. Przy przekierowaniu wyjścia do pliku albo do innego polecenia Windows PowerShell 5.1 może zamienić polskie znaki. Zamiast przekierowania użyj pliku z katalogu `wyniki` albo ustaw kodowanie w bieżącym oknie:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## Wynik przebiegu w JSON

Format `qa-demo/przebieg/1`, zapisywany przez `przebieg.py` i używany w materiale nocnego przebiegu. Wartości w nawiasach ostrych opisują pole:

```text
{
  "format": "qa-demo/przebieg/1",
  "pochodzenie": "uruchomienie",
  "build": {"port": <port>, "numer": "<numer builda>"},
  "zestaw": "testy/test_reset_hasla.py",
  "start": "<data i godzina ze strefą>",
  "podsumowanie": {"liczba_testow": <liczba>, "zaliczony": <liczba>, "niezaliczony": <liczba>, "pominięty": <liczba>, "błąd": <liczba>},
  "testy": [
    {
      "nazwa": "<nazwa testu>",
      "plik": "testy/test_reset_hasla.py",
      "opis": "<docstring testu>",
      "wynik": "<zaliczony | niezaliczony | pominięty | błąd>",
      "czas_ms": <liczba>,
      "komunikat": "<komunikat wyjątku albo powód pominięcia>",
      "miejsce": "<plik>:<numer wiersza>",
      "asercja": "<treść wiersza, na którym test się zatrzymał>",
      "wymiana": [
        {"nr": 1, "zadanie": "POST /test/konto", "dane": {"email": "...", "haslo": "..."}, "status": 201, "odpowiedz": {"email": "..."}}
      ]
    }
  ]
}
```

Wypełniony przykład jest w pliku dla prowadzącego `prowadzacy/odpowiedzi-pokazu.md`.

| Pole | Znaczenie |
| --- | --- |
| `pochodzenie` | `uruchomienie` albo opis materiału przygotowanego ręcznie |
| `wynik` | `zaliczony`, `niezaliczony`, `pominięty` albo `błąd` (wyjątek przed wejściem do testu) |
| `komunikat` | komunikat wyjątku albo powód pominięcia |
| `miejsce`, `asercja` | plik z numerem wiersza i treść wiersza, na którym test się zatrzymał |
| `wymiana` | kolejne żądania wysłane przez test i odpowiedzi aplikacji |

## Kody wyjścia

| Kod | Znaczenie |
| --- | --- |
| 0 | wejście zostało przygotowane, także wtedy, gdy testy są czerwone |
| 2 | narzędzie nie przygotowało wejścia; komunikat mówi, co zrobić, na przykład uruchomić aplikację |

## Uruchamianie

Skrypty uruchamia się z katalogu głównego repozytorium. Skrypty, które rozmawiają z aplikacją, wymagają, żeby działała w drugim oknie (`python app/serwer.py`).
