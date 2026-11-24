# Plik prowadzącego

Katalog `prowadzacy` zawiera jeden plik: `prowadzacy/odpowiedzi-pokazu.md`. To materiał dla osoby, która prowadzi pokaz. Zbiera zdania, które mówią wprost, co model ma w pokazie ustalić sam.

## Po co

Model pracuje w repozytorium jako agent i może czytać pliki. Gdyby dokumentacja podawała odpowiedzi, model mógłby je przepisać, zamiast wyprowadzić z wejścia: z wymagania, wyniku przebiegu albo liczb. Pokaz wyglądałby wtedy lepiej niż praca z modelem na prawdziwym projekcie.

Dlatego dokumentacja w `README.md` i w katalogu `docs` opisuje materiał neutralnie: co gdzie leży, jak to uruchomić i w jakim formacie przychodzi wejście. Tego, co z wejścia wynika, nie podaje.

## Co jest w pliku

- czym różnią się buildy,
- ręczny przykład tej różnicy w PowerShell,
- wyniki testów na buildach,
- co wynika z porównania dwóch testów z pokazu,
- opis testu, którego dotyczy zagadnienie P3,
- liczby zagadnienia 5 zestawione z progami,
- zawartość przykładowego pliku danych zagadnienia 7,
- wypełniony przykład zapisu przebiegu,
- odpowiedzi do zagadnień rozszerzających R1–R18.

## Kto czyta

| Kto | Czy czyta katalog `prowadzacy` |
| --- | --- |
| prowadzący pokaz | tak |
| uczestnik pokazu | według uznania prowadzącego, najlepiej po pokazie |
| model pracujący w repozytorium | nie |

Otwarcie pliku w PowerShell:

```powershell
Get-Content prowadzacy/odpowiedzi-pokazu.md -Encoding UTF8
```

## Jak działa zakaz dla modelu

Zakaz stoi w trzech miejscach:

1. W bloku „Zasady wspólne” każdego z dwudziestu dwóch skilli w `.github/skills`, jako zasada 10.
2. W zasadach pokazu w `README.md`, jako zasada 10.
3. W części „Wejście” każdego z trzech agentów GitHub Copilot w `.github/agents` (opis: [agenci-copilot.md](agenci-copilot.md)).

Zakaz jest instrukcją, a nie blokadą techniczną. Model, który nie załadował żadnego skilla i nie pracuje jako jeden z tych agentów, tej instrukcji nie zna. Jeśli w rozmowie nie używasz skilla ani agenta, dopisz zakaz do prośby albo nie otwieraj pliku w edytorze, w którym pracuje model.

## Czego zakaz nie obejmuje

Odpowiedzi widać także poza katalogiem `prowadzacy`, w miejscach potrzebnych do działania pokazu:

- `app/serwer.py`: kod aplikacji,
- `testy`: kod testów,
- `material`: materiał wejściowy, w tym gotowe zgłoszenie dla zagadnienia P2.

Skille każą brać wejście ze skryptów z katalogu `narzedzia`, ale czytania tych plików nie zakazują. Agenci idą krok dalej: nie czytają kodu aplikacji z katalogu `app`, a pliki z katalogu `material` czytają tylko wtedy, gdy skill bieżącego zagadnienia wskazuje je jako wejście. To także instrukcja, a nie blokada.

## Zmiana pliku

Jeśli zmienisz aplikację, testy albo materiał, popraw `prowadzacy/odpowiedzi-pokazu.md`. Nowych zdań z odpowiedziami nie dopisuj do `README.md` ani do plików w `docs`.
