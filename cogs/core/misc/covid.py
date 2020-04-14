import time
import pycountry
from bs4 import BeautifulSoup
from .. import utils

URL = 'https://www.worldometers.info/coronavirus/'
UPDATE_INTERVAL = 2 * 60
COUNTRIES = ['Vietnam', 'USA', 'Singapore', 'Germany', 'Canada', 'Australia', 'Malaysia', 'Netherlands']

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
    
    async def update(self):
        if self.should_update():
            self.last_update = time.time()
            await self.download_data()
    
    def should_update(self):
        now = time.time()
        data_age = now - self.last_update
        return data_age > UPDATE_INTERVAL

    async def download_data(self):
        data = []

        web_content = await utils.download(URL, as_str=True)
        soup = BeautifulSoup(web_content, 'html.parser')
        table = soup.table

        for tbody in table('tbody')[::-1]:
            rows = tbody('tr')
            for row in rows:
                cols = row('td')
                cols = [c.text.strip() for c in cols]
                country = [c for c in cols]
                data += [country]
        
        data = data[1:]
        self.data = data