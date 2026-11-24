# qa-demo

Zestaw pokazowy dla testerów i QA Engineerów: jak używać modelu AI w codziennej pracy testera tak, żeby model formułował zdanie, a decyzja zostawała przy człowieku.

Repozytorium zawiera pierwszy etap zestawu: materiał pokazu, narzędzia i skrypty oraz zbiór skilli GitHub Copilot. Agentów GitHub Copilot i agentów LangGraph w tym etapie nie ma.

## Co tu jest

| Katalog | Zawartość | Opis |
| --- | --- | --- |
| `app` | aplikacja demonstracyjna z resetem hasła w trzech buildach | [docs/aplikacja.md](docs/aplikacja.md) |
| `testy` | testy pytest, w tym „link działa jeden raz” i „wystarczy kod 200” | [docs/testy.md](docs/testy.md) |
| `material` | wymagania, lista sprawdzeń, liczby dwóch buildów, zgłoszenia, nocny przebieg, notatki z sesji, zmiana w testach | [docs/material.md](docs/material.md) |
| `narzedzia` | skrypty, które podają modelowi wejście w stałym formacie | [docs/format-wejscia.md](docs/format-wejscia.md) |
| `.github/skills` | czternaście skilli dla testerów | [docs/skille.md](docs/skille.md) |
| `prowadzacy` | odpowiedzi pokazu dla prowadzącego; modele tego katalogu nie czytają | [docs/plik-prowadzacego.md](docs/plik-prowadzacego.md) |
| `docs` | dokumentacja, jeden plik na funkcję | |

## Zasady pokazu

1. Narzędzia tylko dostarczają wejście: wymaganie, wynik przebiegu albo liczby. Ocenę formułuje model.
2. Za każdym razem widać osobno zdanie modelu i decyzję człowieka.
3. Model oznacza źródło każdej pozycji: zdanie z wymagania albo reguła własna modelu.
4. Gdy wymaganie czegoś nie mówi, model pisze pytanie. Nie wymyśla polityki.
5. Do zestawu testów wchodzi tylko to, co człowiek potwierdzi.
6. Model opisuje zachowanie systemu („na tym buildzie koszyk przyjmuje zamówienie bez adresu dostawy”), a nie stan testu („test padł”).
7. Model nie osłabia bramek: nie obcina asercji, nie rusza progów, nie wyrzuca przypadku, żeby zmieścić się w czasie.
8. Model nie podejmuje decyzji o wydaniu. Słowa „wgrywamy” w jego wyniku nie ma.
9. Model mówi także, czego nie sprawdził i czego nie ruszał.
10. Model nie czyta katalogu `prowadzacy`, w którym leżą odpowiedzi pokazu dla prowadzącego.

## Szybki start

Potrzebny jest Python 3.10 albo nowszy. Polecenia są w składni PowerShell.

```powershell
git clone https://github.com/LordIllidan/qa-demo.git
cd qa-demo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Jeśli PowerShell odmówi uruchomienia skryptu aktywacji, wykonaj w tym samym oknie `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` i powtórz aktywację.

Pierwsze okno PowerShell, aplikacja we wszystkich buildach:

```powershell
python app/serwer.py
```

Drugie okno PowerShell, przebieg na obu buildach:

```powershell
.\.venv\Scripts\Activate.ps1
python narzedzia/przebieg.py --port 8765
python narzedzia/przebieg.py --port 8766
```

Każde polecenie wypisuje wynik przebiegu w stałej ramce i zapisuje go w katalogu `wyniki`.

## Buildy

| Port | Build | Rola w pokazie |
| --- | --- | --- |
| 8765 | 1.4.0 | wcześniejszy build, używany jako odniesienie |
| 8766 | 1.5.0 | nowszy build |
| 8767 | 1.5.1 | build dostarczony do ponownego testu po zgłoszeniu ZGL-101 (zagadnienie P2) |

Czym buildy się różnią, ma w pokazie ustalić model na podstawie wejścia. Opis dla prowadzącego leży w pliku `prowadzacy/odpowiedzi-pokazu.md`.

## Zagadnienia

Każde zagadnienie ma skill i polecenia, które podają wejście. Skille leżą w `.github/skills/<nazwa>/SKILL.md`.

| Nr | Zagadnienie | Skill | Wejście |
| --- | --- | --- | --- |
| 1 | Luki w wymaganiu | `luki-w-wymaganiu` | `python narzedzia/wymaganie.py reset-hasla` |
| 2 | Defekt z czerwonego przebiegu | `zgloszenie-defektu` | `python narzedzia/przebieg.py --port 8766`, `python narzedzia/przebieg.py --port 8765`, wymaganie |
| 3 | Ocena asercji | `ocena-asercji` | `python narzedzia/tabela_asercji.py`, wymaganie |
| 4 | Zakres po zmianie | `zakres-po-zmianie` | `python narzedzia/lista_sprawdzen.py`, wymaganie |
| 5 | Zdanie o dwóch buildach | `dwa-buildy-w-liczbach` | `python narzedzia/liczby.py` |
| 6 | Karta przed wgraniem | `karta-przed-wgraniem` | `python narzedzia/zbierz_wyniki.py` |
| 7 | Dane pod regułę | `dane-pod-regule` | wymaganie, potem `python narzedzia/przebieg_danych.py --port 8766` |
| 8 | Uprawnienia przy zwykłej historyjce | `przypadki-uprawnien` | `python narzedzia/wymaganie.py reset-hasla`, `python narzedzia/wymaganie.py filtr-zamowien` |
| P1 | Czerwony przebieg: produkt, test czy środowisko | `klasyfikacja-awarii` | `python narzedzia/przebieg_nocny.py` |
| P2 | Ponowny test po poprawce | `test-potwierdzajacy` | `material/zgloszenia/ZGL-101.md`, `python narzedzia/przebieg.py --port 8767 --test test_link_dziala_jeden_raz` |
| P3 | Test niestabilny | `test-niestabilny` | `python narzedzia/historia.py --port 8765` |
| P4 | Pokrycie wymagania testami | `pokrycie-wymagania` | wymaganie, `python narzedzia/lista_testow.py` |
| P5 | Karta sesji eksploracyjnej | `sesja-eksploracyjna` | wymaganie, `material/sesja/ryzyka.md`, `material/sesja/notatki-z-sesji.md` |
| P6 | Przegląd zmiany w testach | `przeglad-zmiany-w-testach` | `python narzedzia/zmiana_w_testach.py`, wymaganie |

„Wymaganie” w tabeli oznacza polecenie `python narzedzia/wymaganie.py reset-hasla`.

Wariant 20-minutowy to zagadnienia 1, 2 i 5. Pokazują trzy rodzaje wejścia: wymaganie, wynik przebiegu i liczby.

## Narzędzia

Każdy skrypt wypisuje wejście w stałej ramce i zapisuje je w katalogu `wyniki`. Żaden niczego nie ocenia.

| Skrypt | Co podaje | Opis |
| --- | --- | --- |
| `narzedzia/wymaganie.py` | tekst wymagania | [docs/narzedzie-wymaganie.md](docs/narzedzie-wymaganie.md) |
| `narzedzia/przebieg.py` | wynik testów na buildzie pod wskazanym portem | [docs/narzedzie-przebieg.md](docs/narzedzie-przebieg.md) |
| `narzedzia/tabela_asercji.py` | kod dwóch testów i tabelę ich wyników na dwóch buildach | [docs/narzedzie-tabela-asercji.md](docs/narzedzie-tabela-asercji.md) |
| `narzedzia/lista_sprawdzen.py` | zdanie o zmianie i listę sprawdzeń z czasami | [docs/narzedzie-lista-sprawdzen.md](docs/narzedzie-lista-sprawdzen.md) |
| `narzedzia/liczby.py` | liczby dwóch buildów z gotowych plików | [docs/narzedzie-liczby.md](docs/narzedzie-liczby.md) |
| `narzedzia/zbierz_wyniki.py` | przebiegi, liczby, zgłoszenia i zakres w jednym pliku | [docs/narzedzie-zbierz-wyniki.md](docs/narzedzie-zbierz-wyniki.md) |
| `narzedzia/przebieg_danych.py` | odpowiedzi builda na dane z pliku obok oczekiwań z pliku | [docs/narzedzie-przebieg-danych.md](docs/narzedzie-przebieg-danych.md) |
| `narzedzia/przebieg_nocny.py` | zapisany nocny przebieg, przebieg referencyjny i log | [docs/narzedzie-przebieg-nocny.md](docs/narzedzie-przebieg-nocny.md) |
| `narzedzia/historia.py` | historię wielu przebiegów tego samego zestawu na jednym buildzie | [docs/narzedzie-historia.md](docs/narzedzie-historia.md) |
| `narzedzia/lista_testow.py` | listę testów z opisami | [docs/narzedzie-lista-testow.md](docs/narzedzie-lista-testow.md) |
| `narzedzia/zmiana_w_testach.py` | różnicę wersji testów i wyniki przed zmianą oraz po niej | [docs/narzedzie-zmiana-w-testach.md](docs/narzedzie-zmiana-w-testach.md) |

`narzedzia/wspolne.py` to moduł wspólny skryptów: ramka, zapis plików, uruchamianie pytest.

## Struktura katalogów

```text
qa-demo/
├── .github/skills/            czternaście katalogów, w każdym SKILL.md
├── app/serwer.py              aplikacja demonstracyjna, porty 8765, 8766 i 8767
├── docs/                      dokumentacja
├── material/
│   ├── wymagania/             reset-hasla.md, filtr-zamowien.md
│   ├── zakres/                lista-sprawdzen.json, zakres-wydania.json
│   ├── liczby/                build-8765.json, build-8766.json
│   ├── dane/                  dane-resetu.json
│   ├── zgloszenia/            ZGL-101.md, otwarte.json
│   ├── przebieg-nocny/        wynik-8766.json, wynik-8765.json, log-8766.txt
│   ├── sesja/                 ryzyka.md, notatki-z-sesji.md
│   └── zmiana-w-testach/      test_reset_hasla.py, opis-zmiany.md
├── narzedzia/                 jedenaście skryptów i wspolne.py
├── prowadzacy/                odpowiedzi-pokazu.md, plik dla prowadzącego
├── testy/                     conftest.py, test_reset_hasla.py, test_wiadomosc_resetu.py
├── pytest.ini
└── requirements.txt
```

Katalog `wyniki` powstaje przy pierwszym uruchomieniu skryptu i nie trafia do repozytorium.
