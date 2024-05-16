from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from queue import PriorityQueue as pq
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

class Trip():
    def __init__(self, location:str, num_adults:int, num_children:int, num_rooms:int, checkin:str, checkout:str, currency:str):
        self.location = location
        self.num_adults = num_adults
        self.num_children = num_children
        self.num_rooms = num_rooms
        self.checkin = checkin
        self.checkout = checkout
        self.currency = currency
    
    def __str__(self):
        return "https://www.booking.com/searchresults.sl.html?ss={location}&ssne={location}&ssne_untouched={location}&efdco=1&label=gog235jc-1FCA"\
                "EoggI46AdII1gDaMsBiAEBmAEjuAEXyAEM2AEB6AEB-AECiAIBqAIDuAKQ9piyBsACAdICJDQwMWFlMGI0LTB"\
                "lNWUtNDRjNS1hNDkyLTY5YmEwNzM0NTIxONgCBeACAQ&aid=397594&lang=sl&sb=1&src_elem=sb&src=searchresults&&checkin={checkin}&checkout={checkout}&"\
                "group_adults={num_adults}&no_rooms={num_rooms}&group_children={num_children}"\
                .format(location=self.location, checkin=self.checkin, checkout=self.checkout, num_adults=self.num_adults, \
                        num_rooms=self.num_rooms, num_children=self.num_children)
    
location = input("Lokacija: ")
num_adults = input("St. odraslih: ")
num_children = input("St. otrok: ")
num_rooms = input("St. sob: ")
checkin = input("Datum prihoda (LLLL-MM-DD): ")
checkout = input("Datum odhoda (LLLL-MM-DD): ")

tr = Trip(location, num_adults, num_children, num_rooms, checkin, checkout, "EUR")
response = requests.get(tr.__str__(), headers=headers)
soup = bs(response.text, 'html.parser')
hotels = soup.find_all('div', {'data-testid' : 'property-card'})
hotels_data = []


for h in hotels:
    try:
        name = h.find('div', {'data-testid': 'title'})
        name = name.text.strip()

        location = h.find('span', {'data-testid': 'address'})
        location = location.text.strip()

        price = h.find('span', {'data-testid': 'price-and-discounted-price'})
        price = price.text.strip()
        price = price[2:]

        rating = h.find('div', {'data-testid': 'review-score'})
        rating = rating.text.strip()
        rating = rating[:4]
        rating = rating[:-1]
        rating = rating.replace(",", ".")
        rat = re.findall(r'\d+\.\d+', rating)
        rating = float(rat[0])

        print(name, location, price, rating)
        hotels_data.append({'name':name, 'location':location, 'price':price, 'rating':rating})
    except Exception as e:
        print(e)

hotel = pd.DataFrame(hotels_data)
hotel.head()

hotel.to_csv('hotels.csv', header=True, index=False)