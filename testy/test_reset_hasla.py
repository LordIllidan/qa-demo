"""Testy resetu hasła. Wymaganie: material/wymagania/reset-hasla.md."""


def test_link_dziala_jeden_raz(aplikacja, konto):
    """Link resetu działa jeden raz: drugie użycie tego samego linku jest odrzucane, a hasło się nie zmienia."""
    token = aplikacja.zamow_link_resetu(konto.email)

    pierwsze_uzycie = aplikacja.ustaw_haslo(token, "NoweHaslo-1")
    assert pierwsze_uzycie.status == 200

    drugie_uzycie = aplikacja.ustaw_haslo(token, "InneHaslo-2")
    assert drugie_uzycie.status == 410

    assert aplikacja.zaloguj(konto.email, "InneHaslo-2").status == 401
    assert aplikacja.zaloguj(konto.email, "NoweHaslo-1").status == 200


def test_wystarczy_kod_200(aplikacja, konto):
    """Ustawienie hasła przez link resetu odpowiada kodem 200."""
    token = aplikacja.zamow_link_resetu(konto.email)

    odpowiedz = aplikacja.ustaw_haslo(token, "NoweHaslo-1")
    assert odpowiedz.status == 200


def test_nowe_haslo_loguje_stare_nie(aplikacja, konto):
    """Po resecie użytkownik loguje się nowym hasłem, a stare hasło przestaje działać."""
    token = aplikacja.zamow_link_resetu(konto.email)
    aplikacja.ustaw_haslo(token, "NoweHaslo-1")

    assert aplikacja.zaloguj(konto.email, "NoweHaslo-1").status == 200
    assert aplikacja.zaloguj(konto.email, konto.haslo).status == 401


def test_nieznany_token_jest_odrzucany(aplikacja, konto):
    """Ustawienie hasła z tokenem, którego system nie wydał, jest odrzucane, a hasło się nie zmienia."""
    odpowiedz = aplikacja.ustaw_haslo("token-ktorego-nikt-nie-wydal", "NoweHaslo-1")
    assert odpowiedz.status == 400

    assert aplikacja.zaloguj(konto.email, "NoweHaslo-1").status == 401
    assert aplikacja.zaloguj(konto.email, konto.haslo).status == 200


def test_stan_zwraca_numer_builda(aplikacja):
    """Adres /stan odpowiada kodem 200 i podaje numer builda."""
    odpowiedz = aplikacja.stan()
    assert odpowiedz.status == 200
    assert odpowiedz.tresc["build"]
