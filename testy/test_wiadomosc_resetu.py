"""Testy wiadomości z linkiem resetu. Wymaganie: material/wymagania/reset-hasla.md."""

import time


def test_wiadomosc_z_linkiem_jest_w_skrzynce(aplikacja, konto):
    """Po prośbie o reset w skrzynce użytkownika jest wiadomość z linkiem resetu."""
    aplikacja.popros_o_reset(konto.email)
    time.sleep(0.06)

    skrzynka = aplikacja.czytaj_skrzynke(konto.email)
    assert skrzynka.status == 200
    assert "/reset?token=" in skrzynka.tresc["link"]
