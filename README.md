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

Czternaście zagadnień: osiem podstawowych (1–8) i sześć dodatkowych (P1–P6). Każde zaczyna się od sytuacji z dnia testera i ma ten sam układ opisu: co model dostaje, co oddaje, czego sam nie robi i jaka decyzja zostaje przy człowieku. Każde ma też skill w `.github/skills/<nazwa>/SKILL.md` i polecenia, które podają wejście.

Opisy mówią, co model robi i z czego. Nie mówią, co w pokazie wychodzi: to ma ustalić model na podstawie wejścia.

| Nr | Zagadnienie | Skill | Wariant 20 min |
| --- | --- | --- | --- |
| 1 | [Luki w wymaganiu](#1-luki-w-wymaganiu) | `luki-w-wymaganiu` | tak |
| 2 | [Defekt z czerwonego przebiegu](#2-defekt-z-czerwonego-przebiegu) | `zgloszenie-defektu` | tak |
| 3 | [Ocena asercji](#3-ocena-asercji) | `ocena-asercji` | – |
| 4 | [Zakres po zmianie](#4-zakres-po-zmianie) | `zakres-po-zmianie` | – |
| 5 | [Zdanie o dwóch buildach](#5-zdanie-o-dwóch-buildach) | `dwa-buildy-w-liczbach` | tak |
| 6 | [Karta przed wgraniem](#6-karta-przed-wgraniem) | `karta-przed-wgraniem` | – |
| 7 | [Dane pod regułę](#7-dane-pod-regułę) | `dane-pod-regule` | – |
| 8 | [Uprawnienia przy zwykłej historyjce](#8-uprawnienia-przy-zwykłej-historyjce) | `przypadki-uprawnien` | – |
| P1 | [Czerwony przebieg: produkt, test czy środowisko](#p1-czerwony-przebieg-produkt-test-czy-środowisko) | `klasyfikacja-awarii` | – |
| P2 | [Ponowny test po poprawce](#p2-ponowny-test-po-poprawce) | `test-potwierdzajacy` | – |
| P3 | [Test niestabilny](#p3-test-niestabilny) | `test-niestabilny` | – |
| P4 | [Pokrycie wymagania testami](#p4-pokrycie-wymagania-testami) | `pokrycie-wymagania` | – |
| P5 | [Karta sesji eksploracyjnej](#p5-karta-sesji-eksploracyjnej) | `sesja-eksploracyjna` | – |
| P6 | [Przegląd zmiany w testach](#p6-przegląd-zmiany-w-testach) | `przeglad-zmiany-w-testach` | – |

Wariant 20-minutowy to zagadnienia 1, 2 i 5. Pokazują trzy rodzaje wejścia: wymaganie, wynik przebiegu i liczby.

Polecenia ze skryptami `przebieg.py`, `tabela_asercji.py`, `przebieg_danych.py`, `historia.py` i `zmiana_w_testach.py` wymagają aplikacji działającej w drugim oknie PowerShell (`python app/serwer.py`). Pozostałe skrypty czytają pliki i aplikacji nie potrzebują.

### 1. Luki w wymaganiu

Wariant 20-minutowy: tak.

- **Sytuacja.** Przed implementacją tester czyta historyjkę i szuka w niej niejednoznaczności, pominięć i zdań, których nie da się sprawdzić. Zwykle kończy z listą pytań do autora.
- **Model dostaje.** Tekst wymagania resetu hasła.
- **Model oddaje.** Dwie listy: pytania do autora i przypadki testowe, które sam dopisał. Każda pozycja ma źródło: zdanie z wymagania z dosłownym cytatem albo reguła własna modelu.
- **Czego model nie robi.** Nie odpowiada na własne pytania w imieniu autora i nie wpisuje „rozsądnych domyślnych” wartości. Nie podaje dopisanej reguły jako wymagania. Niczego nie dodaje do zestawu testów.
- **Decyzja człowieka.** Które pytania idą do autora i które dopisane przypadki wchodzą do zestawu.
- **Skill.** `luki-w-wymaganiu`
- **Skrypt.** `narzedzia/wymaganie.py`

```powershell
python narzedzia/wymaganie.py reset-hasla
```

### 2. Defekt z czerwonego przebiegu

Wariant 20-minutowy: tak.

- **Sytuacja.** Po przebiegu test jest czerwony. Zgłoszenie przeczyta ktoś, kto przebiegu nie widział, więc musi z niego zrozumieć, co system zrobił, co miał zrobić i jak to powtórzyć.
- **Model dostaje.** Wyniki tego samego zestawu testów na dwóch buildach, razem z wymianą żądań i odpowiedzi z aplikacją, oraz wymaganie.
- **Model oddaje.** Szkic zgłoszenia: kroki do ręcznego powtórzenia, wynik faktyczny, wynik oczekiwany z cytatem wymagania, zdanie porównujące oba buildy, dowody, fakty pomocne przy ocenie dotkliwości i to, czego nie sprawdził. Zgłoszenie opisuje zachowanie systemu, a nie to, że test padł.
- **Czego model nie robi.** Nie wysyła zgłoszenia i nie zakłada go w żadnym systemie. Nie nadaje dotkliwości ani priorytetu. Nie podaje domysłu o przyczynie w kodzie jako faktu. Nie zmienia testu ani oczekiwanego wyniku.
- **Decyzja człowieka.** Czy to defekt, jaka dotkliwość i priorytet, czy zgłoszenie wychodzi i do kogo.
- **Skill.** `zgloszenie-defektu`
- **Skrypty.** `narzedzia/przebieg.py`, `narzedzia/wymaganie.py`

```powershell
python narzedzia/przebieg.py --port 8765
python narzedzia/przebieg.py --port 8766
python narzedzia/wymaganie.py reset-hasla
```

### 3. Ocena asercji

- **Sytuacja.** Zielony test jest wart tyle, ile jego asercja. Zanim zespół zacznie polegać na teście jako na bramce, tester sprawdza, czy ten test wykryłby znany defekt.
- **Model dostaje.** Kod dwóch testów („link działa jeden raz” i „wystarczy kod 200”), tabelę ich wyników na dwóch buildach, wymianę żądań i odpowiedzi z każdego uruchomienia oraz wymaganie.
- **Model oddaje.** Jedno zdanie o tym, który z testów nadaje się na bramkę, z uzasadnieniem w wynikach. Pod nim tabelę: co sprawdzają asercje każdego testu, którego zdania wymagania dotyczą i jaki wynik dały na każdym buildzie.
- **Czego model nie robi.** Nie zmienia kodu testów: nie obcina, nie dopisuje i nie łagodzi asercji. Nie usuwa i nie wyłącza słabszego testu. Nie wyprowadza oczekiwanego wyniku z tego, co robi aplikacja.
- **Decyzja człowieka.** Który test jest bramką i co dzieje się ze słabszym testem.
- **Skill.** `ocena-asercji`
- **Skrypty.** `narzedzia/tabela_asercji.py`, `narzedzia/wymaganie.py`

```powershell
python narzedzia/tabela_asercji.py
python narzedzia/wymaganie.py reset-hasla
```

### 4. Zakres po zmianie

- **Sytuacja.** Po zmianie tester ma listę sprawdzeń i ograniczone okno czasu. Musi ustalić, od czego zacząć i co zostanie niesprawdzone, jeśli czasu zabraknie.
- **Model dostaje.** Jedno zdanie o zmianie i czasie („zmiana w resecie, 40 minut”), listę sprawdzeń z czasem wykonania i wymaganie.
- **Model oddaje.** Kolejność sprawdzeń od najwyższego ryzyka z powodem przy każdej pozycji, rachunek czasu narastająco, przypadki, których na liście brakuje względem wymagania, oraz wykaz tego, co nie mieści się w oknie.
- **Czego model nie robi.** Nie usuwa pozycji z listy i nie łączy kilku w jedną. Nie skraca czasów podanych w wejściu. Nie pomija dopisanego przypadku dlatego, że się nie mieści. Nie decyduje, co zostaje pominięte.
- **Decyzja człowieka.** Co wykonać w oknie, czy okno wydłużyć, czy przyjąć ryzyko pominięcia.
- **Skill.** `zakres-po-zmianie`
- **Skrypty.** `narzedzia/lista_sprawdzen.py`, `narzedzia/wymaganie.py`

```powershell
python narzedzia/lista_sprawdzen.py
python narzedzia/wymaganie.py reset-hasla
```

### 5. Zdanie o dwóch buildach

Wariant 20-minutowy: tak.

- **Sytuacja.** Tester ma liczby z dwóch buildów: czasy odpowiedzi, błędy, progi. Osoba, która decyduje o wydaniu, nie przeczyta dwóch tabel. Potrzebuje jednego zdania o tym, co się zmieniło.
- **Model dostaje.** Liczby dwóch buildów z gotowych plików wyników: profil obciążenia, progi i metryki każdej ścieżki. Skrypt niczego nie mierzy.
- **Model oddaje.** Jedno zdanie o zmianie między buildami. Pod nim porównanie profilu, tabelę metryk każdej ścieżki, odniesienie liczb do progów i listę tego, czego nie wie.
- **Czego model nie robi.** Nie zmienia progów i nie proponuje ich podniesienia. Nie porównuje liczb, gdy profile obciążenia się różnią. Nie orzeka o przyczynie w kodzie. Nie uśrednia ścieżek i nie pomija metryki, która wygląda źle.
- **Decyzja człowieka.** Czy zmiana blokuje wydanie, czy powstaje zgłoszenie, czy potrzebna jest dalsza diagnoza.
- **Skill.** `dwa-buildy-w-liczbach`
- **Skrypt.** `narzedzia/liczby.py`

```powershell
python narzedzia/liczby.py
```

### 6. Karta przed wgraniem

- **Sytuacja.** Osoba, która decyduje o wydaniu, nie czyta przebiegów. Tester składa dla niej krótką informację z wyników testów, liczb, otwartych zgłoszeń i zakresu.
- **Model dostaje.** Jeden zbiór: zapisane przebiegi buildów, liczby dwóch buildów, listę otwartych zgłoszeń oraz zakres planowany i wykonany.
- **Model oddaje.** Jedno zdanie i kartę o stałym układzie trzech części: co sprawdzone, co czerwone, czego nie ruszano.
- **Czego model nie robi.** Nie pisze słowa „wgrywamy” ani jego zaprzeczenia i nie zastępuje ich rekomendacją. Nie ocenia ryzyka biznesowego. Nie pomija i nie łagodzi czerwonych wyników. Nie przedstawia jako potwierdzonego czegoś, na co nie widział wyniku.
- **Decyzja człowieka.** Decyzja o wydaniu. Podejmuje ją osoba odpowiedzialna za wydanie.
- **Skill.** `karta-przed-wgraniem`
- **Skrypty.** `narzedzia/przebieg.py` (zapisuje przebiegi), `narzedzia/zbierz_wyniki.py` (zbiera wszystko w jeden plik)

```powershell
python narzedzia/przebieg.py --port 8765
python narzedzia/przebieg.py --port 8766
python narzedzia/zbierz_wyniki.py
```

### 7. Dane pod regułę

- **Sytuacja.** Reguła w wymaganiu mówi ogólnie, a test potrzebuje konkretnych wartości i konkretnego oczekiwanego wyniku. Tester układa dane, które pokazują regułę z każdej strony.
- **Model dostaje.** Wymaganie. Po decyzji człowieka także odpowiedzi builda na wybrane dane.
- **Model oddaje.** Tabelę wejść z oczekiwanym wynikiem i jego źródłem oraz te same dane w formacie pliku, który można wstawić w przebieg. Gdy wymaganie nie mówi, co ma się stać dla danego wejścia, w miejscu wyniku stoi pytanie do autora.
- **Czego model nie robi.** Nie wpisuje oczekiwanego wyniku, którego nie ma w wymaganiu, i nie odczytuje go z odpowiedzi aplikacji. Nie sięga po dane produkcyjne. Nie uruchamia przebiegu z własnej inicjatywy i nie dopisuje do pliku wejść, których człowiek nie wybrał.
- **Decyzja człowieka.** Które wejścia trafiają do przebiegu.
- **Skill.** `dane-pod-regule`
- **Skrypty.** `narzedzia/wymaganie.py`, po decyzji człowieka `narzedzia/przebieg_danych.py`

```powershell
python narzedzia/wymaganie.py reset-hasla
python narzedzia/przebieg_danych.py --port 8766 --dane material/dane/dane-resetu.json
```

Opcja `--dane` wskazuje plik z wejściami wybranymi przez człowieka. `material/dane/dane-resetu.json` to przykład takiego pliku.

### 8. Uprawnienia przy zwykłej historyjce

- **Sytuacja.** Autor historyjki opisuje drogę uprawnionego użytkownika. O tym, co ma się stać przy cudzych danych, starym tokenie albo roli tylko do odczytu, zwykle nie pisze, a tester musi to sprawdzić.
- **Model dostaje.** Dwie historyjki: reset hasła i filtr zamówień z opisem ról.
- **Model oddaje.** Osobną grupę przypadków uprawnień dla każdej historyjki, ułożoną według trzech pytań kontrolnych: obcy identyfikator, wygasły token albo sesja, rola tylko do odczytu. Oczekiwany wynik pochodzi z wymagania i ma cytat. Gdy wymaganie milczy, w jego miejscu stoi pytanie do autora.
- **Czego model nie robi.** Nie wymyśla polityki: kodu odpowiedzi, czasu życia tokenu ani tego, co wolno roli. Nie podaje zalecenia OWASP jako oczekiwanego wyniku. Nie wysyła żądań do systemu. Nie ogłasza, że funkcja jest bezpieczna.
- **Decyzja człowieka.** Politykę dostępu ustala autor wymagania albo właściciel bezpieczeństwa. Tester decyduje, które przypadki wchodzą do zestawu.
- **Skill.** `przypadki-uprawnien`
- **Skrypt.** `narzedzia/wymaganie.py`

```powershell
python narzedzia/wymaganie.py reset-hasla
python narzedzia/wymaganie.py filtr-zamowien
```

### P1. Czerwony przebieg: produkt, test czy środowisko

- **Sytuacja.** Rano po nocnym przebiegu tester ma kilka czerwonych testów. Musi ustalić, które mówią o produkcie, a które o samym teście, danych albo środowisku, i od czego zacząć.
- **Model dostaje.** Zapisany nocny przebieg, przebieg referencyjny tego samego zestawu na buildzie odniesienia i log przebiegu.
- **Model oddaje.** Grupy awarii o wspólnej przyczynie. Dla każdej: co się stało, wynik tych samych testów w przebiegu referencyjnym, proponowaną klasyfikację (produkt, test, dane, środowisko albo „nie ustaliłem”), dowód z wejścia i to, czego dowód nie rozstrzyga.
- **Czego model nie robi.** Nie ponawia przebiegu ani pojedynczych testów. Nie oznacza testu jako niestabilnego i go nie wyłącza. Nie klasyfikuje bez dowodu. Nie zakłada zgłoszeń i nie poprawia testów ani danych.
- **Decyzja człowieka.** Klasyfikacja i następny krok dla każdej grupy: zgłoszenie, poprawka testu, naprawa danych albo naprawa środowiska.
- **Skill.** `klasyfikacja-awarii`
- **Skrypt.** `narzedzia/przebieg_nocny.py`

```powershell
python narzedzia/przebieg_nocny.py
```

### P2. Ponowny test po poprawce

- **Sytuacja.** Programista oddaje build z poprawką. Tester powtarza test, który pokazał defekt, i sprawdza, czy zachowanie opisane w zgłoszeniu ustąpiło.
- **Model dostaje.** Zgłoszenie `material/zgloszenia/ZGL-101.md` i wynik testu wskazanego w zgłoszeniu na buildzie oddanym do ponownego testu.
- **Model oddaje.** Jedno zdanie o tym, czy kroki ze zgłoszenia dają teraz wynik oczekiwany. Pod nim tabelę krok po kroku i listę tego, czego wokół poprawki nie sprawdzono.
- **Czego model nie robi.** Nie zamyka zgłoszenia i nie zmienia jego stanu. Nie pisze, że defekt jest naprawiony. Nie rozszerza wniosku na zachowania, których test nie sprawdza. Nie zmienia testu, żeby pasował do nowego builda.
- **Decyzja człowieka.** Zamknąć zgłoszenie czy otworzyć je ponownie i czy przed tą decyzją wykonać dodatkowe sprawdzenia.
- **Skill.** `test-potwierdzajacy`
- **Skrypt.** `narzedzia/przebieg.py`; zgłoszenie model czyta z pliku

```powershell
python narzedzia/przebieg.py --port 8767 --test test_link_dziala_jeden_raz
```

### P3. Test niestabilny

- **Sytuacja.** Test, który na tym samym buildzie raz przechodzi, a raz nie, uczy zespół ignorować czerwony wynik. Tester szuka takich testów w historii przebiegów, zanim ktoś „naprawi” je ponowieniem albo wyłączeniem.
- **Model dostaje.** Historię dwunastu przebiegów tego samego zestawu na jednym buildzie: tabelę wyników, tabelę czasów i szczegóły uruchomień z wynikiem innym niż zaliczony.
- **Model oddaje.** Zdanie z liczbami: który test ma zmienny wynik i ile razy nie przeszedł. Pod nim okoliczności niezaliczonych uruchomień, przypuszczalny wzorzec oznaczony jako przypuszczenie i to, czego z historii nie da się rozstrzygnąć.
- **Czego model nie robi.** Nie dodaje ponowień ani pominięć i nie zmienia kodu testu. Nie wyłącza testu i nie przenosi go do kwarantanny. Nie nazywa testu niestabilnym na podstawie jednego przebiegu. Nie przesądza, czy przyczyna leży w teście, czy w systemie.
- **Decyzja człowieka.** Kwarantanna, naprawa czy pozostawienie testu, a jeśli naprawa, to testu czy systemu.
- **Skill.** `test-niestabilny`
- **Skrypt.** `narzedzia/historia.py`

```powershell
python narzedzia/historia.py --port 8765
```

### P4. Pokrycie wymagania testami

- **Sytuacja.** Zestaw testów rośnie i przestaje być oczywiste, które zdanie wymagania ma test, a które nie. Tester zestawia wymaganie z testami, żeby zobaczyć braki po obu stronach.
- **Model dostaje.** Wymaganie i listę testów: plik, nazwa i opis każdego testu.
- **Model oddaje.** Tabelę zdań wymagania z testami, które ich dotyczą, oraz dwie listy braków: zdania bez testu i testy bez zdania w wymaganiu. Przy każdym powiązaniu podaje, czy oparł je na opisie testu, czy na jego kodzie.
- **Czego model nie robi.** Nie dopisuje testów i nie usuwa istniejących. Nie ogłasza, że pokrycie jest wystarczające. Nie uznaje zdania za pokryte dlatego, że nazwa testu brzmi podobnie. Nie zmienia wymagania, żeby pasowało do testów.
- **Decyzja człowieka.** Które braki uzupełnić i co zrobić z testami bez zdania w wymaganiu.
- **Skill.** `pokrycie-wymagania`
- **Skrypty.** `narzedzia/wymaganie.py`, `narzedzia/lista_testow.py`

```powershell
python narzedzia/wymaganie.py reset-hasla
python narzedzia/lista_testow.py
```

### P5. Karta sesji eksploracyjnej

- **Sytuacja.** Tester pracujący ręcznie prowadzi sesję eksploracyjną o ograniczonym czasie. Przed sesją potrzebuje karty z celem, a po sesji raportu, który mówi dokładnie to, co jego notatki.
- **Model dostaje.** Przed sesją: wymaganie i listę ryzyk ustaloną przez zespół. Po sesji: notatki testera.
- **Model oddaje.** Przed sesją kartę: cel, ryzyka, których sesja dotyczy, pomysły do zbadania ze źródłem i to, co zostaje poza zakresem. Po sesji raport, który oddziela obserwacje testera od wniosków modelu i wypisuje pytania, które zostały.
- **Czego model nie robi.** Nie dopisuje do raportu czynności, których nie ma w notatkach. Nie uznaje obszaru za sprawdzony na podstawie karty. Nie nazywa obserwacji defektem. Nie zmienia poziomów ryzyka i nie wygładza wątpliwości testera.
- **Decyzja człowieka.** Cel, czas i build sesji oraz pomysły, które wchodzą do karty. Po sesji: które obserwacje są defektami, które pytania idą do autora i czy potrzebna jest kolejna sesja.
- **Skill.** `sesja-eksploracyjna`
- **Skrypt.** `narzedzia/wymaganie.py`; listę ryzyk i notatki model czyta z plików `material/sesja/ryzyka.md` i `material/sesja/notatki-z-sesji.md`

```powershell
python narzedzia/wymaganie.py reset-hasla
Get-Content material/sesja/ryzyka.md -Encoding UTF8
Get-Content material/sesja/notatki-z-sesji.md -Encoding UTF8
```

### P6. Przegląd zmiany w testach

- **Sytuacja.** Ktoś proponuje zmianę w kodzie testów i opisuje ją jako porządki. Po takiej zmianie przebieg bywa zielony, więc tester sprawdza, czy testy nadal pilnują tego samego co przedtem.
- **Model dostaje.** Opis zmiany od autora, różnicę dwóch wersji pliku z testami, tabelę wyników obu wersji na dwóch buildach i wymaganie.
- **Model oddaje.** Listę miejsc, w których bramka stała się słabsza: osłabiona asercja, usunięty przypadek, podniesiony próg, dodane pominięcie albo ponowienie. Przy każdym miejscu podaje zdanie wymagania, którego test pilnował, i skutek widoczny w wynikach. Osobno wypisuje zmiany bez wpływu na bramkę i zestawia opis autora z różnicą wersji.
- **Czego model nie robi.** Nie cofa zmiany i nie poprawia testów. Nie zatwierdza i nie odrzuca zmiany. Nie uznaje zmiany za bezpieczną dlatego, że po niej przebieg jest zielony. Nie ocenia intencji autora.
- **Decyzja człowieka.** Przyjąć zmianę, odrzucić ją albo przyjąć częściowo.
- **Skill.** `przeglad-zmiany-w-testach`
- **Skrypty.** `narzedzia/zmiana_w_testach.py`, `narzedzia/wymaganie.py`

```powershell
python narzedzia/zmiana_w_testach.py
python narzedzia/wymaganie.py reset-hasla
```

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
