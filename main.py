import os
import sys

# Importujemy funkcję do czytania listy produktów z pliku tekstowego
from utils.file_reader import czytaj_szukane_frazy

# Importujemy dedykowane funkcje pobierania pojedynczych stron (dla dynamicznej paginacji)
from modules.allegro.fetcher import pobierz_strone_allegro
from modules.olx.fetcher import pobierz_strone_olx
from modules.vinted.fetcher import pobierz_strone_vinted
from modules.allegrolokalnie.fetcher import pobierz_strone_allegrolokalnie
from modules.amazon.fetcher import pobierz_strone_amazon

# Importujemy funkcję do zapisywania zebranych danych do pliku Excel
from utils.excel_handler import zapisz_dane_do_excela

# Importujemy filtr
from utils.filter import filtruj_oferty

def run_scraper():
    """
    Uruchamia proces pobierania danych w trybie konsolowym.
    """
    print("\n" + "="*40)
    print("   🛍️  SCALPER - TRYB KONSOLOWY (SMART) 🛍️")
    print("="*40)
    
    frazy = czytaj_szukane_frazy()
    if not frazy:
        print("Brak fraz do wyszukania. Sprawdź plik produkt.txt.")
        return

    # --- KONFIGURACJA ---
    MAX_OFERT = 10
    print(f"Cel: Znaleźć {MAX_OFERT} POTWIERDZONYCH ofert dla każdej frazy na każdym serwisie.")

    wszystkie_oferty = []

    # Słownik konfiguracji serwisów: Nazwa -> Funkcja pobierająca stronę
    serwisy = {
        "ALLEGRO": pobierz_strone_allegro,
        "OLX": pobierz_strone_olx,
        "VINTED": pobierz_strone_vinted,
        "ALLEGRO LOKALNIE": pobierz_strone_allegrolokalnie,
        "AMAZON": pobierz_strone_amazon
    }

    for fraza in frazy:
        print(f"\n" + ("#"*50))
        print(f" >>> SZUKAM: {fraza} <<<")
        print(("#"*50))
        
        for nazwa_serwisu, funkcja_pobierajaca in serwisy.items():
            print(f"\n--- [{nazwa_serwisu}] Start dla '{fraza}' ---")
            
            collected_for_service = []
            page = 1
            max_pages = 20 # Zabezpieczenie przed nieskończoną pętlą (np. max 20 stron)
            
            while len(collected_for_service) < MAX_OFERT:
                print(f"   -> Pobieram stronę {page} ({nazwa_serwisu})...")
                try:
                    # Pobieramy ofertę z danej strony
                    raw_page = funkcja_pobierajaca(fraza, numer_strony=page, verbose=False)
                    
                    if not raw_page:
                        print(f"   -> Brak ofert na stronie {page}. Koniec wyszukiwania w {nazwa_serwisu}.")
                        break
                    
                    # Filtrujemy (Smart Filter)
                    dobre, odrzucone = filtruj_oferty(raw_page)
                    print(f"      Strona {page}: Pobranno {len(raw_page)}, Odrzucono {odrzucone}, OK {len(dobre)}")
                    
                    collected_for_service.extend(dobre)
                    
                    # Jeśli uzbieraliśmy komplet, przerywamy
                    if len(collected_for_service) >= MAX_OFERT:
                        break
                    
                    page += 1
                    if page > max_pages:
                        print(f"   -> Osiągnięto limit stron ({max_pages}) dla {nazwa_serwisu}.")
                        break
                        
                except Exception as e:
                    print(f"Błąd {nazwa_serwisu} strona {page}: {e}")
                    # W razie błędu jednej strony próbujemy iść dalej? Lepiej przerwać dla tego serwisu.
                    break
            
            # Dodajemy wyniki z tego serwisu do puli, przycinając do limitu
            finalne_z_serwisu = collected_for_service[:MAX_OFERT]
            print(f"   [{nazwa_serwisu}] Zukces! Dodano {len(finalne_z_serwisu)} ofert.")
            wszystkie_oferty.extend(finalne_z_serwisu)

    # 3. Zapis do Excela
    print(f"\n" + "="*40)
    print(f"PODSUMOWANIE CAŁKOWITE: {len(wszystkie_oferty)} ofert.")
    
    if wszystkie_oferty:
        zapisz_dane_do_excela(wszystkie_oferty)
    else:
        print("Nie znaleziono żadnych ofert spełniających kryteria.")
    
    print("\nZakończono pracę.")

def main():

     run_scraper()
        
if __name__ == "__main__":
    main()
