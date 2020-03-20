import discord
import upsidedown

from discord.ext import commands
from trivia.unscramble import unscramble

MOCK_REPLACES = {
    'c': 'k',
    'n': 'm',
}

def spongebob_mock(s):
    s = s.lower()
    for char, sub in MOCK_REPLACES.items():
        s = s.lower().replace(char, sub)
    return ''.join(c.upper() if i % 2 else c for i, c in enumerate(s))

class Texts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['usd'])
    async def upsidedown(self, context, *, text):
        text = text.replace('||', '')
        text = upsidedown.transform(text)
        await context.send(text)
    
    @commands.command()
    async def mock(self, context, *, text):
        mock = discord.utils.get(self.bot.emojis, name='mock')
        mock2 = discord.utils.get(self.bot.emojis, name='mock2')
        text = spongebob_mock(text)
        text = f'{mock2} {text} {mock}'
        await context.send(text)
    
    @commands.command(aliases=['usb'])
    async def unscramble(self, context, *, text):
        anagrams = unscramble(text)
        response = f'**Anagrams**: '
        if anagrams:
            response += ' '.join([f'`{a}`' for a in anagrams])
        else:
            response += 'Not found!'
        await context.send(response)

def setup(bot):
    bot.add_cog(Texts(bot))