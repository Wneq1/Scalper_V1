
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
import os

def fetch_allegro_lokalnie():
    url = "https://allegrolokalnie.pl/oferty/q/RTX"
    print(f"Fetching {url}...")
    
    options = Options()
    # options.add_argument("--headless=new") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Edge(options=options)
    try:
        driver.get(url)
        time.sleep(5) # Wait for load
        
        # Scroll down to trigger lazy load if any
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        
        html = driver.page_source
        with open("allegrolokalnie.html", "w", encoding="utf-8") as f:
            f.write(html)
            
        print("Saved to allegrolokalnie.html")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_allegro_lokalnie()
