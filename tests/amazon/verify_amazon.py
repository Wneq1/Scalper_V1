from pobierz_z_amazona import uruchom_amazon

print("Testowanie modułu Amazon...")
oferty = uruchom_amazon(["lego"], max_ofert=5)

print(f"\nZnaleziono {len(oferty)} ofert:")
for o in oferty:
    print(f"- {o['title']} | {o['price']} | {o['url']}")
