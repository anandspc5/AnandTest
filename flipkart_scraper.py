import requests
from bs4 import BeautifulSoup
import json

def flipkart_scraper(product_name):
    # Construct the search URL
    search_url = f"https://www.flipkart.com/search?q={product_name}"
    
    # Send a GET request to the search URL
    response = requests.get(search_url)
    
    # Parse the response content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find product details
    products = []
    for item in soup.find_all('div', class_='_1AtVbE'):
        name = item.find('a', class_='IRpwTa')
        price = item.find('div', class_='_30jeq3')
        rating = item.find('div', class_='_3LWZlK')

        if name and price and rating:
            product = {
                'name': name.get_text(),
                'price': price.get_text(),
                'rating': rating.get_text()
            }
            products.append(product)
    
    # Save results to a JSON file
    with open('flipkart_results.json', 'w') as json_file:
        json.dump(products, json_file, indent=4)

if __name__ == "__main__":
    product_name = input("Enter the product name to search on Flipkart: ")
    flipkart_scraper(product_name)