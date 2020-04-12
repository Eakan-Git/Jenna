from discord.ext import commands
from ..utils import download
import re

async def to_partial_emoji(context, s):
    try:
        return await commands.PartialEmojiConverter().convert(context, s)
    except:
        print(s)

EMOJID_PATTERN = '<(a*):[^:\s]+:(\d+)>'
def shorten(emoji):
    id = re.findall(EMOJID_PATTERN, str(emoji))
    if id:
        id = ''.join(id[0])
    return id

def expand(name, id):
    if re.findall(EMOJID_PATTERN, id):
        return id
    a = ''
    if id.startswith('a'):
        a = 'a'
        id = id[1:]
    return f'<{a}:{name}:{id}>'