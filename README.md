# 🛒 Inteligentny Scalper Ofert (Smart Edition)

Zaawansowany robot do automatycznego wyszukiwania najlepszych okazji na polskich i zagranicznych portalach aukcyjnych. Program nie tylko pobiera oferty, ale inteligentnie je analizuje, odrzucając "śmieci" (akcesoria, uszkodzone przedmioty) i sortując wyniki według opłacalności.

## 🌍 Obsługiwane serwisy
- **Allegro** (wraz z analizą sekcji "Stan")
- **Allegro Lokalnie**
- **OLX** (z obsługą dynamicznej paginacji)
- **Vinted**
- **Amazon**

---

## 🚀 Jak zacząć?

### 1. Wymagania
Program wymaga zainstalowanego **Pythona 3.8+** oraz przeglądarki **Microsoft Edge** (używanej do symulowania zachowania człowieka).

### 2. Instalacja zależności
Otwórz terminal w folderze projektu i uruchom:
```bash
pip install selenium xlsxwriter beautifulsoup4 thefuzz
```

### 3. Konfiguracja (`produkt.txt`)
Wpisz frazy, których szukasz, w pliku `produkt.txt`. Każda fraza w nowej linii.
Możesz używać **minusów**, aby wykluczyć niechciane słowa (np. `-uszkodzony`).

**Przykład zawartości `produkt.txt`:**
```text
iPhone 13 -etui -szkło
PlayStation 5 -gra -digital
MacBook Air M1
Xiaomi watch 2 pro
```

### 4. Uruchomienie
Aby uruchomić skaner, wpisz w konsoli:
```bash
python main.py
```
Program uruchomi przeglądarkę w tle, zacznie przeszukiwać serwisy i na bieżąco informować o postępach w konsoli.

---

## 🧠 Smart Filtr - Jak to działa?
To nie jest zwykły scraper. Program posiada wielopoziomowy system weryfikacji jakości ofert:

1.  **Globalna Czarna Lista (`filter.py`)**:
    *   Automatycznie odrzuca setki słów oznaczających akcesoria (etui, pudełka, kable, paski) oraz uszkodzenia (uszkodzony, na części, zablokowany).
2.  **Inteligentne czyszczenie parametrów**:
    *   Program ignoruje parametry techniczne w tytułach, aby uniknąć pomyłek (np. `iPhone 16 GB` nie zostanie pomylony z `iPhone 16` tylko przez liczbę 16).
3.  **Fuzzy Logic (TheFuzzy)**:
    *   Algorytm rozmytego dopasowania tekstu wyłapuje literówki i mylące opisy.
    *   Stosuje restrykcyjne dopasowanie dla krótkich słów kluczowych (np. "Air", "Pro", "Mini"), aby uniknąć fałszywych trafień.
4.  **Wykluczenia użytkownika**:
    *   Respektuje Twoje minusy z pliku konfiguracyjnego (np. `-powystawowy`).

---

## 📊 Wyniki i Raport Excel (`wyniki.xlsx`)
Po zakończeniu pracy program generuje plik `wyniki.xlsx`, który otwiera się automatycznie.

### Cechy raportu:
*   **Sortowanie**: Oferty są automatycznie sortowane od najtańszej.
*   **Kolorowanie składni**:
    *   🟢 **Ciemna zieleń**: Nowy / Idealny
    *   🟢 **Jasna zieleń**: Powystawowy / Bez metki
    *   🟠 **Pomarańczowy/Żółty**: Używany (Dobry/Bardzo dobry)
    *   🔴 **Czerwony**: Uszkodzony / Stan niezadowalający
*   **Aktywne linki**: Możesz kliknąć w link, aby przejść bezpośrednio do oferty.

---

## 📂 Struktura Techniczna

*   `main.py` - Główny orkiestrator. Zarządza wątkami dla każdego serwisu i zbiera wyniki. Limituje pobieranie do **10 potwierdzonych ofert** na frazę per serwis (można zmienić zmienną `MAX_OFERT` w kodzie).
*   `modules/` - Niezależne moduły dla każdego serwisu (API/Scrapery).
    *   Każdy moduł (np. `allegro`) posiada `fetcher.py` (Selenium/Requests) oraz `parser.py` (BeautifulSoup4).
*   `utils/`
    *   `filter.py` - Logika "Smart Filtra" i fuzzy matchingu.
    *   `excel_handler.py` - Generowanie raportu `.xlsx` z warunkowym formatowaniem.
*   `temp/` - Katalog na tymczasowe pliki HTML (zapisywane podczas debugowania/rozwoju).
