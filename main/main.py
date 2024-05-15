import requests
from bs4 import BeautifulSoup as bs
import time
import random
import csv

urls = []
visited_urls = []
products = []

query = "pralni stroj"

def sestavi_url(query: str):
    r_query = "+".join(query.split())
    return f"https://www.bigbang.si/izdelki/?search_q={r_query}"
    
urls.append(sestavi_url(query))

def get_html(url):
    try:
        return requests.get(url)
    except Exception as e:
        print(e)
        return ''
    
while len(urls) != 0 and len(visited_urls) < 15:
    curr_url = urls.pop()
    visited_urls.append(curr_url)

    response = get_html(curr_url)
    soup = bs(response.content, "html.parser")
    
    # Find all product links
    links = soup.find_all('a', href=True)
    for link in links:
        url = link['href']
        if url not in visited_urls and '-'.join(query.split()) in url:
            full_url = "https://www.bigbang.si" + url if not url.startswith("http") else url
            urls.append(full_url)
            print(full_url)
    
    # Scrape product details
    product = {}
    product["url"] = curr_url
    product_image = soup.select_one("#product-images img")
    product["slika"] = product_image["src"] if product_image else "N/A"
    product_name = soup.select_one(".cd-title")
    product["name"] = product_name.text.strip() if product_name else "N/A"
    product_price = soup.select_one(".cd-current-price")
    product["price"] = product_price.text.strip() if product_price else "N/A"
    
    products.append(product)
    
    time.sleep(random.uniform(1, 3))

with open('products.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["URL", "Image", "Name", "Price"])
    for product in products:
        writer.writerow(product.values())

print("Scraping completed. Products saved to products.csv.")
