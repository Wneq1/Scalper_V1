import requests
from bs4 import BeautifulSoup

def fetch_amazon(query):
    url = f"https://www.amazon.pl/s?k={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    print(f"Pobieranie: {url}")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Sukces! Zapisuję amazon.html")
            with open("amazon.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            return True
        else:
            print(f"Błąd HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"Błąd: {e}")
        return False

if __name__ == "__main__":
    fetch_amazon("iphone 13")
