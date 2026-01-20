from bs4 import BeautifulSoup
import os
import re

def parsuj_html_amazon(plik_html="amazon.html"):
    """
    Parsuje lokalny plik HTML z Amazon.pl
    """
    if not os.path.exists(plik_html):
        return []

    print(f"Parsuję Amazon: {plik_html}")
    
    with open(plik_html, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        
    produkty = []
    
    # Kontenerem pojedynczego wyniku jest zazwyczaj div z atrybutem data-component-type="s-search-result"
    wyniki = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
    
    for wynik in wyniki:
        try:
            # 1. Tytuł - zazwyczaj w h2
            tytul = "Brak tytułu"
            h2 = wynik.find("h2")
            if h2:
                tytul = h2.get_text(strip=True)
            
            # 2. Link
            link = "Brak linku"
            if h2:
                # Sprawdź czy a jest wewnątrz h2
                a_tag = h2.find("a")
                if not a_tag:
                    # Sprawdź czy a jest rodzicem h2 (częsty przypadek na Amazon)
                    if h2.parent.name == "a":
                        a_tag = h2.parent
                
                if a_tag and a_tag.get('href'):
                    href = a_tag['href']
                    if href.startswith("/"):
                        link = "https://www.amazon.pl" + href
                    else:
                        link = href
            
            # 3. Cena
            cena = "Sprawdź cenę"
            
            price_container = wynik.find(class_="a-price")
            if price_container:
                # Metoda 1: a-offscreen (tekst dla screen readerów)
                offscreen = price_container.find(class_="a-offscreen")
                if offscreen:
                    # np. "1 921,69 zł" (ze spacjami nierozdzielającymi)
                    raw_cena = offscreen.get_text(strip=True)
                    # Usuwamy "zł", spacje i nbsp
                    # Zmieniamy na wielkie litery, żeby usunąć ZŁ i zŁ
                    clean_c = raw_cena.upper().replace("ZŁ", "").replace("ZL", "").replace("\xa0", "").replace(" ", "")
                    
                    # Logika dla separatorów (Amazon PL: przecinek to grosze, kropka to czasem tysiące)
                    # Jeśli jest i kropka i przecinek, usuwamy kropkę (tysiące)
                    if "." in clean_c and "," in clean_c:
                        clean_c = clean_c.replace(".", "")
                    
                    # Jeśli jest tylko kropka i ma 2 cyfry po niej (np. 129.99), zamieniamy na przecinek
                    # Ale bezpieczniej zostawić kropkę, Excel Handler sobie poradzi (zamienia przecinek na kropkę)
                    
                    cena = f"{clean_c} zł"
                else:
                    # Fallback
                    whole = price_container.find(class_="a-price-whole")
                    fraction = price_container.find(class_="a-price-fraction")
                    
                    if whole:
                        # Cleaning: remove dots (thousands sep in some locales), spaces
                        c_calosc = whole.get_text(strip=True).replace(".", "").replace(",", "")
                        c_ułamek = fraction.get_text(strip=True) if fraction else "00"
                        cena = f"{c_calosc},{c_ułamek} zł"
            
            # Cleaning ceny z waluty i spacji, żeby excel ładnie przyjął (opcjonalnie, bo obsluga_excela to robi)
            # Ale tutaj tylko zwracamy stringa
            
            produkty.append({
                "title": tytul,
                "price": cena,
                "url": link,
                "condition": "Nowy", # Amazon to głównie nówki, chyba że Warehouse
                "source": "Amazon"
            })
            
        except Exception as e:
            # print(f"Błąd parsowania oferty Amazon: {e}")
            continue
            
    return produkty
