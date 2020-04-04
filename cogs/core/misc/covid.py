import requests
import time
import pycountry
from bs4 import BeautifulSoup

URL = 'https://www.worldometers.info/coronavirus/'
UPDATE_INTERVAL = 2 * 60
COUNTRIES = ['Vietnam', 'USA', 'Singapore', 'Germany', 'Canada', 'Australia', 'Malaysia', 'Japan']

FLAG_EMOTES_BY_COUNTRY = {}
for name in COUNTRIES:
    alpha2 = pycountry.countries.search_fuzzy(name)[0].alpha_2
    FLAG_EMOTES_BY_COUNTRY[name] = ':flag_%s:' % alpha2.lower()

WORLD = 'World'
COUNTRIES.insert(0, WORLD)
FLAG_EMOTES_BY_COUNTRY[WORLD] = ':earth_asia:'

class CoronaStatus:
    def __init__(self):
        self.data = []
        self.last_update = 0
    
    def update(self):
        if self.should_update():
            self.last_update = time.time()
            self.download_data()
    
    def should_update(self):
        now = time.time()
        data_age = now - self.last_update
        return data_age > UPDATE_INTERVAL

    def download_data(self):
        data = []

        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        for tbody in table.find_all('tbody')[::-1]:
            rows = tbody.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [c.text.strip() for c in cols]
                country = [c for c in cols]
                data += [country]
        
        data = data[1:]
        self.data = data