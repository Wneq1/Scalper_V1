from bs4 import BeautifulSoup
import re

def parsuj_html(plik_html="allegro.html"):
    """
    Parsuje plik HTML z Allegro i zwraca listę produktów.
    Wykorzystuje bibliotekę BeautifulSoup do analizy struktury DOM.
    
    Args:
        plik_html (str): Ścieżka do pliku HTML do sparsowania.
        
    Returns:
        list: Lista słowników, gdzie każdy słownik to jedna oferta (tytuł, cena, url itp.)
    """
    print(f"Parsuję plik: {plik_html}...")
    
    try:
        with open(plik_html, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except FileNotFoundError:
        print(f"Błąd: Plik {plik_html} nie istnieje. Pominiecie parsowania.")
        return []

    produkty = []
    
    # Allegro zazwyczaj trzyma oferty w tagach <article>
    artykuly = soup.find_all("article")
    
    print(f"Znaleziono {len(artykuly)} potencjalnych ofert.")

    for art in artykuly:
        try:
            # 1. Tytuł: zazwyczaj znajduje się w nagłówku <h2> lub bezpośrednio w linku <a>
            # Musimy obsłużyć oba przypadki, bo struktura Allegro się zmienia
            tytul_element = art.find("h2")
            if tytul_element:
                tytul = tytul_element.get_text(strip=True)
            else:
                # Alternatywne miejsce: tekst wewnątrz linku
                link_elem = art.find("a")
                if link_elem:
                    tytul = link_elem.get_text(strip=True)
                else:
                    tytul = "Brak tytułu"

            # 2. Cena - szukamy elementu z ceną
            cena = "Brak ceny"
            uwagi = ""
            
            # Strategia 1: Szukamy po aria-label "aktualna cena" (najbardziej wiarygodne na Allegro)
            # np. aria-label="3 099,00 zł aktualna cena"
            cena_aria = art.find(attrs={"aria-label": lambda L: L and "aktualna cena" in L})
            if cena_aria:
                tekst_aria = cena_aria['aria-label']
                # Wyciągamy liczby
                match = re.search(r'([\d\s,]+)\s*zł', tekst_aria)
                if match:
                    cena_czysta = match.group(1).strip().replace(" ", "").replace(",", ".")
                    cena = cena_czysta
            
            # Strategia 2 (Fallback): Stara metoda przeszukiwania tekstu
            if cena == "Brak ceny":
                elementy_z_cena = art.find_all(string=lambda text: "zł" in text if text else False)
                if elementy_z_cena:
                    for el in elementy_z_cena:
                        tekst_brudny = el.strip()
                        
                        # Ignorujemy oferty ratalne (np. "x 30 rat")
                        if "rat" in tekst_brudny.lower():
                            continue

                        # Sprawdzamy czy to wygląda na cenę (ma cyfry)
                        if any(char.isdigit() for char in tekst_brudny):
                            match = re.search(r'([\d\s,]+)\s*zł\s*(.*)', tekst_brudny)
                            if match:
                                cena_czysta = match.group(1).strip()
                                cena_czysta = cena_czysta.replace(" ", "").replace(",", ".")
                                uwagi_reszta = match.group(2).strip()
                                
                                cena = cena_czysta
                                uwagi = uwagi_reszta
                                break # Znaleziono sensowną cenę
            
            # 3. Stan (Nowy/Używany)
            stan = "Nieznany"
            try:
                # Szukamy elementu <dt> z tekstem "Stan"
                stan_label = art.find("dt", string=lambda x: x and "Stan" in x)
                if stan_label:
                    # Szukamy następnego rodzeństwa <dd>
                    stan_wartosc = stan_label.find_next_sibling("dd")
                    if stan_wartosc:
                        stan = stan_wartosc.get_text(strip=True)
            except:
                pass

            # 4. Link
            link_element = art.find("a", href=True)
            if link_element:
                link = link_element['href']
                # Linki mogą być relatywne
                if not link.startswith("http"):
                    link = "https://allegro.pl" + link
            else:
                link = "Brak linku"

            produkty.append({
                "title": tytul,
                "price": cena,
                "condition": stan,
                "info": uwagi,
                "url": link
            })
            
        except Exception as e:
            print(f"Błąd przy parsowaniu oferty: {e}")
            continue

    return produkty
