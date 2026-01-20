import xlsxwriter
import os

def zapisz_dane_do_excela(dane, nazwa_pliku="wyniki.xlsx"):
    """
    Funkcja tworzy nowy plik Excel i zapisuje w nim listę znalezionych ofert.
    Zajmuje się też ładnym formatowaniem (kolory, pogrubienia, linki).
    
    Args:
        dane (list): Lista słowników z ofertami (tytuł, cena, link, itp.)
        nazwa_pliku (str): Nazwa pliku wyjściowego (domyślnie 'wyniki.xlsx')
    """
    print(f"Generuję plik Excel: {nazwa_pliku}...")
    
    # Tworzymy nowy skoroszyt (plik Excel) using biblioteki xlsxwriter
    workbook = xlsxwriter.Workbook(nazwa_pliku)
    # Dodajemy arkusz o nazwie "Promocje"
    worksheet = workbook.add_worksheet("Promocje")

    # --- DEFINICJA STYLÓW I FORMATOWANIA ---
    
    # Format nagłówka: pogrubiona czcionka, tło szałwiowe (#D7E4BC), obramowanie
    naglowek_fmt = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
    
    # Format dla linków: niebieska czcionka, podkreślenie, wyrównanie w pionie do środka
    link_fmt = workbook.add_format({'font_color': 'blue', 'underline': 1, 'valign': 'vcenter'})
    
    # Format ogólny dla tekstu: wyrównanie w pionie do środka (żeby tekst nie był przyklejony do góry komórki)
    text_fmt = workbook.add_format({'valign': 'vcenter'})
    
    # Format waluty: np. "1 200,00 zł" (#,##0.00 oznacza separator tysięcy i dwa miejsca po przecinku)
    waluta_fmt = workbook.add_format({'num_format': '#,##0.00 "zł"', 'valign': 'vcenter'})

    # --- FORMATY DLA STANU PRZEDMIOTU (KOLORY) ---
    # Używamy różnych kolorów tła w zależności od stanu przedmiotu, żeby łatwiej było przeglądać oferty.
    
    # 1. Idealny (Nowy) - Ciemna zieleń (najlepsze oferty)
    fmt_nowy_idealny = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100', 'valign': 'vcenter'})
    
    # 2. Prawie nowy (Bez metki, powystawowy) - Jasna zieleń
    fmt_prawie_nowy = workbook.add_format({'bg_color': '#E2EFDA', 'font_color': '#006100', 'valign': 'vcenter'})
    
    # 3. Bardzo dobry - Żółty (ostrzegawczy, ale wciąż ok)
    fmt_bdb = workbook.add_format({'bg_color': '#FFF2CC', 'font_color': '#9C6500', 'valign': 'vcenter'})
    
    # 4. Dobry - Pomarańczowy
    fmt_dobry = workbook.add_format({'bg_color': '#FCE4D6', 'font_color': '#9C5700', 'valign': 'vcenter'})
    
    # 5. Używany standard / Zadowalający - Jasny czerwony
    fmt_uzywany = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006', 'valign': 'vcenter'})
    
    # 6. Uszkodzony - Ciemniejszy czerwony/szary (najgorsze)
    fmt_zly = workbook.add_format({'bg_color': '#E6B8B7', 'font_color': '#9C0006', 'valign': 'vcenter'})


    # Wpisujemy nagłówki w pierwszym wierszu (A1)
    naglowki = ["Nazwa Ogłoszenia", "Cena [zł]", "Stan", "Źródło", "Link"]
    worksheet.write_row('A1', naglowki, naglowek_fmt)

    # --- SORTOWANIE DANYCH PO CENIE ---
    # Funkcja pomocnicza, która wyciąga cenę jako liczbę (float) z oferty
    def wyciagnij_cene(produkt):
        try:
            # Pobieramy cenę, zamieniamy na napis
            raw_price = str(produkt.get('price', 0))
            # Zamieniamy przecinek na kropkę (ważne dla Pythona: 12,50 -> 12.50)
            raw_price = raw_price.replace(',', '.')
            # Zostawiamy tylko cyfry i kropkę
            clean_price = "".join(c for c in raw_price if c.isdigit() or c == '.')
            if not clean_price:
                return 0.0
            return float(clean_price)
        except:
            return 0.0

    print("Sortowanie ofert od najtańszej do najdroższej...")
    # Sortujemy listę 'dane' w miejscu, używając funkcji wyciagnij_cene jako klucza
    dane.sort(key=wyciagnij_cene)
    # --------------------------------------------------

    # Pętla wpisująca dane wiersz po wierszu
    for i, produkt in enumerate(dane):
        # i zaczyna się od 0, a w Excelu pierwszy wiersz to nagłówki (indeks 0), więc dane zaczynamy od wiersza 1
        row = i + 1
        
        # Kolumna A (indeks 0): Nazwa ogłoszenia
        worksheet.write(row, 0, produkt.get('title', 'Brak nazwy'), text_fmt)
        
        # Kolumna B (indeks 1): Cena
        # Musimy ponownie wyczyścić cenę, żeby zapisać ją jako liczbę w Excelu (dla poprawnego sortowania w samym Excelu)
        try:
            raw_price = str(produkt.get('price', 0))
            # FIX: Zamiana przecinka na kropkę PRZED czyszczeniem (np. 800,00 -> 800.00)
            raw_price = raw_price.replace(',', '.')
            clean_price = "".join(c for c in raw_price if c.isdigit() or c == '.')
            if not clean_price: 
                cena = 0.0
            else:
                cena = float(clean_price)
        except:
            cena = 0.0
        # Zapisujemy cenę z formatem waluty (zł)
        worksheet.write(row, 1, cena, waluta_fmt)

        # Kolumna C (indeks 2): Stan
        stan = produkt.get('condition', 'Nieznany')
        s = stan.lower() # Zamieniamy na małe litery dla łatwiejszego porównywania
        
        wybrany_format = text_fmt # Domyślny format (brak koloru)
        
        # Logika dopasowania koloru do stanu
        # Sprawdzamy słowa kluczowe w opisie stanu
        if any(x in s for x in ["nowy z metką", "nowe z metką"]):
            wybrany_format = fmt_nowy_idealny
        elif any(x in s for x in ["nowy", "nowe"]): 
            # Sam "nowy" też traktujemy jako idealny
            wybrany_format = fmt_nowy_idealny
        elif any(x in s for x in ["bez metki", "powystawowy", "odnowiony"]):
            wybrany_format = fmt_prawie_nowy
        elif "bardzo dobry" in s:
            wybrany_format = fmt_bdb
        elif "dobry" in s: 
            # Uwaga: "bardzo dobry" zawiera w sobie słowo "dobry", dlatego sprawdzamy go wcześniej
            wybrany_format = fmt_dobry
        elif any(x in s for x in ["zadowalający", "używany", "używane"]):
            wybrany_format = fmt_uzywany
        elif any(x in s for x in ["uszkodzony", "uszkodzone"]):
            wybrany_format = fmt_zly
            
        worksheet.write(row, 2, stan, wybrany_format)
        
        # Kolumna D (indeks 3): Źródło (np. Allegro, OLX)
        worksheet.write(row, 3, produkt.get('source', 'Allegro'), text_fmt)
        
        # Kolumna E (indeks 4): Link
        url = produkt.get('url', '')
        # Sprawdzamy, czy link jest poprawny
        if url and url != "Brak linku":
             # Zapisujemy jako aktywny link z opisem "Link" (żeby nie zaśmiecać widoku długim URL-em)
             worksheet.write_url(row, 4, url, link_fmt, string='Link')
        else:
             worksheet.write(row, 4, "", text_fmt)

    # Ustawianie szerokości kolumn dla lepszej czytelności
    worksheet.set_column('A:A', 50) # Tytuł - szeroki
    worksheet.set_column('B:B', 15) # Cena
    worksheet.set_column('C:C', 20) # Stan 
    worksheet.set_column('D:D', 15) # Źródło
    worksheet.set_column('E:E', 10) # Link - wąski, bo to tylko słowo "Link"

    # Zamykamy i zapisujemy plik fizycznie na dysku
    workbook.close()
    
    # Próba automatycznego otwarcia pliku po zapisaniu
    try:
        os.startfile(nazwa_pliku)
        print("Excel otwarty pomyślnie.")
    except:
        # Jeśli się nie uda otworzyć (np. na serwerze bez GUI), wypisujemy ścieżkę
        print(f"Zapisano plik: {os.path.abspath(nazwa_pliku)}")