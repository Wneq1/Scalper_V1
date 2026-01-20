from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



import urllib.parse
import re
from .parser import parsuj_html

def polacz_przez_edge_v2(url, nazwa_pliku="allegro.html", verbose=True):
    """
    Łączy się z podanym URL używając Selenium (Edge) w trybie stealth.
    Akceptuje zgody (jeśli się pojawią) i zapisuje kod HTML strony do pliku.
    
    Args:
        url (str): Adres strony do odwiedzenia
        nazwa_pliku (str): Nazwa pliku wyjściowego (HTML)
        verbose (bool): Czy wypisywać logi w konsoli
    """
    if verbose:
        print("Uruchamiam przeglądarkę Microsoft Edge...")
    
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    try:
        driver = webdriver.Edge(options=options)
        if verbose:
            print(f"Łączę się z: {url}")
        driver.get(url)
        
        # ZWIĘKSZAMY CZAS: Allegro potrzebuje chwili na załadowanie ofert
        if verbose:
            print("CZEKAM 30 SEKUND: Kliknij 'Akceptuję' i poczekaj na załadowanie ofert...")
        try:
            if verbose:
                print("Szukam przycisku zgód...")
            # Czekaj maksymalnie 15 sekund, aż przycisk będzie klikalny
            # Szukamy przycisku, który ma w tekście "kcept" (Akceptuję) lub "gadzam" (Zgadzam się)
            xpath_zgody = "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'kcept') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'gadzam')]"
            
            przycisk_akceptuj = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, xpath_zgody))
            )
            przycisk_akceptuj.click()
            if verbose:
                print("Kliknięto przycisk automatycznie!")
            
            # Po kliknięciu warto dać stronie 2-3 sekundy na przeładowanie ofert
            time.sleep(3) 
        except Exception as e:
            if verbose:
                print("Nie udało się kliknąć automatycznie (może przycisk się nie pojawił?):", e)
        
        if verbose:
            print("Pobieram kod strony...")
        html = driver.page_source
        
        # SPRAWDZAMY CZY POBRAŁO COŚ WIĘCEJ NIŻ PUSTĄ STRONĘ
        if len(html) < 1000:
            if verbose:
                print("Ostrzeżenie: Pobrany kod jest bardzo krótki. Możliwa blokada.")

        # USTALAMY PEŁNĄ ŚCIEŻKĘ DO PLIKU
        sciezka_pliku = os.path.join(os.getcwd(), nazwa_pliku)
        
        with open(sciezka_pliku, "w", encoding="utf-8") as f:
            f.write(html)
            
        if verbose:
            print("-" * 30)
            print(f"SUKCES! Plik został zapisany tutaj:")
            print(sciezka_pliku)  # To Ci powie dokładnie gdzie jest plik
            print(f"Rozmiar pliku: {os.path.getsize(sciezka_pliku)} bajtów")
            print("-" * 30)
        
    except Exception as e:
        if verbose:
            print(f"Wystąpił błąd podczas pracy: {e}")
    finally:
        if verbose:
            print("Zamykam przeglądarkę.")
        if 'driver' in locals():
            driver.quit()

def pobierz_dane_z_allegro(frazy, verbose=True):
    """
    Funkcja pomocnicza do pobierania pojedynczych stron dla listy fraz.
    (Może być używana do prostych testów bez paginacji).
    """
    if not frazy:
        if verbose:
            print("Nie znaleziono żadnych fraz w pliku produkt.txt!")
    else:
        if verbose:
            print(f"Znaleziono {len(frazy)} fraz do wyszukania.")

        for fraza in frazy:
            if verbose:
                print(f"\n--- Przetwarzam frazę: '{fraza}' ---")
            
            # Kodujemy frazę do URL (np. spacje na %20)
            encoded_fraza = urllib.parse.quote(fraza)
            
            # Tworzymy link do listy ofert (dodajemy parametr string=...)
            url = f'https://allegro.pl/listing?string={encoded_fraza}'
            
            # Tworzymy nazwe pliku allegro.html
            bezpieczna_nazwa = os.path.join("temp", "allegro.html")
            
            # Uruchamiamy pobieranie
            polacz_przez_edge_v2(url, nazwa_pliku=bezpieczna_nazwa, verbose=verbose)

        print("pobrano dane")

def pobierz_strone_allegro(fraza, numer_strony=1, verbose=False):
    """
    Pobiera i parsuje jedną stronę wyników Allegro dla danej frazy.
    """
    # Przygotuj URL z numerem strony
    encoded_fraza = urllib.parse.quote(fraza)
    url = f'https://allegro.pl/listing?string={encoded_fraza}&p={numer_strony}'
    
    # Nazwa pliku tymczasowego
    nazwa_pliku = os.path.join("temp", f"allegro_{numer_strony}.html")
    
    # Pobierz stronę
    polacz_przez_edge_v2(url, nazwa_pliku=nazwa_pliku, verbose=verbose)
    
    # Sparsuj
    tabela_nazwa = os.path.join("temp", f"allegro_{numer_strony}.html")
    if not os.path.exists(tabela_nazwa):
         return []
         
    nowe_oferty = parsuj_html(tabela_nazwa)
    
    # Dodajemy informację o szukanej frazie
    for oferta in nowe_oferty:
        oferta['search_query'] = fraza
        
    # Sprzątanie (opcjonalne, można zostawić do debugowania)
    # try:
    #     os.remove(tabela_nazwa)
    # except:
    #     pass
        
    return nowe_oferty

def uruchom_allegro(frazy, max_ofert=120, verbose=True):
    """
    Wersja zachowana dla kompatybilności, ale zaleca się używanie sterowania z main.py
    """
    print("\n" + "="*40)
    print(" ROZPOCZYNAM POBIERANIE Z ALLEGRO ")
    print("="*40)

    try:
        wszystkie_oferty = []
        
        if not frazy:
            if verbose:
                print("Brak fraz do wyszukania.")
            return []

        for fraza in frazy:
            if verbose:
                print(f"\n--- Przetwarzam Allegro: {fraza} ---")
            
            oferty_dla_frazy = []
            numer_strony = 1
            
            while len(oferty_dla_frazy) < max_ofert:
                if verbose:
                    print(f"\n--- Pobieram stronę {numer_strony} dla '{fraza}' ---")
                
                nowe_oferty = pobierz_strone_allegro(fraza, numer_strony, verbose=False)
                
                if not nowe_oferty:
                    if verbose:
                        print("Brak (więcej) ofert na tej stronie. Kończę pobieranie dla tej frazy.")
                    break
                    
                oferty_dla_frazy.extend(nowe_oferty)
                if verbose:
                    print(f"Pobrano {len(nowe_oferty)} ofert z tej strony. Razem mam: {len(oferty_dla_frazy)}")
                
                numer_strony += 1
                if numer_strony > 100: # Zabezpieczenie
                    break
            
            # Przytnij do limitu
            if len(oferty_dla_frazy) > max_ofert:
                oferty_dla_frazy = oferty_dla_frazy[:max_ofert]
                
            if verbose:
                print(f"Zakończono dla '{fraza}'. Zebrano łącznie {len(oferty_dla_frazy)} ofert.")
                
            wszystkie_oferty.extend(oferty_dla_frazy)

        return wszystkie_oferty

    except Exception as e:
        print(f"Wystąpił błąd w module Allegro: {e}")
        return []
