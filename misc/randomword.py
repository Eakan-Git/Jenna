import requests
from bs4 import BeautifulSoup

GOOGLE_URL = 'https://www.google.com/search?q='
URL = 'https://randomword.com/'
IDIOM = 'Idiom'
WORD = 'word'

def get_random_word():
    return get_random()

def get_random_idiom():
    return get_random(IDIOM)

def get_random(what=''):
    what = what.lower()
    if what == WORD:
        what = ''
    url = URL + what
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    word = soup.find(id='random_word').text
    definition = soup.find(id='random_word_definition').text

    return word, definition