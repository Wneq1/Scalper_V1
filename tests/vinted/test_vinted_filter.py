
from parsuj_vinted import parsuj_html_vinted

def test_filtering():
    print("Testing Vinted filtering...")
    # Parsuj istniejący plik vinted.html
    try:
        oferty = parsuj_html_vinted("vinted.html")
    except Exception as e:
        print(f"Error parsing file: {e}")
        return

    # Sprawdź czy jest czarna bluza
    znaleziono_bluze = False
    for oferta in oferty:
        if "bluza" in oferta['title'].lower() or "pro rtx" in oferta.get('brand', '').lower():
            print(f"FAILED: Found banned item: {oferta['title']} (Brand: {oferta.get('brand')})")
            znaleziono_bluze = True
    
    if not znaleziono_bluze:
        print("SUCCESS: No black sweatshirt or 'Pro rtx' items found.")
        print(f"Total valid items found: {len(oferty)}")

if __name__ == "__main__":
    test_filtering()
