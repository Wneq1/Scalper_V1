from bs4 import BeautifulSoup
import re

def parsuj_html_vinted(plik_html="vinted.html"):
    """
    Parsuje plik HTML z Vinted.
    Wykorzystuje strukturę gdzie główne informacje (tytuł, cena, stan) są w atrybucie alt obrazka.
    """
    try:
        with open(plik_html, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except Exception as e:
        print(f"Błąd otwierania pliku Vinted: {e}")
        return []

    produkty = []
    
    # Szukamy kontenerów ofert
    items = soup.find_all("div", attrs={"data-testid": "grid-item"})
    
    for item in items:
        try:
            # Inicjalizacja zmiennych
            tytul = "Nieznany tytuł"
            marka = "Nieznana marka"
            stan = "Nieznany stan"
            cena_num = "0,00 zł"

            # 1. URL i Tytuł (jako fallback)
            link_tag = item.find("a", href=True)
            if not link_tag:
                continue
                
            url = link_tag['href']
            # Uzupełnij URL jeśli relatywny
            if not url.startswith("http"):
                url = "https://www.vinted.pl" + url
            
            # 2. Szukanie ceny w DOM (lepsze niż ALT)
            # Próbujemy znaleźć element z ceną
            # Vinted często używa <p> z konkretną klasą lub po prostu tekstu z walutą
            cena_dom = None
            
            # Szukamy elementu, który wygląda jak cena (zawiera "zł")
            price_candidates = item.find_all(["p", "h3", "h4", "span", "div"])
            for kandydat in price_candidates:
                txt = kandydat.get_text(strip=True)
                if "zł" in txt:
                    # Sprawdzamy czy to nie jest np. "wysyłka od 5 zł"
                    if "wysyłka" in txt.lower() or "dostawa" in txt.lower():
                        continue
                        
                    # Prosty regex do wyciągnięcia liczby
                    # Obsługuje spacje: "2 102,90 zł"
                    match_dom = re.search(r"(\d[\d\s]*[,.]?\d*)\s*zł", txt)
                    if match_dom:
                        cena_dom = match_dom.group(1).replace(" ", "").replace(",", ".")
                        break
            
            if cena_dom:
                cena_num = f"{cena_dom} zł"
            
            # 3. Dane z ALT obrazka (Tytuł, Marka, Stan, ewentualnie Cena fallback)
            img_tag = item.find("img")
            if img_tag and img_tag.get("alt"):
                alt_text = img_tag['alt']
                
                # Wyciąganie tytułu - zazwyczaj wszystko przed "marka:" lub pierwszym przecinkiem
                if "marka:" in alt_text:
                    tytul = alt_text.split("marka:")[0].strip().rstrip(",")
                else:
                    tytul = alt_text.split(",")[0].strip()
                
                # Wyciąganie marki
                match_marka = re.search(r"marka:\s*([^,]+)", alt_text)
                if match_marka:
                    marka = match_marka.group(1).strip()
                    
                # Wyciąganie stanu
                match_stan = re.search(r"stan:\s*([^,]+)", alt_text)
                if match_stan:
                    stan = match_stan.group(1).strip()
                
                # Cena z ALT (tylko jak nie znaleziono w DOM)
                if not cena_dom:
                    match_cena = re.search(r"(\d[\d\s]*[,.]?\d*)\s*z", alt_text)
                    if match_cena:
                        raw_c = match_cena.group(1).replace(" ", "")
                        cena_num = raw_c.replace(",", ".")
                        if cena_num.endswith("."): cena_num = cena_num[:-1]
                        cena_num = f"{cena_num} zł"
                    else:
                        # Ostatnia deska ratunku
                        parts = alt_text.split(",")
                        for part in parts:
                            if "z" in part and any(c.isdigit() for c in part) and "wysyłka" not in part:
                                    cena_raw = "".join(c for c in part if c.isdigit() or c == ',')
                                    if cena_raw:
                                        cena_num = f"{cena_raw.replace(',', '.')} zł"
                                        break

            # Filtrowanie "śmieci" (np. ubrań z nazwą RTX)
            BLOCKED_BRANDS = ["pro rtx", "rtx pro", "rtx"]
            BLOCKED_KEYWORDS = ["bluza", "koszulka", "t-shirt", "spodnie", "kurtka", "czapka"]
            
            # Sprawdzenie marki
            if marka.lower() in BLOCKED_BRANDS:
                continue

            # Sprawdzenie słów kluczowych w tytule
            if any(keyword in tytul.lower() for keyword in BLOCKED_KEYWORDS):
                continue

            produkty.append({
                "title": tytul,
                "price": cena_num,
                "condition": stan,
                "source": "Vinted",
                "url": url,
                "brand": marka # Dodatkowo
            })
            
        except Exception as e:
            print(f"Błąd parsowania oferty Vinted: {e}") 
            continue
            
    return produkty
