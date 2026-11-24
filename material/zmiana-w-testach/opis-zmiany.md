# Porządki w testach resetu hasła

Przebieg na buildzie 1.5.0 był czerwony i blokował scalanie. Uporządkowałem testy resetu:

- hasło używane w kilku testach trafiło do stałej `NOWE_HASLO`,
- uprościłem sprawdzenie drugiego użycia linku,
- usunąłem powtarzające się sprawdzenia.

Po zmianie przebieg jest zielony na obu buildach.
