import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import sys
import random

class FlipkartScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.base_url = "https://www.flipkart.com/search"

    def search_products(self, query):
        try:
            params = {
                'q': query,
                'otracker': 'search',
                'marketplace': 'FLIPKART'
            }
            
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            product_cards = soup.find_all('div', {'class': ['_1AtVbE', '_2kHMtA', '_4ddWXP']})
            
            for card in product_cards:
                product = self._extract_product_info(card)
                if product:
                    products.append(product)
            
            return products
            
        except requests.RequestException as e:
            print(f"Error fetching products: {str(e)}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return []

    def _extract_product_info(self, card):
        try:
            name_elem = (
                card.find('div', {'class': '_4rR01T'}) or
                card.find('a', {'class': 's1Q9rs'}) or
                card.find('a', {'class': 'IRpwTa'})
            )
            
            price_elem = (
                card.find('div', {'class': '_30jeq3'}) or
                card.find('div', {'class': '_30jeq3 _1_WHN1'})
            )
            
            rating_elem = (
                card.find('div', {'class': '_3LWZlK'}) or
                card.find('div', {'class': '_3LWZlK _3uSWvT'})
            )
            
            link_elem = card.find('a', href=True)
            
            if name_elem and price_elem:
                product = {
                    'name': name_elem.get_text().strip(),
                    'price': price_elem.get_text().strip(),
                    'rating': rating_elem.get_text().strip() if rating_elem else 'No rating',
                    'link': f"https://www.flipkart.com{link_elem['href']}" if link_elem else None
                }
                return product
                
        except Exception as e:
            print(f"Error extracting product info: {str(e)}")
        
        return None

    def save_results(self, products, query):
        if not products:
            print("No products found to save.")
            return
        
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'flipkart_results_{timestamp}.json'
        
        data = {
            'metadata': {
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'total_products': len(products)
            },
            'products': products
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"\nResults saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {str(e)}")

def main():
    scraper = FlipkartScraper()
    
    while True:
        print("\nFlipkart Product Scraper")
        print("=" * 30)
        query = input("Enter product to search (or 'quit' to exit): ").strip()
        
        if query.lower() == 'quit':
            print("Thank you for using Flipkart Scraper!")
            break
        
        if not query:
            print("Please enter a valid product name.")
            continue
        
        print(f"\nSearching for '{query}' on Flipkart...")
        products = scraper.search_products(query)
        
        if products:
            print(f"\nFound {len(products)} products!")
            print("\nTop 3 Results:")
            for i, product in enumerate(products[:3], 1):
                print(f"\n{i}. {product['name']}")
                print(f"   Price: {product['price']}")
                print(f"   Rating: {product['rating']}")
                print(f"   Link: {product['link']}")
            
            scraper.save_results(products, query)
        else:
            print("No products found. Try a different search term.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScraper stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)