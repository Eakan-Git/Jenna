from bs4 import BeautifulSoup
from datetime import datetime
from .. import utils
import time
import pycountry
import colors

URL = 'https://www.worldometers.info/coronavirus/'
UPDATE_INTERVAL = 2 * 60

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

        web_content = await utils.download(URL)
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

COUNTRIES_OF_INTEREST = ['Vietnam', 'USA', 'Singapore', 'Germany', 'Canada', 'Australia', 'Malaysia', 'Netherlands']

FLAG_EMOTES_BY_COUNTRY = {}
for name in COUNTRIES_OF_INTEREST:
    alpha2 = pycountry.countries.search_fuzzy(name)[0].alpha_2
    FLAG_EMOTES_BY_COUNTRY[name] = ':flag_%s:' % alpha2.lower()

WORLD = 'World'
COUNTRIES_OF_INTEREST.insert(0, WORLD)
FLAG_EMOTES_BY_COUNTRY[WORLD] = ':earth_asia:'

TOTAL_CASES = 'Total Cases'
NEW_CASES = 'New Cases'
TOTAL_DEATHS = 'Total Deaths'
NEW_DEATHS = 'New Deaths'
RECOVERED_EMOTE = ':recovered:'
RECOVERED = 'Recovered'
STATS_TEMPLATE = f''':microbe: **{TOTAL_CASES}(+{NEW_CASES})**
:skull: **{TOTAL_DEATHS}(+{NEW_DEATHS})**
{RECOVERED_EMOTE} **{RECOVERED}**
__
'''
TITLE = 'Worldometer Coronavirus Update'
def embed_countries(data, recovered_emote):
    global STATS_TEMPLATE
    STATS_TEMPLATE = STATS_TEMPLATE.replace(RECOVERED_EMOTE, str(recovered_emote))
    embed = colors.embed(title=TITLE, url=URL, description=STATS_TEMPLATE)
    embed.timestamp = datetime.now().astimezone()

    for country in data:
        for i, value in enumerate(country):
            country[i] = str(value or 0).replace('+', '')
        name, total_cases, new_cases, total_deaths, new_deaths, recovered = country[:6]
        if name not in COUNTRIES_OF_INTEREST: continue

        flag_emote = FLAG_EMOTES_BY_COUNTRY[name]
        country_name = f'{flag_emote} {name}'

        content = STATS_TEMPLATE \
            .replace(TOTAL_CASES, total_cases) \
            .replace(NEW_CASES, new_cases) \
            .replace(TOTAL_DEATHS, total_deaths) \
            .replace(NEW_DEATHS, new_deaths) \
            .replace(RECOVERED, recovered)
        
        embed.add_field(name=country_name, value=content)
    
    return embed