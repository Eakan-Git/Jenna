from bs4 import BeautifulSoup
from discord.ext import commands
from urllib.parse import urlparse
from .. import utils

import discord
import textwrap
import re

ICON_URL = 'https://www.redditstatic.com/icon.png'
SUB_TOP_URL = 'https://www.reddit.com/r/{}/top/'
RSS = '.rss'
TOP_RSS = SUB_TOP_URL + RSS
MIN_SUB_NAME = 3
MAX_TEXT = 2000
MAX_TITLE = 250

VREDDIT = 'v.redd.it'
GFYCAT = 'gfycat'
SPECIAL_WEBSITES = [VREDDIT, GFYCAT, 'twitter', 'imgur', 'youtu']
def is_special_website(url):
    return any(site in url for site in SPECIAL_WEBSITES)

def get_sub_url(sub):
    return SUB_TOP_URL.format(sub)

def subname(sub):
    sub = sub.replace('r/', '').replace('/r/', '')
    if len(sub) < 3:
        raise commands.BadArgument(f'`r/{sub}` is not a subreddit')
    return sub

def posts(s):
    start = 0
    if any(s.endswith(word) for word in ['st', 'nd', 'rd', 'th']):
        posts = int(s[:-2])
        start = posts - 1
    else:
        try: posts = int(s)
        except: raise BadArgument(f'`{s}`? >.< I dun understand!')
    return range(start, posts)

class RedditEntry:
    def __init__(self, sub, title, url, author, thumbnail, content_url, text):
        self.sub = sub
        self.title = title
        self.url = url

        self.titles = textwrap.wrap(title, MAX_TITLE)
        if len(self.titles) > 1:
            self.titles[0] += '...'
            self.titles[1] = '...' + self.titles[1]

        self.author_name = author['name']
        self.author_uri = author['uri']
        self.author = f'[{self.author_name}]({self.author_uri})'

        self.image = content_url if utils.url_is_image(content_url) else ''
        self.thumbnail = thumbnail if not self.image else ''

        self.content_url = ''
        if content_url not in [self.url, self.image]:
            if GFYCAT in content_url:
                content_url = re.sub('\/\w+\/', '/', content_url)
            self.content_url = content_url
            self.content_url_hostname = urlparse(content_url).hostname
            self.content_url_field = f'[{self.content_url_hostname}]({self.content_url})'

        self.text = text
        if len(text) > MAX_TEXT:
            self.text = text[:MAX_TEXT] + '...'
        self.sub_logo = ''
    
    def __str__(self):
        return '\n'.join([self.sub,
        self.title,
        self.url,
        self.thumbnail,
        self.content_url]).replace('\n\n', '\n')
            
def parse_entry(entry):
    content = BeautifulSoup(entry.content.text, 'html.parser')
    sub = entry.category['label']
    title = entry.title.text
    url = entry.link['href']
    thumbnail = content.img['src'] if content.img else ''

    content_url = content.span.a['href'] or ''
    text = content.div
    text = text.text if text else ''

    author = entry.author
    author = {
        'name': author.find('name').text,
        'uri': author.uri.text
    }

    return RedditEntry(sub, title, url, author, thumbnail, content_url, text)

async def top(subreddit, index=0):
    sub = subreddit.lower()
    url = TOP_RSS.format(sub)
    rss = await utils.download(url)
    if not rss:
        raise commands.UserInputError(f'`r\{subreddit}` does not exist')

    soup = BeautifulSoup(rss, 'html.parser')
    entries = soup('entry')
    sub_name = soup.feed.category['label']
    if not entries:
        raise commands.UserInputError(f'`r\{subreddit}` has no new posts today or does not exist')
    
    try:
        entry = entries[index]
    except:
        raise commands.BadArgument(f'`r\{subreddit}` only has {len(entries)} top posts')
    entry = parse_entry(entry)
    sub_logo = soup.feed.logo
    if sub_logo:
        entry.sub_logo = sub_logo.text
    return entry