import requests
from bs4 import BeautifulSoup
import time

def track_price(url, target_price):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # This selector varies by website (Example for a generic store)
    price_text = soup.find(id="priceblock_ourprice").get_text()
    price = float(price_text.replace('€', '').replace(',', '.').strip())
    
    if price <= target_price:
        print("ALERT: Price dropped! Buy now!")
    else:
        print(f"Current price: {price}€. Still too high.")

if __name__ == "__main__":
    track_price("https://amazon.es/dp/example", 500.00)
