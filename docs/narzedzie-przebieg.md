# Narzędzie: przebieg.py

Uruchamia testy na buildzie pod wskazanym portem i podaje wynik przebiegu.

- Zagadnienia: 2, 3, 6, P2, R4, R18
- Rodzaj wejścia: wynik przebiegu
- Wymaga działającej aplikacji

## Użycie

```powershell
python narzedzia/przebieg.py --port 8765
python narzedzia/przebieg.py --port 8766
python narzedzia/przebieg.py --port 8767 --test test_link_dziala_jeden_raz
```

| Opcja | Znaczenie |
| --- | --- |
| `--port` | port builda; wymagana |
| `--test` | nazwa testu z zestawu; można powtórzyć, żeby uruchomić kilka testów |
| `--zestaw` | plik albo katalog z testami; domyślnie `testy/test_reset_hasla.py` |

Domyślny zestaw ma pięć testów. Ich wyniki na buildach pokazu są w pliku dla prowadzącego `prowadzacy/odpowiedzi-pokazu.md`.

## Co zapisuje

| Plik | Zawartość |
| --- | --- |
| `wyniki/przebieg-<port>.txt` | tekst w stałej ramce |
| `wyniki/przebieg-<port>.json` | ten sam przebieg w formacie `qa-demo/przebieg/1` |

Kolejne uruchomienie na tym samym porcie nadpisuje oba pliki, także wtedy, gdy opcja `--test` zawęziła zestaw. Skrypt `zbierz_wyniki.py` bierze z tych plików ostatni zapisany przebieg każdego portu.

Dla każdego testu skrypt podaje opis, wynik, czas, a przy wyniku innym niż zaliczony także komunikat i wiersz, na którym test się zatrzymał. Każdy test ma zapis wymiany żądań i odpowiedzi z aplikacją. Opis formatu: `docs/format-wejscia.md`.

## Czego nie robi

Nie ponawia testów, nie interpretuje wyniku i nie wskazuje przyczyny. Czerwony test nie jest błędem narzędzia: skrypt kończy się kodem 0, gdy wynik został zapisany.
