# Narzędzie: przebieg_ui.py

Uruchamia krótki przebieg strony resetu hasła w Playwright i podaje kroki, selektory i tekst ze strony.

- Zagadnienia: R12
- Rodzaj wejścia: wynik przebiegu interfejsu
- Wymaga działającej aplikacji i przeglądarki Playwright

## Użycie

```powershell
python -m pip install playwright
python -m playwright install chromium
python narzedzia/przebieg_ui.py --port 8765
```

| Opcja | Znaczenie |
| --- | --- |
| `--port` | port builda |

Pakiet `playwright` jest w `requirements.txt`. Przeglądarkę doinstalowuje osobne polecenie powyżej. Bez niej skrypt kończy pracę kodem wyjścia 2.

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| stronę `http://127.0.0.1:<port>/` przez Playwright | `wyniki/przebieg-ui-<port>.txt` |

Przebieg: otwarcie strony, wpisanie `anna@example.com`, kliknięcie „Wyślij link”, odczyt tekstu z elementu o roli status.

## Czego nie robi

Nie ocenia przebiegu, nie czyta surowego logu Playwrighta i nie zapisuje zrzutu ekranu.
