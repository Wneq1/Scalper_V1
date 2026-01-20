from bs4 import BeautifulSoup

def parsuj_html_olx(plik_html="olx.html"):
    """
    Parsuje plik HTML z OLX.
    Szuka kart ogłoszeń oznaczonych jako 'l-card' i wyciąga z nich tytuł, cenę oraz link.
    """
    try:
        with open(plik_html, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except Exception as e:
        print(f"Błąd otwierania pliku: {e}")
        return []

    produkty = []
    # Szukamy kart ogłoszeń
    oferty = soup.find_all("div", attrs={"data-cy": "l-card"})

    for oferta in oferty:
        try:
            # 1. Tytuł - zazwyczaj w h6, ale czasem h4 lub w alt obrazka
            title_elem = oferta.find("h6")
            if not title_elem:
                title_elem = oferta.find("h4")

            if title_elem:
                tytul = title_elem.get_text(strip=True)
            else:
                # Fallback: szukamy w alt obrazka
                img_elem = oferta.find("img")
                if img_elem and img_elem.get('alt'):
                    tytul = img_elem['alt']
                else:
                    tytul = "Brak tytułu"

            # 2. Szukamy ceny
            cena_tag = oferta.find("p", attrs={"data-testid": "ad-price"})
            cena = cena_tag.get_text(strip=True) if cena_tag else "0"
            # Czyścimy cenę (zostawiamy cyfry i kropkę)
            cena_text = cena.replace(",", ".")
            cena_num = "".join(c for c in cena_text if c.isdigit() or c == '.')

            # 3. Stan (Nowe/Używane)
            stan = "Nieznany"
            if "używ" in oferta.get_text(strip=True).lower():
                stan = "Używane"
            elif "now" in oferta.get_text(strip=True).lower():
                stan = "Nowe"
            
            # Próba dokładniejszego wyciągnięcia z tagu title, jeśli istnieje
            possible_conditions = oferta.find_all(attrs={"title": True})
            for pc in possible_conditions:
                if pc['title'] in ["Używane", "Nowe"]:
                    stan = pc['title']
                    break

            # 4. Szukamy linku
            link_tag = oferta.find("a", href=True)
            link = link_tag['href'] if link_tag else ""
            if link.startswith("/"):
                link = "https://www.olx.pl" + link

            produkty.append({
                "title": tytul,
                "price": cena_num,
                "condition": stan,
                "url": link,
                "source": "OLX"
            })
        except:
            continue
            
    return produkty