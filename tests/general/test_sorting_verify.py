from obsluga_excela import zapisz_dane_do_excela
import os
import time

# Dummy data with unsorted prices and conditions
test_data = [
    {'title': 'Produkt Drogi', 'price': '1000 zł', 'condition': 'Nowe', 'source': 'Allegro', 'url': 'http://test.com/1'},
    {'title': 'Produkt Tani', 'price': '50,99 zł', 'condition': 'Używane', 'source': 'OLX', 'url': 'http://test.com/2'},
    {'title': 'Produkt Średni', 'price': '250.0', 'condition': 'Nowe', 'source': 'Allegro', 'url': 'http://test.com/3'},
    {'title': 'Produkt Bez Ceny', 'price': 'Do negocjacji', 'condition': 'Używane', 'source': 'OLX', 'url': 'http://test.com/4'},
]

print("Uruchamiam test zapisu z sortowaniem i kolumną Stan...")
filename = "test_sortowania_stan.xlsx"
zapisz_dane_do_excela(test_data, filename)

print(f"Plik {filename} został utworzony.")
print("Sprawdź ręcznie czy:")
print("1. Kolejność cen: Bez ceny (0), 50.99, 250.0, 1000.")
print("2. Kolumna C zawiera: Używane, Używane, Nowe, Nowe (odpowiednio dla ofert). (Pamiętaj o sortowaniu!)")
print("   - Produkt Bez Ceny (do negocjacji) -> Używane")
print("   - Produkt Tani (50.99) -> Używane")
print("   - Produkt Średni (250.0) -> Nowe")
print("   - Produkt Drogi (1000) -> Nowe")
