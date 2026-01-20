from obsluga_excela import zapisz_dane_do_excela
import os

# Sample data with varied conditions to test gradient
dane_testowe = [
    {"title": "Produkt 1 - Nowy z metką", "price": 100.0, "condition": "Nowy z metką", "source": "Test", "url": "http://example.com/1"},
    {"title": "Produkt 2 - Nowy", "price": 110.0, "condition": "Nowe", "source": "Test", "url": "http://example.com/2"},
    {"title": "Produkt 3 - Bez metki", "price": 90.0, "condition": "Nowy bez metki", "source": "Test", "url": "http://example.com/3"},
    {"title": "Produkt 4 - Bardzo dobry", "price": 80.0, "condition": "Bardzo dobry", "source": "Test", "url": "http://example.com/4"},
    {"title": "Produkt 5 - Dobry", "price": 70.0, "condition": "Dobry", "source": "Test", "url": "http://example.com/5"},
    {"title": "Produkt 6 - Używany", "price": 50.0, "condition": "Używany", "source": "Test", "url": "http://example.com/6"},
    {"title": "Produkt 7 - Zadowalający", "price": 40.0, "condition": "Zadowalający", "source": "Test", "url": "http://example.com/7"},
    {"title": "Produkt 8 - Uszkodzony", "price": 10.0, "condition": "Uszkodzony", "source": "Test", "url": "http://example.com/8"},
    {"title": "Produkt 9 - Inny/Nieznany", "price": 200.0, "condition": "Inny", "source": "Test", "url": "http://example.com/9"},
]

filename = "test_kolory_gradient.xlsx"

# Clean up previous test
if os.path.exists(filename):
    try:
        os.remove(filename)
    except:
        pass

print("Generowanie testowego pliku Excel z gradientem...")
zapisz_dane_do_excela(dane_testowe, filename)
print(f"Plik {filename} został wygenerowany. Proszę sprawdzić kolory w kolumnie 'Stan'.")
