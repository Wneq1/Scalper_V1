from bs4 import BeautifulSoup
import json
import re

def parsuj_html_allegrolokalnie(plik_html="allegrolokalnie.html"):
    """
    Parsuje plik HTML z Allegro Lokalnie wykorzystując JSON-LD.
    Zwraca listę produktów.
    """
    print(f"Parsuję Allegro Lokalnie: {plik_html}...")
    
    try:
        with open(plik_html, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except Exception as e:
        print(f"Błąd otwierania pliku Allegro Lokalnie: {e}")
        return []
        
    produkty = []
    
    # Szukamy skryptów JSON-LD
    scripts = soup.find_all("script", type="application/ld+json")
    
    for script in scripts:
        try:
            content = script.string
            if not content:
                continue
                
            data = json.loads(content)
            
            # Szukamy obiektu ItemList
            if isinstance(data, dict) and data.get("@type") == "ItemList":
                items = data.get("itemListElement", [])
                
                for entry in items:
                    item = entry.get("item", {})
                    
                    # Tytuł
                    tytul = item.get("name", "Brak tytułu")
                    
                    # URL
                    url = item.get("url", "")
                    
                    # Cena
                    offers = item.get("offers", {})
                    cena_raw = offers.get("price", "0")
                    # Upewnij się że cena to string
                    cena = str(cena_raw).replace(",", ".")
                    
                    # Stan
                    # "itemCondition": "https://schema.org/UsedCondition"
                    cond_url = item.get("itemCondition", "")
                    stan = "Nieznany"
                    if "NewCondition" in cond_url:
                        stan = "Nowy"
                    elif "UsedCondition" in cond_url:
                        stan = "Używany"
                    
                    produkty.append({
                        "title": tytul,
                        "price": cena,
                        "condition": stan,
                        "source": "Allegro Lokalnie",
                        "url": url,
                        "info": "" 
                    })
                
                # Jeśli znaleźliśmy ItemList, to przerywamy (zazwyczaj jest jeden główny)
                # break - USUWAMY TO, BO MOŻE BYĆ WIĘCEJ LIST (np. promowane i zwykłe)
                pass
                
        except Exception as e:
            # print(f"Błąd parsowania JSON-LD: {e}")
            continue
            
    return produkty
