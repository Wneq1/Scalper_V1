from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
# Importujemy funkcję parsującą (analizującą) HTML z pliku obok
from .parser import parsuj_html_vinted

def polacz_z_vinted(url, nazwa_pliku="vinted.html", verbose=True):
    """
    Łączy się z Vinted używając przeglądarki Edge (Selenium).
    Vinted wymaga JavaScript, dlatego zwykłe pobranie (requests) nie wystarczy.
    """
    if verbose:
        print("Uruchamiam przeglądarkę dla Vinted...")
    
    # Konfigurujemy przeglądarkę
    options = Options()
    # Ukrywamy fakt, że to bot (AutomationControlled) - pomaga ominąć proste blokady
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    try:
        # Uruchamiamy przeglądarkę
        driver = webdriver.Edge(options=options)
        driver.get(url)
        
        if verbose:
            print("Czekam na załadowanie strony Vinted (10s)...")
        # Vinted bywa wolne, czekamy chwilę na wczytanie skryptów
        time.sleep(5) 

        # --- OBSŁUGA PLIKÓW COOKIE ---
        # Większość stron wyświetla popup "Zaakceptuj pliki cookie". Musimy go kliknąć, żeby odsłonić treść.
        try:
            xpath_cookies = "//button[@id='onetrust-accept-btn-handler']"
            # Czekamy max 5 sekund aż przycisk się pojawi i będzie klikalny
            przycisk = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath_cookies))
            )
            przycisk.click()
            if verbose:
                print("Zaakceptowano cookies Vinted.")
            time.sleep(2)
        except:
            # Jeśli błąd, to znaczy że przycisk się nie pojawił lub jest inny ID. Ignorujemy i próbujemy dalej.
            if verbose:
                print("Nie znaleziono/kliknięto cookies (może nie wyskoczyły).")

        # --- SCROLLOWANIE (PRZEWIJANIE) ---
        # Vinted często doczytuje oferty dopiero jak zjedziemy na dół strony (tzw. lazy loading).
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        
        # Pobieramy gotowy kod HTML strony
        html = driver.page_source
        
        # Zapisujemy kod do pliku
        sciezka_pliku = os.path.join(os.getcwd(), nazwa_pliku)
        with open(sciezka_pliku, "w", encoding="utf-8") as f:
            f.write(html)
            
        if verbose:
            print(f"Zapisano Vinted HTML: {sciezka_pliku}")
            
    except Exception as e:
        if verbose:
            print(f"Błąd Vinted: {e}")
    finally:
        # Zawsze zamykamy przeglądarkę na końcu, żeby nie wisiała w tle
        if 'driver' in locals():
            driver.quit()

def pobierz_strone_vinted(fraza, numer_strony=1, verbose=False):
    """
    Pobiera i parsuje jedną stronę wyników Vinted.
    """
    # URL Vinted: https://www.vinted.pl/catalog?search_text=fraza&page=numer
    encoded = urllib.parse.quote(fraza)
    url = f"https://www.vinted.pl/catalog?search_text={encoded}&page={numer_strony}"
    
    path_html = os.path.join("temp", f"vinted_{numer_strony}.html")
    polacz_z_vinted(url, path_html, verbose)
    
    if not os.path.exists(path_html):
        return []
        
    oferty = parsuj_html_vinted(path_html)
    for o in oferty:
        o['search_query'] = fraza
        
    return oferty

def uruchom_vinted(frazy, max_ofert=20, verbose=True):
    """
    Główna funkcja modułu Vinted (kompatybilność wsteczna).
    """
    print("\n" + "="*40)
    print(" ROZPOCZYNAM POBIERANIE Z VINTED ")
    print("="*40)
    
    wszystkie_oferty = []
    
    for fraza in frazy:
        oferty_dla_frazy = []
        numer_strony = 1
        
        while len(oferty_dla_frazy) < max_ofert:
            nowe = pobierz_strone_vinted(fraza, numer_strony, verbose=False)
            if not nowe:
                break
                
            oferty_dla_frazy.extend(nowe)
            if verbose:
                print(f"Pobrano {len(nowe)} ofert z Vinted (strona {numer_strony}). Razem: {len(oferty_dla_frazy)}")
            
            numer_strony += 1
            if numer_strony > 20: break
            
        # Przycinamy
        oferty_dla_frazy = oferty_dla_frazy[:max_ofert]
        wszystkie_oferty.extend(oferty_dla_frazy)
            
    return wszystkie_oferty
