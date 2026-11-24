# Agenci GitHub Copilot dla testerów

Trzech niestandardowych agentów GitHub Copilot. Każdy obsługuje grupę zagadnień i przy każdym zagadnieniu stosuje odpowiedni skill z katalogu `.github/skills`. Agent nie zastępuje skilla: wybiera go, pilnuje źródła wejścia i zasad wspólnych oraz zatrzymuje się przed decyzją człowieka.

## Gdzie leżą i w jakim formacie

Agenci leżą w katalogu `.github/agents`. Z tego miejsca GitHub Copilot ładuje agentów repozytorium (dokumentacja: [Creating custom agents for Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents), [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)).

```text
.github/agents/
├── analiza-wymagania.agent.md
├── analiza-przebiegu.agent.md
└── zakres-i-wydanie.agent.md
```

Każdy agent to plik Markdown z rozszerzeniem `.agent.md` i nagłówkiem YAML. Nazwa pliku może zawierać tylko litery `a-z` i `A-Z`, cyfry, kropkę, łącznik i podkreślenie. Nazwa pliku bez `.agent.md` jest identyfikatorem agenta.

| Pole nagłówka | Czy użyte | Reguły |
| --- | --- | --- |
| `name` | tak | nazwa wyświetlana; pole opcjonalne, bez niego nazwą jest nazwa pliku |
| `description` | tak | pole wymagane; co agent robi i kiedy go użyć |
| `tools` | tak | lista narzędzi dostępnych agentowi; bez tego pola agent ma wszystkie narzędzia |
| `target`, `model`, `mcp-servers` i pozostałe | nie | bez `target` agent jest dostępny i w VS Code, i w GitHub Copilot; model wybiera użytkownik |

Treść pod nagłówkiem to instrukcja agenta. Limit wynosi 30 000 znaków. Najdłuższa z trzech instrukcji ma około 6 800 znaków.

## Lista agentów

| Agent | Plik | Zagadnienia | Co robi |
| --- | --- | --- | --- |
| Analiza wymagania | `analiza-wymagania.agent.md` | 1, 7, 8, P4, P5, R1, R4, R5, R6, R7 | Pracuje z tekstem wymagania: pytania do autora, dane pod regułę, przypadki uprawnień, pokrycie wymagania testami, karta i raport sesji eksploracyjnej, przypadki testowe techniką, szkic testu automatycznego, testy niefunkcjonalne, testy po zmianie wymagania, testy z opisu interfejsu. |
| Analiza przebiegu | `analiza-przebiegu.agent.md` | 2, 3, P1, P2, P3, P6, R2 | Pracuje z wynikiem przebiegu albo z obserwacją testera: zgłoszenie defektu, ocena asercji, klasyfikacja awarii, ponowny test po poprawce, test niestabilny, przegląd zmiany w testach, zgłoszenie z obserwacji ręcznej. |
| Zakres i wydanie | `zakres-i-wydanie.agent.md` | 4, 5, 6, R3, R8 | Przygotowuje informację przed wydaniem: zakres po zmianie, zdanie o liczbach dwóch buildów, karta przed wgraniem. Zestawia też sprawdzenia ręczne z testami automatycznymi przed wyborem tego, co automatyzować, i układa szkic planu testów iteracji. |

Razem agenci obsługują wszystkie dwadzieścia dwa zagadnienia, czyli czternaście zagadnień pokazu i osiem rozszerzających, każde dokładnie raz. Opis zagadnień jest w `README.md`. Podział zagadnień na pracę testera manualnego i automatyzującego opisuje [role-testerow.md](role-testerow.md).

| Zagadnienie | Skill | Agent |
| --- | --- | --- |
| 1. Luki w wymaganiu | `luki-w-wymaganiu` | Analiza wymagania |
| 2. Defekt z czerwonego przebiegu | `zgloszenie-defektu` | Analiza przebiegu |
| 3. Ocena asercji | `ocena-asercji` | Analiza przebiegu |
| 4. Zakres po zmianie | `zakres-po-zmianie` | Zakres i wydanie |
| 5. Zdanie o dwóch buildach | `dwa-buildy-w-liczbach` | Zakres i wydanie |
| 6. Karta przed wgraniem | `karta-przed-wgraniem` | Zakres i wydanie |
| 7. Dane pod regułę | `dane-pod-regule` | Analiza wymagania |
| 8. Uprawnienia przy zwykłej historyjce | `przypadki-uprawnien` | Analiza wymagania |
| P1. Czerwony przebieg: produkt, test czy środowisko | `klasyfikacja-awarii` | Analiza przebiegu |
| P2. Ponowny test po poprawce | `test-potwierdzajacy` | Analiza przebiegu |
| P3. Test niestabilny | `test-niestabilny` | Analiza przebiegu |
| P4. Pokrycie wymagania testami | `pokrycie-wymagania` | Analiza wymagania |
| P5. Karta sesji eksploracyjnej | `sesja-eksploracyjna` | Analiza wymagania |
| P6. Przegląd zmiany w testach | `przeglad-zmiany-w-testach` | Analiza przebiegu |
| R1. Przypadki testowe techniką | `projektowanie-przypadkow` | Analiza wymagania |
| R2. Zgłoszenie z obserwacji ręcznej | `zgloszenie-z-obserwacji` | Analiza przebiegu |
| R3. Kandydaci do automatyzacji | `kandydaci-do-automatyzacji` | Zakres i wydanie |
| R4. Szkic testu automatycznego | `szkic-testu-automatycznego` | Analiza wymagania |
| R5. Testy niefunkcjonalne | `testy-niefunkcjonalne` | Analiza wymagania |
| R6. Testy po zmianie wymagania | `testy-po-zmianie-wymagania` | Analiza wymagania |
| R7. Testy z opisu interfejsu | `testy-z-opisu-interfejsu` | Analiza wymagania |
| R8. Plan testów iteracji | `plan-testow-iteracji` | Zakres i wydanie |

## Budowa agenta

Każdy plik agenta ma te same części:

1. Wstęp: w jakiej pracy agent pomaga i kto podejmuje decyzję.
2. **Zagadnienia i skille**: tabela, która prośbę testera przypisuje do zagadnienia i do pliku skilla. Pod tabelą stoi, które prośby obsługuje inny agent.
3. **Jak pracujesz**: pięć kroków. Agent ustala zagadnienie, czyta w całości plik skilla, pobiera wejście, oddaje wynik w formacie skilla i czeka na decyzję.
4. **Wejście**: których skryptów z katalogu `narzedzia` agent używa i czego nie czyta.
5. **Zasady, których pilnujesz zawsze**: skrót zasad wspólnych ważnych dla tej grupy zagadnień.
6. **Co wolno ci zapisać** albo **Czego nie zmieniasz**: granice zmian w plikach.

Agent nie powtarza treści skilli. Kroki pracy, format wyniku i zakazy właściwe dla zagadnienia są tylko w pliku `SKILL.md`. Agent każe ten plik przeczytać przy każdej prośbie. Działa to wszędzie tam, gdzie agent ma narzędzie do czytania plików, i nie zależy od tego, czy dana powierzchnia Copilota sama ładuje skille.

## Skąd agent bierze wejście

Jedynym źródłem wejścia są skrypty z katalogu `narzedzia` i pliki, które skill bieżącego zagadnienia wskazuje jako wejście. Format wejścia opisuje [format-wejscia.md](format-wejscia.md).

| Agent | Skrypty |
| --- | --- |
| Analiza wymagania | `wymaganie.py`, `lista_testow.py`, `zmiana_wymagania.py`, `opis_interfejsu.py`, po decyzji człowieka `przebieg_danych.py` i `przebieg.py` |
| Analiza przebiegu | `przebieg.py`, `tabela_asercji.py`, `przebieg_nocny.py`, `historia.py`, `zmiana_w_testach.py`, `wymaganie.py` |
| Zakres i wydanie | `lista_sprawdzen.py`, `liczby.py`, `zbierz_wyniki.py`, `lista_testow.py`, `plan_iteracji.py`, `zmiana_wymagania.py`, `wymaganie.py`, na polecenie człowieka `przebieg.py` |

Każdy agent ma zapisane, że:

- nie czyta katalogu `prowadzacy` (opis: [plik-prowadzacego.md](plik-prowadzacego.md)),
- nie czyta kodu aplikacji z katalogu `app`,
- pliki z katalogu `material` czyta tylko wtedy, gdy skill bieżącego zagadnienia wskazuje je jako wejście,
- przy kodzie wyjścia 2 przekazuje komunikat skryptu i czeka, a brakującego wejścia nie zastępuje domysłem.

## Narzędzia agentów

| Agent | `tools` | Dlaczego |
| --- | --- | --- |
| Analiza wymagania | `read`, `search`, `execute`, `edit` | `edit` jest potrzebne w trzech sytuacjach, każdej po decyzji człowieka: zapis pliku danych w katalogu `wyniki` (zagadnienie 7), dopisanie wskazanych przypadków do zestawu testów (zagadnienie 1) i zapis przyjętego kodu testu w nowym pliku w katalogu `testy` (zagadnienie R4) |
| Analiza przebiegu | `read`, `search`, `execute` | agent niczego nie zmienia; brak `edit` wzmacnia zasadę „nie obcinasz asercji” |
| Zakres i wydanie | `read`, `search`, `execute` | agent niczego nie zmienia; brak `edit` wzmacnia zasadę „nie ruszasz progów” |

`read`, `search`, `execute` i `edit` to aliasy narzędzi z dokumentacji GitHuba. `execute` oznacza powłokę właściwą dla systemu, na Windows PowerShell.

## Zasady, które trzyma każdy agent

| Zasada | Jak jest zapisana w agencie |
| --- | --- |
| widać osobno zdanie modelu i decyzję człowieka | wynik w formacie skilla, pól decyzji agent nie wypełnia, po wyniku czeka |
| zdanie z wymagania albo reguła własna modelu | etykieta przy każdym oczekiwaniu; zdanie z wymagania wymaga numeru i dosłownego cytatu |
| gdy wymaganie milczy, pytanie | pytanie do autora w miejscu oczekiwanego wyniku, bez wymyślonej polityki |
| nie obcina asercji i nie rusza progów | zakaz osłabiania bramek, także jako propozycji |
| nie mówi „wgrywamy” | zakaz słowa „wgrywamy” i jego zaprzeczenia w każdej formie |
| mówi, czego nie sprawdził | brak informacji nazwany wprost |
| nie czyta katalogu `prowadzacy` | zakaz w części „Wejście” |

Pełne brzmienie zasad jest w bloku „Zasady wspólne” każdego skilla (opis: [skille.md](skille.md)). Agent powtarza je w skrócie po to, żeby obowiązywały także w krótkiej odpowiedzi poza formatem skilla.

## Jak użyć

Wymagania wstępne są takie same jak dla skryptów: środowisko z `README.md`, a przy zagadnieniach 2, 3, 6, 7, P2, P3 i P6 oraz przy uruchomieniu testu w zagadnieniu R4 aplikacja uruchomiona w osobnym oknie PowerShell:

```powershell
python app/serwer.py
```

### Visual Studio Code

1. Otwórz katalog repozytorium w VS Code.
2. Otwórz okno czatu Copilota i z listy agentów wybierz „Analiza wymagania”, „Analiza przebiegu” albo „Zakres i wydanie”.
3. Napisz prośbę. Agent sam uruchomi polecenie w terminalu; VS Code zapyta o zgodę według własnych ustawień.

### GitHub Copilot CLI

Wybór agenta w trybie interaktywnym, z katalogu repozytorium:

```powershell
copilot
```

Potem `/agent` i wybór z listy.

Wybór agenta w poleceniu:

```powershell
copilot --agent analiza-wymagania --prompt "Przejrzyj wymaganie resetu hasła i wypisz pytania do autora."
copilot --agent analiza-przebiegu --prompt "Przygotuj zgłoszenie defektu z czerwonego przebiegu."
copilot --agent zakres-i-wydanie --prompt "Zbierz wyniki w kartę dla osoby, która decyduje o wydaniu."
```

Wartość opcji `--agent` to identyfikator, czyli nazwa pliku bez `.agent.md`.

### GitHub.com

Agenci z gałęzi domyślnej są widoczni na liście agentów na stronie [github.com/copilot/agents](https://github.com/copilot/agents) po wybraniu repozytorium. Agent pracuje tam w środowisku GitHuba, w którym nie ma drugiego okna z aplikacją. Zagadnienia, które wymagają działającej aplikacji, skończą się tam kodem wyjścia 2 i komunikatem skryptu. Do pokazu służą VS Code i Copilot CLI.

## Ograniczenia

- Zakazy w pliku agenta są instrukcją, a nie blokadą techniczną. Model może ich nie posłuchać. Dlatego wynik zawsze czyta człowiek.
- Lista `tools` ogranicza narzędzia, ale agent z `execute` może zmienić plik poleceniem w terminalu. Agentom zakazuje tego instrukcja.
- W Copilot CLI lista `tools` może zostać uzupełniona o narzędzia domyślne. Ścisłe ograniczenie daje tam pole `strict-tools-list: true`, opisane tylko w dokumentacji CLI. Agenci tego pola nie mają.
- Agenci nie używają pola `skills` w nagłówku. Opisuje je tylko dokumentacja VS Code, a dokumentacja GitHuba i Copilot CLI go nie wymienia. Zamiast tego agent czyta plik skilla wskazany w tabeli.
- Agenci nie przekazują pracy między sobą. Prośbę spoza swoich zagadnień agent odsyła do właściwego agenta, a wyboru dokonuje człowiek.

## Zmiana agentów

- Nowe zagadnienie: dodaj skill w `.github/skills`, a potem wiersz w tabeli „Zagadnienia i skille” właściwego agenta i w tabelach tego pliku.
- Zmiana sposobu pracy przy zagadnieniu: zmień skill. Pliku agenta nie trzeba ruszać.
- Zmiana zasad wspólnych: zmień blok w dwudziestu dwóch skillach i skrót w trzech agentach.
- Po zmianie sprawdź, że nagłówek YAML się wczytuje i że każda ścieżka skilla z tabeli istnieje.
