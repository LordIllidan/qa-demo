# Plan spotkania: AI na chapter Frontend (60 min)

Godzinne spotkanie chapteru frontendowego o AI: aktualności, status tematów firmowych, A2UI 1.0 oraz praktyka dla zespołu UI.

## Cel

Zespół FE wychodzi ze spotkania ze wspólnym obrazem: co się zmieniło w AI dla frontu, jak w firmie domykamy wybrane tematy AI, czym jest A2UI 1.0 i jakie 2–3 rzeczy warto przetestować lokalnie w najbliższym sprincie.

## Agenda (60 min)

| Czas | Blok | Kto | Forma |
| --- | --- | --- | --- |
| 0–5 | Otwarcie, cel, agenda | prowadzący | mówione |
| 5–15 | 1. Co nowego w AI | prowadzący / chętny | skrót + 1–2 linki |
| 15–25 | 2. Status załatwiania tematów AI w firmie | Ty | Ty prowadzisz treść |
| 25–35 | 3. A2UI 1.0 — oficjalny release | prowadzący | krótki briefing |
| 35–50 | 4. Praktyka FE: generative UI, design system, MCP/Skills | prowadzący + zespół | rozmowa + przykłady |
| 50–60 | 5. Pytania, decyzje, follow-upy | wszyscy | lista akcji |

## 1. Co nowego w AI (ok. 10 min)

Skrót pod frontend — bez ogólnego „hype tour”.

Proponowane punkty do omówienia:

- **Agenci w IDE i w terminalu** — praca wieloplikowa (Cursor / Copilot Agent / Claude Code): kiedy agent ma sens przy feature UI, a kiedy zostaje tylko completion.
- **MCP i Skills** — agent łączy się z narzędziami (np. Figma, repo, CI); Skills dają instrukcję „jak używać narzędzi”, nie tylko surowe API. Dla FE: design → komponenty → PR w jednym przebiegu, z review człowieka.
- **UI świadome kontekstu wizualnego** — narzędzia, które widzą DOM / przeglądarkę, a nie tylko pliki; znaczenie dla regresji layoutu i „czy to wygląda dobrze”.
- **Granica odpowiedzialności** — model proponuje, człowiek zatwierdza design system, a11y i kontrakt API (ta sama zasada co w qa-demo: zdanie modelu ≠ decyzja zespołu).

Materiał do pokazania (opcjonalnie 1 slajd / 1 ekran):

- lista 3 narzędzi używanych w chapterze + 1 zdanie „do czego u nas”;
- 1 przykład „złe użycie AI na FE” (np. nowy styl poza DS) vs „dobre” (generacja wariantów w ramach tokenów).

## 2. Status załatwiania tematów AI w firmie (ok. 10 min)

**Treść prowadzisz Ty** — w agendzie tylko slot i ramy.

Sugerowane ramy (wypełniasz na żywo):

- które tematy AI są już domknięte / w toku / zablokowane;
- co to oznacza dla chapteru FE (narzędzia, licencje, polityka, dane);
- czego zespół ma się trzymać od dziś (1–3 reguły).

Bez materiałów zastępczych w tym dokumencie — treść jest Twoja.

## 3. A2UI 1.0 — krótko dla zespołu (ok. 10 min)

Oficjalny, stabilny release otwartego protokołu **generative UI** od Google (ogłoszenie ~11 Nov 2026). Agent nie odpowiada wyłącznie ścianą tekstu — opisuje interaktywny ekran (formularz, wykres, karta potwierdzenia), a **aplikacja rysuje go swoimi natywnymi komponentami**.

### Co powiedzieć zespołowi (3–4 zdania)

1. **Agent opisuje UI, appka go renderuje** — A2UI to protokół wiadomości (JSON stream), nie gotowy framework UI „zamiast Reacta”.
2. **Design system zostaje nasz** — agent układa tylko zarejestrowane komponenty; brand i tokeny zostają po stronie aplikacji.
3. **1.0 = produkcyjny kontrakt** — stabilny protokół, dwukierunkowe wywołania funkcji (np. picker sprawdza dostępność od razu), wsparcie a11y i metadanych; renderery web: React, Angular, Lit; też Flutter / SwiftUI; Jetpack Compose dogania 1.0.
4. **Łączy się z MCP Apps** — ten sam widok może wejść w asystenta (Claude / Gemini) i w naszą appkę; przykłady u partnerów: Atlassian (karty w Jira), Alation (feed z wykresami).

### Czego nie obiecywać na spotkaniu

- że „wyrzucamy obecny frontend”;
- że generative UI zastępuje deterministyczne ekrany (listy, nawigacja, standardowe formularze zostają jak są).

### Linki na follow-up

- Ogłoszenie: [A2UI 1.0 — Google Developers Blog](https://developers.googleblog.com/en/a2ui-10-build-delightful-fast-reliable-agentic-experiences/)
- Spec / quickstart: [a2ui.org](https://a2ui.org/)
- Spec v1.0: [v1.0 Protocol Specification](https://a2ui.org/specification/v1.0-a2ui/)

## 4. Reszta agendy — propozycja (ok. 15 min + 10 min na domknięcie)

### 4a. Generative UI a nasz design system (ok. 7 min)

Pytania do chapteru:

- które komponenty z DS miałyby sens jako katalog A2UI (formularze decyzji, porównania, potwierdzenia akcji)?;
- gdzie generative UI **nie** wchodzi (checkout krytyczny, compliance, stała nawigacja)?;
- kto pilnuje katalogu komponentów i review „czy agent nie wyszedł poza DS”?

Wynik bloku: 1 zdanie decyzji roboczej („interesuje nas / parkujemy / ktoś robi spike”).

### 4b. Codzienny workflow FE z agentem (ok. 5 min)

Szybka mapa ról narzędzia (bez dema live, chyba że jest gotowe):

| Potrzeba | Typ narzędzia | Uwaga |
| --- | --- | --- |
| szybkie dopisywanie w pliku | completion (Copilot itd.) | niski koszt review |
| feature / refactor wielu plików | agent w IDE | obowiązkowy diff + a11y |
| design → kod | MCP (Figma itd.) + Skills | tylko tokeny / komponenty z DS |
| „czy UI wygląda OK” | agent z przeglądarką / DOM | nie zastępuje testów wizualnych |

### 4c. Domknięcie: pytania i akcje (ok. 10 min)

Na tablicy / w notatce po spotkaniu zostają maksymalnie trzy punkty:

1. **Spike (opcjonalnie):** kto w 0,5–1 dzień odpala playground A2UI (React) i wraca z wnioskiem „pasuje / nie pasuje do naszego DS”.
2. **Reguła chapteru:** 1 zdanie o review AI na FE (np. „AI nie wprowadza nowych wzorców wizualnych poza DS”).
3. **Następne spotkanie:** czy powtarzamy „co nowego w AI” cyklicznie (np. co miesiąc, 15 min).

## Materiały prowadzącego (checklista przed startem)

- [ ] 1 slajd / notatka: „Co nowego w AI” (max 5 bulletów)
- [ ] Twoja treść do bloku 2 (status firmowy)
- [ ] 1 ekran lub link: A2UI playground / ogłoszenie 1.0
- [ ] Pusta lista follow-upów (3 sloty)
- [ ] Timer na bloki 10 / 10 / 10 / 15 / 10

## Po spotkaniu

Wkleić do notatek chapteru: decyzje z bloku 4c oraz właścicieli spike’ów. Ten plik zostaje szablonem na kolejne edycje (aktualizować tylko sekcję 1 i ewentualnie A2UI, gdy wyjdzie minor po 1.0).
