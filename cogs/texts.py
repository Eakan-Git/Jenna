from discord.ext import commands
from .core.dank.unscramble import unscramble

import typing
import discord
import upsidedown
import colors
import googletrans

def LangCode(s):
    s = s.lower().replace('-', '')
    if s in googletrans.LANGUAGES or s in googletrans.LANGCODES:
        return s
    raise BadArgument(f'%s is not a language code')

class Texts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = googletrans.Translator()
    
    @commands.command(aliases=['usd'])
    async def upsidedown(self, context, *, text):
        text = text.replace('||', '')
        text = upsidedown.transform(text)
        await context.send(text)
    
    @commands.command(aliases=['usb'])
    async def unscramble(self, context, *, text):
        await context.trigger_typing()
        anagrams = await unscramble(text)
        response = f'{context.author.mention}\n**Anagrams**: '
        if anagrams:
            response += ' '.join([f'`{a}`' for a in anagrams])
        else:
            response += 'Not found!'
        await context.send(response)
    
    @commands.command(aliases=['tr', 'tl'])
    async def translate(self, context, dest:typing.Optional[LangCode]='en', *, text):
        await context.trigger_typing()
        translated = self.translator.translate(text, dest)
        embed = colors.embed()
        embed.description = f'{translated.text}'.replace('nhoan', 'cringy')
        embed.set_footer(text=f'{translated.src}: {text}')
        await context.send(embed=embed)
    
    @commands.command()
    async def listlang(self, context):
        output = 'Supported Languages:\n'
        output += ' '.join([f'`{code}` - {lang.title()}' for code, lang in googletrans.LANGUAGES.items()])
        await context.send(output)

def setup(bot):
    bot.add_cog(Texts(bot))