from ...core import utils
from discord.ext import commands
from urllib.parse import quote

import json
import colors
import textwrap
import const

API = 'https://api.dictionaryapi.dev/api/v2/entries/{}/{}'
GOOGLE_URL = 'https://www.google.com/search?q=define+'

WORD = 'word'
PHONETIC = 'phonetic'
MEANINGS = 'meanings'
PART_OF_SPEECH = 'partOfSpeech'
DEFINITIONS = 'definitions'
DEFINITION = 'definition'
EXAMPLE = 'example'
SYNONYMS = 'synonyms'
ORIGIN = 'origin'

NO_DEFS = 'No definitions found for this word.'
GOOGLE_DICTIONARY = 'Google Dictionary'

async def define(lang, word):
    url = API.format(lang, word)
    data = await utils.download(url)
    data = json.loads(data or '{}')

    embed = colors.embed(title=word, url=GOOGLE_URL + quote(word))
    embed.set_author(name=GOOGLE_DICTIONARY)
    if not isinstance(data, list):
        embed.description = NO_DEFS
        return embed

    for d in data:
        for meaning in d[MEANINGS]:
            lines = []
            phonetic = d.get(PHONETIC)
            part_of_speech = meaning.get(PART_OF_SPEECH)
            title = ' - '.join(filter(None, [phonetic, part_of_speech]))

            defs = meaning[DEFINITIONS]
            for i, de in enumerate(defs):
                if not de: continue
                numbering = f'{i+1}. ' if len(defs) > 1 else ''
                new_lines = []
                new_lines += [numbering + de.get(DEFINITION, '')]
                
                example = de.get(EXAMPLE)
                if example:
                    new_lines += [f'*"{example}"*']
                
                synonyms = de.get(SYNONYMS, [])
                if len(''.join(synonyms)):
                    new_lines += [f'**{SYNONYMS.title()}**: ' + ' • '.join(f'`{s}`' for s in synonyms)]
                new_lines += ['']
                
                value = '\n'.join(lines + new_lines)
                if len(value) > 1024:
                    add_lines_as_field(embed, title, lines)
                    phonetic = const.INVISIBLE
                    lines = []
                lines += new_lines
            
            origin = d.get(ORIGIN)
            if origin:
                lines += [f'**{ORIGIN.title()}**: {origin}\n']

            add_lines_as_field(embed, title, lines)
    
    return embed

def add_lines_as_field(embed, title, lines):
    value = '\n'.join(lines)
    embed.add_field(name=title, value=value, inline=False)

SUPPORTED_LANGS = {
    'en': 'English',
    'hi': 'Hindi',
    'es': 'Spanish',
    'fr': 'French',
    'ja': 'Japanese',
    'ru': 'Russian',
    'de': 'German',
    'it': 'Italian',
    'ko': 'Korean',
    'pt-BR': 'Brazilian Portuguese',
    'zh-CN': 'Chinese (Simplified)',
    'ar': 'Arabic',
    'tr': 'Turkish',
}

def DefinedLang(lang):
    if lang not in SUPPORTED_LANGS:
        raise commands.BadArgument('Language not supported')
    return lang