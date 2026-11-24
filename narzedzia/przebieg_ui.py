"""Uruchamia krótki przebieg interfejsu w Playwright i podaje kroki, nie surowy log.

Użycie:  python narzedzia/przebieg_ui.py --port 8765

Każdy krok ma czynność, selektor i tekst, który strona pokazała. Skrypt
nie ocenia, czy przebieg jest zgodny z wymaganiem. Wymaga pakietu
playwright i przeglądarki: python -m playwright install chromium
"""

from __future__ import annotations

import argparse

from wspolne import ADRES, BladNarzedzia, build_na_porcie, oddaj, tabela, uruchom_narzedzie


def main() -> None:
    parser = argparse.ArgumentParser(description="Przebieg interfejsu resetu hasła w Playwright.")
    parser.add_argument("--port", type=int, required=True, help="port builda")
    argumenty = parser.parse_args()
    build = build_na_porcie(argumenty.port)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as blad:
        raise BladNarzedzia(
            "brak pakietu playwright. Zainstaluj go: python -m pip install playwright; "
            "python -m playwright install chromium"
        ) from blad

    adres = f"http://{ADRES}:{argumenty.port}/"
    kroki = []
    with sync_playwright() as playwright:
        try:
            przegladarka = playwright.chromium.launch(headless=True)
        except Exception as blad:
            raise BladNarzedzia(
                "Playwright nie uruchomił przeglądarki. Zainstaluj ją: python -m playwright install chromium. "
                f"({type(blad).__name__}: {blad})"
            ) from blad
        strona = przegladarka.new_page()
        strona.goto(adres)
        kroki.append(("otwarcie strony", adres, strona.get_by_role("heading").first.inner_text()))
        strona.get_by_label("Adres e-mail").fill("anna@example.com")
        kroki.append(("wpisanie adresu", "label: Adres e-mail", "anna@example.com"))
        strona.get_by_role("button", name="Wyślij link").click()
        strona.wait_for_function("() => document.getElementById('wynik').textContent.trim().length > 0")
        wynik = strona.get_by_role("status").inner_text()
        kroki.append(("kliknięcie przycisku", "button: Wyślij link", wynik))
        przegladarka.close()

    tresc = [
        "## Przebieg interfejsu",
        f"narzędzie przeglądarki: Playwright, chromium, headless",
        f"build: {build['numer']} (port {build['port']})",
        f"adres: {adres}",
        "",
        *tabela(["krok", "czynność", "selektor", "tekst ze strony"],
                [[n, *krok] for n, krok in enumerate(kroki, start=1)]),
        "",
    ]
    oddaj("przebieg_ui.py", "wynik przebiegu interfejsu", tresc, f"przebieg-ui-{argumenty.port}.txt")


if __name__ == "__main__":
    uruchom_narzedzie(main)
