
import os
from parsuj_allegro import parsuj_html
from parsuj_olx import parsuj_html_olx

def test_parsing():
    """
    Funkcja testowa do szybkiego sprawdzania parsowania.
    Działa na lokalnych plikach 'allegro.html' i 'olx.html' (jeśli istnieją),
    bez konieczności uruchamiania przeglądarki.
    """
    print("--- TESTOWANIE PARSOWANIA ---")
    
    # Test Allegro
    print("\n1. Sprawdzam Allegro...")
    if os.path.exists("allegro.html"):
        wyniki_allegro = parsuj_html("allegro.html")
        print(f"Wynik Allegro: znaleziono {len(wyniki_allegro)} ofert.")
        if wyniki_allegro:
            print(f"Przykładowa oferta: {wyniki_allegro[0]}")
    else:
        print("Brak pliku allegro.html")

    # Test OLX
    print("\n2. Sprawdzam OLX...")
    if os.path.exists("olx.html"):
        wyniki_olx = parsuj_html_olx("olx.html")
        print(f"Wynik OLX: znaleziono {len(wyniki_olx)} ofert.")
        if wyniki_olx:
            print(f"Przykładowa oferta: {wyniki_olx[0]}")
    else:
        print("Brak pliku olx.html")

if __name__ == "__main__":
    test_parsing()
