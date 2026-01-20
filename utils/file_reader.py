import os

def czytaj_szukane_frazy(nazwa_pliku="produkt.txt"):
    """
    Funkcja wczytuje szukane frazy (produkty) z pliku tekstowego.
    Jeśli plik nie istnieje, tworzy go automatycznie z przykładowymi danymi,
    aby użytkownik wiedział jak go uzupełnić.
    
    Args:
        nazwa_pliku (str): Ścieżka do pliku z frazami (domyślnie 'produkt.txt')
        
    Returns:
        list: Lista fraz do wyszukania (np. ["rtx 4060", "konsola ps5"])
    """
    
    # Sprawdzamy, czy plik o podanej nazwie fizycznie istnieje na dysku
    if not os.path.exists(nazwa_pliku):
        # Jeśli plik nie istnieje, tworzymy go w trybie zapisu ("w" - write)
        # Dzięki temu użytkownik nie dostanie błędu "File not found" przy starcie
        with open(nazwa_pliku, "w", encoding="utf-8") as f:
            # Wpisujemy przykładowe produkty, każdy w nowej linii (\n to znak nowej linii)
            f.write("rtx 4060\nrtx 3060")
        
        # Informujemy użytkownika o utworzeniu pliku
        print(f"Utworzono plik {nazwa_pliku}. Wpisz tam swoje produkty.")
    
    # Otwieramy plik w trybie odczytu ("r" - read)
    with open(nazwa_pliku, "r", encoding="utf-8") as f:
        # readlines() wczytuje wszystkie linie do listy
        # linia.strip() usuwa białe znaki z początku i końca (np. spacje, entery)
        # if linia.strip() sprawdza, czy linia nie jest pusta (żeby nie szukać pustych napisów)
        frazy = [linia.strip() for linia in f.readlines() if linia.strip()]
        
    # Zwracamy gotową listę fraz
    return frazy