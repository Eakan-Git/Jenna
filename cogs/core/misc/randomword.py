from bs4 import BeautifulSoup
from .. import utils

GOOGLE_URL = 'https://www.google.com/search?q='
URL = 'https://randomword.com/'
IDIOM = 'Idiom'
WORD = 'word'

async def get_random_word():
    return get_random()

async def get_random_idiom():
    return get_random(IDIOM)

async def get_random(what=''):
    what = what.lower()
    if what == WORD:
        what = ''
    url = URL + what
    web_content = await utils.download(url, as_str=True)
    soup = BeautifulSoup(web_content, 'html.parser')
    word = soup.find(id='random_word').text
    definition = soup.find(id='random_word_definition').text

    return word, definition