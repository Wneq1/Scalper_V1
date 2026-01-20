# 🛒 Inteligentny Scalper Ofert (Smart Edition)

To zaawansowany robot do wyszukiwania okazji na polskich i zagranicznych portalach aukcyjnych.
Program automatycznie pobiera, filtruje i ocenia oferty, odrzucając "śmieci" (akcesoria, uszkodzone, błędne opisy).

## 🌍 Obsługiwane serwisy
- **Allegro**
- **Allegro Lokalnie**
- **OLX**
- **Vinted**
- **Amazon**

---

## 🚀 Jak zacząć?

### 1. Instalacja
Upewnij się, że masz Pythona i wymagane biblioteki:
```bash
pip install selenium xlsxwriter beautifulsoup4 thefuzz
```

### 2. Konfiguracja szukania (`produkt.txt`)
Wpisz frazy w pliku `produkt.txt` (każda w nowej linii).
Możesz używać **minusów**, aby wykluczyć słowa!

**Przykład:**
```text
iPhone 13 -etui -szkło
PlayStation 5 -gra -digital
MacBook Air M1
```
*Program automatycznie odrzuci też typowe śmieci jak "pudełko", "uszkodzony", "bateria" dzięki wbudowanemu Smart Filtrowi.*

### 3. Uruchomienie
Włącz program klikając w `main.py` lub wpisując w konsoli:
```bash
python main.py
```

---

## 🧠 Jak działa Smart Filtr?
Program nie pobiera wszystkiego jak leci. Posiada 3-stopniowy system weryfikacji:
1.  **Globalna Czarna Lista**: Automatycznie usuwa tysiące śmieci (etui, kable, pudełka, uszkodzone).
2.  **Wykluczenia Użytkownika**: Respektuje Twoje minusy (np. `-uszkodzony`).
3.  **Fuzzy Logic**: Inteligentne dopasowanie tytułu. Jeśli szukasz "MacBook Air", program odrzuci "MacBook Pro", nawet jeśli sprzedawca użył mylącego opisu.

## 📊 Wyniki (`wyniki.xlsx`)
Po zakończeniu pracy powstanie plik Excel z ofertami posortowanymi od najtańszej.
- 🟢 **Zielony**: Nowy / Idealny
- 🟡 **Żółty**: Używany
- 🔴 **Czerwony**: Uszkodzony / Nieznany

---

## 📂 Struktura plików
- `main.py` - Główny silnik programu.
- `modules/` - Skrypty pobierające dla każdego serwisu.
- `utils/` - Logika filtrowania (`filter.py`) i zapisu (`excel_handler.py`).
- `temp/` - Pliki tymczasowe (czyszczone automatycznie).

## 🛠️ Technologie i działanie
Program został napisany w języku **Python** i wykorzystuje szereg nowoczesnych bibliotek do automatyzacji przeglądarki i przetwarzania danych:
- **Selenium**: Do symulowania zachowania użytkownika i dynamicznego ładowania stron (szczególnie dla OLX i Vinted).
- **BeautifulSoup4**: Do szybkiego i precyzyjnego parsowania kodu HTML i wyciągania kluczowych informacji (ceny, tytuły, linki).
- **FuzzyWuzzy (TheFuzzy)**: Algorytmy rozmytego dopasowania tekstu pozwalają na inteligentne filtrowanie ogłoszeń, które nie pasują dokładnie do frazy, ale są z nią powiązane (lub wykluczanie tych, które są podobne do "ofert śmieciowych").
- **Pandas/XlsxWriter**: Do generowania przejrzystych raportów w formacie Excel z kolorowaniem składni w zależności od stanu produktu.

### Architektura
Projekt jest podzielony na niezależne moduły (`modules/`), co pozwala na łatwe dodawanie nowych serwisów. Każdy moduł posiada własny `fetcher` (pobieranie) i `parser` (analiza). Całością zarządza `main.py`, który orkiestruje proces wyszukiwania, filtrowania i zapisywania wyników.
