from bs4 import BeautifulSoup
import os

def inspect():
    with open("vinted.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    items = soup.find_all("div", attrs={"data-testid": "grid-item"})
    if not items:
        return

    item = items[0]
    print("--- ITEM STRUCTURE ---")
    
    # URL
    link = item.find("a", href=True)
    if link:
        print(f"URL: {link['href']}")
        print(f"URL Title: {link.get('title')}")
    else:
        print("Brak linku <a>")

    # Title
    # Helper to print class and text
    for child in item.find_all(recursive=True):
        if child.name in ['p', 'h2', 'h4', 'span', 'div']:
             txt = child.get_text(strip=True)
             if txt and len(txt) < 100:
                 # Check if it looks like title or price
                 print(f"Tag: {child.name}, Class: {child.get('class')}, Text: {txt}")

    # Image Alt
    img = item.find("img")
    if img:
        print(f"IMG ALT: {img.get('alt')}")

if __name__ == "__main__":
    inspect()
