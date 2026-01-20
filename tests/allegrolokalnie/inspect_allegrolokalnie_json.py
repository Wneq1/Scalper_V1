
import json
from bs4 import BeautifulSoup

def inspect_json():
    with open("allegrolokalnie.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    scripts = soup.find_all("script", type="application/ld+json")
    print(f"Found {len(scripts)} ld+json scripts.")
    
    found_items = False
    
    for script in scripts:
        try:
            data = json.loads(script.string)
            # Check if it's the ItemList we want
            if isinstance(data, dict) and data.get("@type") == "ItemList":
                print("Found ItemList!")
                items = data.get("itemListElement", [])
                print(f"Number of items: {len(items)}")
                
                for entry in items[:5]: # Show first 5
                    item = entry.get("item", {})
                    name = item.get("name")
                    url = item.get("url")
                    offers = item.get("offers", {})
                    price = offers.get("price")
                    condition = item.get("itemCondition")
                    
                    print(f"Title: {name}")
                    print(f"Price: {price}")
                    print(f"URL: {url}")
                    print(f"Condition: {condition}")
                    print("-" * 20)
                found_items = True
                break
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            continue
            
    if not found_items:
        print("Could not find relevant ItemList JSON.")

if __name__ == "__main__":
    inspect_json()
