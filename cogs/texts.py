from discord.ext import commands
from .core.dank.unscramble import unscramble
from .core.texts import randomword, palabrasaleatorias as pa

import typing
import discord
import upsidedown
import colors
import googletrans
import const

SUPPORTED_LANGS = { 'auto': 'Automatic', **googletrans.LANGUAGES, **googletrans.LANGCODES}

def Src2Dest(s):
    src2dest = s.split('>')
    if len(src2dest) != 2:
        raise commands.BadArgument('Not in lang>lang format!')
    
    src, dest = src2dest
    src = src or 'auto'
    dest = dest or 'en'
    return '>'.join([src, dest])

class Texts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = googletrans.Translator()
    
    @commands.command(aliases=['usd'])
    async def upsidedown(self, context, *, text):
        text = text.replace('||', '')
        text = upsidedown.transform(text)
        await context.send(text)
    
    @commands.command(aliases=['usb'], hidden=True)
    async def unscramble(self, context, *, text):
        await context.trigger_typing()
        anagrams = await unscramble(text)
        response = f'`{text}` → '
        if anagrams:
            response += ' '.join([f'`{a}`' for a in anagrams])
        else:
            response += 'Not found!'
        await context.send(response)
    
    @commands.group(aliases=['tr', 'tl'], invoke_without_command=True)
    async def translate(self, context, src2dest:typing.Optional[Src2Dest]='auto>en', *, text=None):
        await context.trigger_typing()
        
        src2dest = src2dest.split('>')
        for lang in src2dest:
            if lang and lang not in SUPPORTED_LANGS:
                raise commands.BadArgument(f'`{lang}` is not a language code')
        src, dest = src2dest
        
        if not text:
            last_message = await context.history(limit=1, before=context.message).flatten()
            text = last_message[0].content

        translated = self.translator.translate(text, dest=dest, src=src)
        embed = colors.embed()
        embed.description = f'{translated.text}'.replace('nhoan', 'cringy')
        embed.set_footer(text=f'{translated.src}>{translated.dest}: {text}')
        await context.send(embed=embed)
    
    @translate.command()
    async def lang(self, context):
        output = '**Supported Languages**:\n'
        output += const.BULLET.join([f'`{code}`-{lang.title()}' for code, lang in googletrans.LANGUAGES.items()])
        await context.send(output)

    @commands.command(aliases=['rdw'])
    async def randomword(self, context, lang='en'):
        await context.trigger_typing()
        if lang == 'en':
            await self.send_random(context)
        else:
            word, definitions = await pa.get_random(lang)
            embed = colors.embed(title=word)
            embed.set_author(name=pa.get_title(lang), url=pa.get_url(lang))
            embed.description = const.BULLET.join([f'[[{site}]]({url})' for site, url in definitions.items()])
            await context.send(embed=embed)

    async def send_random(self, context, what='Word'):
        word, definition = await randomword.get_random(what)
        url = randomword.get_google_url(word)
        embed = colors.embed(title=word, url=url, description=definition)
        embed.set_author(name=f'Random {what}', url=randomword.URL)
        await context.send(embed=embed)
    
    @commands.command(aliases=['rdi'])
    async def randomidiom(self, context):
        await self.send_random(context, randomword.IDIOM)

def setup(bot):
    bot.add_cog(Texts(bot))