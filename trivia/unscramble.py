import requests
from bs4 import BeautifulSoup

URLS = [
    'https://www.allscrabblewords.com/unscramble/',
    'https://wordfinder.yourdictionary.com/unscramble/',
]

SPECIAL_CASES = {
    'calypso': ['cosplay']
}

def unscramble(word):
    for url in URLS:
        anagrams = get_anagrams(word, url)
        if anagrams:
            break
    for word, missing_words in SPECIAL_CASES.items():
        if word in anagrams:
            anagrams += missing_words
    return anagrams

PARSER = 'html.parser'
 
def get_anagrams(word, url):
    soup = request_site(word, url)
    anagrams = [a.text.strip() for a in soup.find_all('a') if valid_anagram(word, a.text)]
    return anagrams

def valid_anagram(original, anagram, same_length=True):
    anagram = anagram.strip()
    one_word = ' ' not in anagram
    same_length = len(anagram) == len(original) or not same_length
    return one_word and same_length and anagram.islower()

def request_site(word, url):
    url = url + word
    response = requests.get(url)
    soup = BeautifulSoup(response.text, PARSER)
    return soup