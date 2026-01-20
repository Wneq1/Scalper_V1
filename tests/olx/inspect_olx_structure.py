
from bs4 import BeautifulSoup

def inspect_olx_structure():
    """
    Funkcja pomocnicza (debug) do sprawdzania konkretnych elementów 'card' w HTML OLX.
    Pomaga ustalić, jak wyglądają dane pojedynczego ogłoszenia w kodzie.
    """
    with open("olx.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    card = soup.find("div", attrs={"data-cy": "l-card"})
    if card:
        print("--- Karta znaleziona ---")
        print(card.prettify()[:1000]) # Print first 1000 chars of the card
    else:
        print("Nie znaleziono karty z data-cy='detail-card'")

if __name__ == "__main__":
    inspect_olx_structure()
