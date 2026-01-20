from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import urllib.parse
from .parser import parsuj_html_amazon

def polacz_z_amazonem(url, nazwa_pliku="amazon.html", verbose=True):
    """
    Łączy się z Amazon używając Selenium (Edge) i zapisuje HTML.
    """
    if verbose:
        print(f"Uruchamiam przeglądarkę dla Amazon: {url}")
    
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Opcjonalnie: options.add_argument("--headless=new")
    
    driver = None
    try:
        driver = webdriver.Edge(options=options)
        driver.get(url)
        
        if verbose:
            print("Czekam na załadowanie strony Amazon...")
        
        # Amazon może wymagać Captcha, ale przy zwykłym uruchomieniu często przechodzi.
        # Sprawdzamy zgody cookies "sp-cc-accept"
        try:
            xpath_cookies = "//input[@id='sp-cc-accept']"
            przycisk = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.XPATH, xpath_cookies))
            )
            przycisk.click()
            if verbose:
                print("Zaakceptowano cookies Amazon.")
            time.sleep(2)
        except:
            pass # Może nie być cookies
            
        # Poczekaj chwilę na render produktów
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(2)
        
        html = driver.page_source
        
        sciezka = os.path.join(os.getcwd(), nazwa_pliku)
        with open(sciezka, "w", encoding="utf-8") as f:
            f.write(html)
            
        if verbose:
            print(f"Zapisano Amazon HTML: {sciezka}")
            
    except Exception as e:
        if verbose:
            print(f"Błąd Amazon Selenium: {e}")
    finally:
        if driver:
            driver.quit()

def pobierz_strone_amazon(fraza, numer_strony=1, verbose=False):
    """
    Pobiera i parsuje jedną stronę wyników Amazon.
    """
    # URL Amazon: https://www.amazon.pl/s?k={query}&page={page}
    encoded = urllib.parse.quote(fraza)
    url = f"https://www.amazon.pl/s?k={encoded}&page={numer_strony}"
    
    nazwa_pliku = os.path.join("temp", f"amazon_{numer_strony}.html")
    polacz_z_amazonem(url, nazwa_pliku, verbose)
    
    if not os.path.exists(nazwa_pliku):
        return []
        
    oferty = parsuj_html_amazon(nazwa_pliku)
    for o in oferty:
        o['search_query'] = fraza
        
    return oferty

def uruchom_amazon(frazy, max_ofert=20, verbose=True):
    print("\n" + "="*40)
    print(" ROZPOCZYNAM POBIERANIE Z AMAZON ")
    print("="*40)
    
    wszystkie_oferty = []
    
    for fraza in frazy:
        oferty_dla_frazy = []
        numer_strony = 1
        
        while len(oferty_dla_frazy) < max_ofert:
            nowe = pobierz_strone_amazon(fraza, numer_strony, verbose=False)
            if not nowe:
                break
                
            oferty_dla_frazy.extend(nowe)
            if verbose:
                print(f"Pobrano {len(nowe)} ofert z Amazon (strona {numer_strony}). Razem: {len(oferty_dla_frazy)}")
            
            numer_strony += 1
            if numer_strony > 20: break
            
        oferty_dla_frazy = oferty_dla_frazy[:max_ofert]
        wszystkie_oferty.extend(oferty_dla_frazy)
            
    return wszystkie_oferty
