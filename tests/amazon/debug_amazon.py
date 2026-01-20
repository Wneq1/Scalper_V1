import sys
import os
# Must go up 3 levels: tests/amazon/debug_amazon.py -> tests/amazon -> tests -> scalper
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules.amazon.parser import parsuj_html_amazon
import os

def debug():
    if not os.path.exists("amazon.html"):
        print("Brak pliku amazon.html")
        return

    produkty = parsuj_html_amazon("amazon.html")
    print(f"Znaleziono {len(produkty)} produktów.")
    for i, p in enumerate(produkty[:5]):
        print(f"--- PARSED ITEM {i} ---")
        print(f"Title: {p.get('title')}")
        print(f"Price: {p.get('price')}")
        print(f"Link: {p.get('url')}")


    import bs4
    with open("amazon.html", "r", encoding="utf-8") as f:
        soup = bs4.BeautifulSoup(f, "html.parser")
    
    wyniki = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
    print(f"DEBUG: Found {len(wyniki)} items.")
    
    for i, wynik in enumerate(wyniki[:5]):
        print(f"--- ITEM {i} ---")
        h2 = wynik.find("h2")
        if h2:
            print(f"H2 found. Parent: {h2.parent.name}")
            print(f"H2 children: {[c.name for c in h2.children if c.name]}")
            # Check if 'a' is a parent
            curr = h2
            link_found = None
            while curr and curr.name != "div":
                if curr.name == "a":
                    link_found = curr
                    break
                curr = curr.parent
            print(f"Link found via parent traversal: {link_found.get('href') if link_found else 'None'}")
            
            # Alternative: find first 'a' inside h2 usually works, but if not:
            atag = h2.find("a")
            print(f"Link direct child: {atag.get('href') if atag else 'None'}")
        else:
            print("No H2 found")
        
        price = wynik.find(class_="a-price")
        if price:
            # print(f"Price HTML: {price}")
            offscreen = price.find(class_="a-offscreen")
            print(f"Offscreen Price: {offscreen.get_text(strip=True) if offscreen else 'None'}")

if __name__ == "__main__":
    debug()
