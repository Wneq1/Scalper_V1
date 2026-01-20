from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
import os
import urllib.parse
from .parser import parsuj_html_allegrolokalnie

def polacz_z_allegrolokalnie(url, nazwa_pliku="allegrolokalnie.html", verbose=True):
    """
    Łączy się z Allegro Lokalnie przy użyciu Selenium.
    """
    if verbose:
        print(f"Uruchamiam przeglądarkę dla Allegro Lokalnie: {url}")
    
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Opcjonalnie: options.add_argument("--headless=new")

    driver = None
    try:
        driver = webdriver.Edge(options=options)
        driver.get(url)
        
        # Czas na załadowanie
        time.sleep(4)
        
        # Scrollowanie
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        
        html = driver.page_source
        
        sciezka_pliku = os.path.join(os.getcwd(), nazwa_pliku)
        with open(sciezka_pliku, "w", encoding="utf-8") as f:
            f.write(html)
            
        if verbose:
            print(f"Zapisano HTML: {sciezka_pliku}")
            
    except Exception as e:
        if verbose:
            print(f"Błąd Allegro Lokalnie: {e}")
    finally:
        if driver:
            driver.quit()

def pobierz_strone_allegrolokalnie(fraza, numer_strony=1, verbose=False):
    """
    Pobiera i parsuje jedną stronę wyników Allegro Lokalnie.
    """
    # URL pattern: https://allegrolokalnie.pl/oferty/q/{query}?page={numer}
    encoded = urllib.parse.quote(fraza)
    url = f"https://allegrolokalnie.pl/oferty/q/{encoded}?page={numer_strony}"
    
    nazwa_pliku = os.path.join("temp", f"allegrolokalnie_{numer_strony}.html")
    polacz_z_allegrolokalnie(url, nazwa_pliku, verbose)
    
    if not os.path.exists(nazwa_pliku):
        return []
        
    oferty = parsuj_html_allegrolokalnie(nazwa_pliku)
    for o in oferty:
        o['search_query'] = fraza
        
    return oferty

def uruchom_allegrolokalnie(frazy, max_ofert=20, verbose=True):
    print("\n" + "="*40)
    print(" ROZPOCZYNAM POBIERANIE Z ALLEGRO LOKALNIE ")
    print("="*40)
    
    wszystkie_oferty = []
    
    for fraza in frazy:
        oferty_dla_frazy = []
        numer_strony = 1
        
        while len(oferty_dla_frazy) < max_ofert:
            nowe = pobierz_strone_allegrolokalnie(fraza, numer_strony, verbose=False)
            if not nowe:
                break
                
            oferty_dla_frazy.extend(nowe)
            if verbose:
                print(f"Pobrano {len(nowe)} ofert z Allegro Lokalnie (strona {numer_strony}). Razem: {len(oferty_dla_frazy)}")
            
            numer_strony += 1
            if numer_strony > 20: break
            
        oferty_dla_frazy = oferty_dla_frazy[:max_ofert]
        wszystkie_oferty.extend(oferty_dla_frazy)
            
    return wszystkie_oferty
