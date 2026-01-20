from bs4 import BeautifulSoup

def inspect_olx_html():
    """
    Funkcja pomocnicza (debug) do analizy struktury HTML pliku z OLX.
    Wypisuje fragmenty kodu strony, aby ułatwić znalezienie odpowiednich tagów.
    """
    try:
        with open("olx.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            
        card = soup.find("div", attrs={"data-cy": "l-card"})
        if card:
            print("--- Found Card ---")
            print(card.prettify())
        else:
            print("No card with data-cy='l-card' found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        with open("olx.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            
        card = soup.find("div", attrs={"data-cy": "l-card"})
        if card:
            # Print first 30 lines of prettified html
            print("\n".join(card.prettify().splitlines()[:50]))
            
            # Check for header tags
            for h in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                headers = card.find_all(h)
                if headers:
                    print(f"\nFound {h} tags:")
                    for header in headers:
                        print(header)
        else:
            print("No card found")
    except Exception as e:
        print(f"Error: {e}")
