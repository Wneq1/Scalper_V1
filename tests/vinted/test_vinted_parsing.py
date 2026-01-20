from parsuj_vinted import parsuj_html_vinted
import os

def test_vinted_parsing():
    if not os.path.exists("vinted.html"):
        print("Brak pliku vinted.html - pominiecie testu")
        return

    print("--- Testowanie parsowania Vinted ---")
    produkty = parsuj_html_vinted("vinted.html")
    
    print(f"Znaleziono {len(produkty)} produktow.")
    if produkty:
        print("Pierwsze 3 produkty:")
        for p in produkty[:3]:
            print(p)
            
    # Simple assertions
    assert len(produkty) > 0, "Powinno znaleźć produkty"
    assert "title" in produkty[0], "Produkt musi mieć tytuł"
    assert "price" in produkty[0], "Produkt musi mieć cenę"
    print("\nTest parsowania Vinted: SUKCES")

if __name__ == "__main__":
    test_vinted_parsing()
