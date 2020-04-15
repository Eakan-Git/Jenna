from bs4 import BeautifulSoup
from datetime import datetime
from .. import utils
from ..emotes import utils as emutils 
from discord.ext import commands
from dataclasses import dataclass

import discord
import time
import pycountry
import colors

URL = 'https://www.worldometers.info/coronavirus/'
UPDATE_INTERVAL = 5 * 60

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
                
                if country[0] == 'Total:':
                    country[0] = country[-1]
                for i, value in enumerate(country):
                    value = str(value or 0).replace('+', '').replace(',', '')
                    try: country[i] = int(value)
                    except: pass

                data += [country]
        
        self.data = data

COUNTRIES_OF_INTEREST = ['Vietnam', 'USA', 'Singapore', 'Germany', 'Canada', 'Australia', 'Malaysia', 'Netherlands']

FLAG_EMOTES_BY_COUNTRY = {}
for name in COUNTRIES_OF_INTEREST:
    alpha2 = pycountry.countries.search_fuzzy(name)[0].alpha_2
    FLAG_EMOTES_BY_COUNTRY[name] = ':flag_%s:' % alpha2.lower()

WORLD = 'World'
GLOBE = ':earth_asia:'
COUNTRIES_OF_INTEREST.insert(0, WORLD)
FLAG_EMOTES_BY_COUNTRY[WORLD] = GLOBE

TOTAL_CASES = 'Total Cases'
NEW_CASES = 'New Cases'
TOTAL_DEATHS = 'Total Deaths'
NEW_DEATHS = 'New Deaths'
RECOVERED_EMOTE = ':recovered:'
RECOVERED = 'Recovered'
EXPLANATION = f''':microbe: **{TOTAL_CASES}** (+{NEW_CASES})
:skull: **{TOTAL_DEATHS}** (+{NEW_DEATHS})
{RECOVERED_EMOTE} **{RECOVERED}**
__
'''
STATS = ''':microbe: **{:,}** {}
:skull: **{:,}** {}
{} **{:,}**
__
'''

@dataclass
class CustomEmotes:
    recovered: str
    active: str
    critical: str

def set_emotes(recovered, active, critical):
    global emotes
    emotes = CustomEmotes(recovered, active, critical)

def compile_stats(country_data):
    total_cases, new_cases, total_deaths, new_deaths, recovered = country_data[1:6]
    new_cases = plus(new_cases)
    new_deaths = plus(new_deaths)
    return STATS.format(total_cases, new_cases, total_deaths, new_deaths, emotes.recovered, recovered)

def comma(number):
    return f'{number:,}' if type(number) is int else number

def plus(number):
    return f'(+{number:,})' if number else ''

TITLE = 'Worldometer Coronavirus Update'
def embed_countries(data):
    embed = colors.embed(title=TITLE, url=URL, description=EXPLANATION.replace(RECOVERED_EMOTE, emotes.recovered))
    embed.timestamp = datetime.now().astimezone()

    for country_data in data:
        name = country_data[0]
        if name not in COUNTRIES_OF_INTEREST: continue

        flag_emote = FLAG_EMOTES_BY_COUNTRY[name]
        country_name = f'{flag_emote} {name}'
        content = compile_stats(country_data)

        embed.add_field(name=country_name, value=content)
    
    return embed

def percent(num, denom):
    if type(num) == str or num == 0 or denom == 0: return ''
    number = num / denom * 100
    num_str = f'{number:.1g}' if number < 1 else f'{number:.1f}'
    return f'[{num_str}%]' if number else ''

def embed_region(data, region):
    country_data, flag = get_country_data_fuzzy(data, region)
    if not country_data:
        raise commands.UserInputError('Country not found!')

    wtotal_cases, _, wtotal_deaths = data[0][1:4]
    name, total_cases, new_cases, total_deaths, new_deaths, recovered, active_cases, critical = country_data[:8]

    wcases_percent = percent(total_cases, wtotal_cases)
    wdeaths_percent = percent(total_deaths, wtotal_deaths)
    deaths_percent = percent(total_deaths, total_cases)
    recovered_percent = percent(recovered, total_cases)
    active_percent = percent(active_cases, total_cases)
    critical_percent = percent(critical, total_cases)

    is_world = country_data[-1] == 'All'
    wcases_percent = f'{GLOBE} {wcases_percent}' if wcases_percent and not is_world else ''
    wdeaths_percent = f'{GLOBE} {wdeaths_percent}' if wdeaths_percent and not is_world else ''
    deaths_percent = f'{flag} {deaths_percent}' if deaths_percent else ''

    new_cases = plus(new_cases)
    new_deaths = plus(new_deaths)

    total_cases, _, total_deaths, _, recovered, active_cases, critical = map(comma, country_data[1:8])

    embed = colors.embed()
    embed.title = f'Coronavirus cases for {name} {flag}'
    embed \
        .add_field(name=f':microbe: {TOTAL_CASES}', value=f'**{total_cases}** {new_cases} {wcases_percent}') \
        .add_field(name=f':skull: {TOTAL_DEATHS}', value=f'**{total_deaths}** {new_deaths} {wdeaths_percent} {deaths_percent}', inline=False) \
        .add_field(name=f'{emotes.recovered} {RECOVERED}', value=f'**{recovered}** {recovered_percent}') \
        .add_field(name=f'{emotes.active} Active Cases', value=f'**{active_cases}** {active_percent}') \
        .add_field(name=f'{emotes.critical} Critical', value=f'**{critical}** {critical_percent}')
    embed.timestamp = datetime.now().astimezone()
    return embed

CONTINENTS = ['World', 'All', 'Europe', 'North America', 'South America', 'Asia', 'Africa', 'Oceania']

def get_country_data_fuzzy(data, region):
    country = None
    if region.title() not in CONTINENTS:
        if region.upper() == 'UK':
            country = pycountry.countries.get(alpha_2='GB')
        else:
            try:
                countries = pycountry.countries.search_fuzzy(region)
                country = countries[0]
            except:
                pass
    
    possible_names = [region]
    if country:
        acronym = ''.join(word[0] for word in country.name.split())
        official_name = getattr(country, 'official_name', '')
        common_name = getattr(country, 'common_name', '')
        possible_names += [country.alpha_2, country.alpha_3, country.name, official_name, common_name, acronym]
    possible_names = [n.lower() for n in possible_names]

    def match_name(c):
        name = c[0]
        return str(name).lower() in possible_names
    country_data = discord.utils.find(match_name, data)
    
    flag = ':flag_{}:'.format(country.alpha_2.lower()) if country else ':flags:'
    if country_data and country_data[-1] == 'All':
        flag = GLOBE
    return country_data, flag