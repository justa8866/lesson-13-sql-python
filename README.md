# Lekcja 13 — SQL w Pythonie

Praca domowa z analizy danych: zadania SQL wykonywane w Pythonie z użyciem SQLite, pandas i NumPy.

## Zawartość

- `zadanie_01.py`–`zadanie_20.py` — rozwiązania zadań: filtrowanie, sortowanie, łączenie tabel, agregacje, podzapytania, funkcje okienkowe i analiza danych.
- `zadanie_20_nieoptymalna.py`, `zadanie_20_czesciowa.py`, `zadanie_20_optymalna.py` — osobne warianty przetwarzania danych do porównania wydajności.
- `zadanie_20.py` — wspólne porównanie trzech strategii pod względem czasu, pamięci i liczby pobranych wierszy.

## Uruchomienie

Wymagany jest Python 3. Zainstaluj zależności w terminalu otwartym w katalogu projektu:

```powershell
python -m pip install -r requirements.txt
```

Następnie uruchom wybrany plik, na przykład:

```powershell
python zadanie_02.py
```

Każdy skrypt tworzy własną bazę SQLite w pamięci i wyświetla wyniki w terminalu. Nie trzeba przygotowywać zewnętrznej bazy danych. Moduły `sqlite3` i `time` należą do biblioteki standardowej Pythona.
