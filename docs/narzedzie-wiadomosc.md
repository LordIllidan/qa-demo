# Narzędzie: wiadomosc.py

Prosi build o reset hasła i podaje nagłówki oraz treść wiadomości ze skrzynki testowej.

- Zagadnienia: R14
- Rodzaj wejścia: wiadomość przychodząca
- Wymaga działającej aplikacji

## Użycie

```powershell
python narzedzia/wiadomosc.py --port 8765
python narzedzia/wiadomosc.py --port 8765 --email anna@example.com
```

| Opcja | Znaczenie |
| --- | --- |
| `--port` | port builda |
| `--email` | adres skrzynki; domyślnie `anna@example.com` |

## Co czyta i co zapisuje

| Czyta | Zapisuje |
| --- | --- |
| `POST /reset/zamow`, potem `GET /test/skrzynka` | `wyniki/wiadomosc-<port>.txt` |

Podaje nadawcę, odbiorcę, temat, link, token i treść. Czeka na wiadomość do dwóch sekund.

## Czego nie robi

Nie ocenia nadawcy, treści, linku ani tokenu i nie otwiera linku.
