# Narzędzie: pdf.py

Pobiera PDF z builda i wyciąga tytuł oraz wiersze tekstu.

- Zagadnienia: R15
- Rodzaj wejścia: tekst i metadane PDF
- Wymaga działającej aplikacji

## Użycie

```powershell
python narzedzia/pdf.py --port 8765
```

| Opcja | Znaczenie |
| --- | --- |
| `--port` | port builda |

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| `GET /test/potwierdzenie.pdf` | `wyniki/pdf-<port>.txt` |

Tytuł bierze z pola `/Title`. Wiersze bierze z napisów UTF-16 w strumieniu treści (`<FEFF…> Tj`). Plik nie osadza czcionki Unicode, więc podgląd w czytniku PDF może nie pokazać polskich znaków. Tekst dla modelu pochodzi z wyciągu, nie z renderu.

## Czego nie robi

Nie ocenia treści względem wymagania, nie liczy stron i nie renderuje układu.
