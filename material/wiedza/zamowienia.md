# Zamówienia: statusy, daty i plik CSV

- Rodzaj: opis działania dla zespołu
- Właściciel dokumentu: zespół programistów zamówień
- Aktualizacja: 21.10.2026

## Statusy zamówienia

Zamówienie ma jeden z czterech statusów: nowe, opłacone, wysłane, anulowane. Zamówienie zaczyna jako nowe. Po zaksięgowaniu płatności przechodzi w opłacone, a po przekazaniu przewoźnikowi w wysłane. Anulować można zamówienie nowe albo opłacone. Zamówienia wysłanego nie da się anulować.

## Data złożenia

Data złożenia to dzień, w którym zamówienie dostało status nowe. Sklep zapisuje ją w strefie czasowej Europe/Warsaw. Zmiana statusu nie zmienia daty złożenia.

## Plik CSV z listą zamówień

Plik ma jeden wiersz na zamówienie i kolumny: numer, data złożenia, status, kwota. Separatorem jest średnik, kodowanie UTF-8. Plik zawiera te same zamówienia co lista po zastosowaniu filtrów.
