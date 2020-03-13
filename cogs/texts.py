import discord
import upsidedown

from discord.ext import commands

DEFAULT_TEXT = 'Enter something will you'

def spongebob_mock(s):
    return ''.join(c.upper() if i % 2 else c for i, c in enumerate(s.lower().replace('c', 'k')))

class Texts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['usd'])
    async def upsidedown(self, context, *, text=DEFAULT_TEXT):
        text = text.replace('||', '')
        text = upsidedown.transform(text)
        await context.send(text)
    
    @commands.command()
    async def mock(self, context, *, text=DEFAULT_TEXT):
        mock = discord.utils.get(self.bot.emojis, name='mock')
        mock2 = discord.utils.get(self.bot.emojis, name='mock2')
        text = spongebob_mock(text)
        text = f'{mock2} {text} {mock}'
        await context.send(text)

def setup(bot):
    bot.add_cog(Texts(bot))