# Korzystamy z gotowej funkcji łączenia się przez Selenium z modułu Allegro,
# ponieważ mechanizm pobierania strony jest bardzo podobny.
from modules.allegro.fetcher import polacz_przez_edge_v2
from .parser import parsuj_html_olx
import urllib.parse
import os

def pobierz_strone_olx(fraza, numer_strony=1, verbose=False):
    """
    Pobiera i parsuje jedną stronę wyników OLX.
    """
    # Budowanie adresu URL dla OLX
    fraza_dashed = fraza.strip().replace(" ", "-")
    encoded_fraza = urllib.parse.quote(fraza_dashed)
    
    url = f'https://www.olx.pl/oferty/q-{encoded_fraza}/?page={numer_strony}'
    
    path_html = os.path.join("temp", f"olx_{numer_strony}.html")
    polacz_przez_edge_v2(url, nazwa_pliku=path_html, verbose=verbose)
    
    if not os.path.exists(path_html):
        return []

    nowe_oferty = parsuj_html_olx(path_html)
    
    for oferta in nowe_oferty:
        oferta['search_query'] = fraza
        
    return nowe_oferty

def uruchom_olx(frazy, max_ofert=50, verbose=True):
    """
    Główna funkcja sterująca pobieraniem z OLX.
    Generuje odpowiednie adresy URL i pobiera kolejne strony wyników.
    """
    print("\n" + "="*40)
    print(" ROZPOCZYNAM POBIERANIE Z OLX ")
    print("="*40)
    
    try:
        wszystkie_oferty = []
        
        if not frazy:
            return []

        for fraza in frazy:
            if verbose:
                print(f"\n--- Przetwarzam OLX: {fraza} ---")
            
            oferty_dla_frazy = []
            numer_strony = 1
            
            # Pętla pobierająca kolejne strony wyników (paginacja), dopóki nie osiągniemy limitu max_ofert
            while len(oferty_dla_frazy) < max_ofert:
                if verbose:
                    print(f"\n--- Pobieram stronę {numer_strony} OLX dla '{fraza}' ---")
                
                nowe_oferty = pobierz_strone_olx(fraza, numer_strony, verbose=False)
                
                # Jeśli funkcja parsująca nie zwróciła żadnych ofert, to znaczy, że strony się skończyły
                if not nowe_oferty:
                    if verbose:
                        print("Brak (więcej) ofert na tej stronie OLX.")
                    break
                    
                # Dodajemy nowe oferty do listy wyników dla tej frazy
                oferty_dla_frazy.extend(nowe_oferty)
                if verbose:
                    print(f"Pobrano {len(nowe_oferty)} ofert z OLX. Razem: {len(oferty_dla_frazy)}")
                
                numer_strony += 1
                # Zabezpieczenie przed pętlą nieskończoną - max 20 stron
                if numer_strony > 20: 
                    break
                    
            # Jeśli pobraliśmy więcej niż limit, przycinamy listę
            if len(oferty_dla_frazy) > max_ofert:
                oferty_dla_frazy = oferty_dla_frazy[:max_ofert]
                
            # Dodajemy wyniki z tej frazy do głównej listy wszystkich ofert
            wszystkie_oferty.extend(oferty_dla_frazy)
            
        return wszystkie_oferty

    except Exception as e:
        print(f"Wystąpił błąd w module OLX: {e}")
        return []

