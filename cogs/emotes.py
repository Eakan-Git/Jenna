import discord
import typing
import re
import aiohttp
import colors
import math
import random
import converter as conv
import cogs

from discord.ext import commands

PEEK = 'peek'
LUV = 'worryluv'
MAD = 'worryduoi'

LOVE_WORDS = ['luv', 'love', 'iu', 'thank', 'good']
HATE_WORDS = ['fuck', 'screw', 'hate', 'ngu']

EMOTES_PER_PAGE = 25
EMOJI_PATTERN = '(:[^:\s]+:)(?!\d)'
INTERROBANG = '⁉️'
HOME_GUILD = 596171359747440657

EMBED_BACKCOLOR = 0x2f3136

TWEMOJI_CDN = 'https://twemoji.maxcdn.com/v/latest/72x72/%x.png'

class Emotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['big'])
    async def enlarge(self, context, emoji:conv.NitroEmoji):
        embed = discord.Embed(color=EMBED_BACKCOLOR)
        url = None
        if type(emoji) in [discord.Emoji, discord.PartialEmoji]:
            url = emoji.url
        elif len(emoji) == 1:
            url = TWEMOJI_CDN % ord(emoji)
        
        if url:
            embed.set_image(url=url)
            await context.send(embed=embed)
        else:
            React = self.bot.get_cog(cogs.REACT)
            await React.add_reaction(context.message, ':interrobang:')

    @commands.command(aliases=['emojis'])
    async def emotes(self, context, page:int=1):
        home_guild = self.bot.get_guild(HOME_GUILD)
        embed = colors.embed()
        embed.set_author(name='Available Emotes')
        total_page = math.ceil(len(home_guild.emojis) / EMOTES_PER_PAGE)
        embed.set_footer(text=f'Page {page}/{total_page}')
        
        all_emojis = sorted(home_guild.emojis, key=lambda e: e.name)
        emojis = []
        start = EMOTES_PER_PAGE * (page - 1)
        end = EMOTES_PER_PAGE * page
        page_emojis = all_emojis[start:end]
        for e in page_emojis:
            emojis += [f'{e} `:{e.name}:`']
        embed.description = '\n'.join(emojis)
        await context.send(embed=embed)
    
    @commands.command()
    @commands.guild_only()
    async def drop(self, context, emoji:conv.NitroEmoji, author:typing.Optional[conv.Member], i:int=1):
        counter = 1
        async for message in context.history(limit=None, before=context.message):
            if author and message.author != author:
                continue
                
            if counter < i:
                counter += 1
                continue
            break
        
        await message.add_reaction(emoji)
        
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user: return
        context = await self.bot.get_context(msg)
        if context.command:
            return
        await self.reply_emotes(msg)
        await self.drop_emotes_on_mention(msg)
    
    def get_emoji(self, name):
        return discord.utils.get(self.bot.emojis, name=name)
    
    async def drop_emotes_on_mention(self, msg):
        direct_mention = str(self.bot.user.id) in msg.content
        indirect_mention = self.bot.user.name.lower() in msg.content.lower()
        if direct_mention or indirect_mention:
            emoji = PEEK
            if any(word in msg.content.lower() for word in LOVE_WORDS):
                emoji = LUV
            elif any(word in msg.content.lower() for word in HATE_WORDS):
                emoji = MAD
            
            emoji = self.get_emoji(emoji)
            await msg.add_reaction(emoji)

    async def reply_emotes(self, msg):
        match = re.findall(EMOJI_PATTERN, msg.content)
        emojis = []

        for emoji in match:
            emoji = self.get_emoji(emoji.replace(':', ''))
            if emoji:
                emojis += [str(emoji)]
        
        if emojis:
            emojis = ' '.join(emojis)
            await msg.channel.send(emojis)
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def addemote(self, context, url, name=None):
        image = None
        response = INTERROBANG
        
        async with context.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    if r.status == 200:
                        image = await r.read()
            
            if image:
                if not name:
                    name = 'emote%04d' % random.randint(0, 9999)
                await context.guild.create_custom_emoji(name=name, image=image)
                response = self.get_emoji(name)
            await context.message.add_reaction(response)

def setup(bot):
    bot.add_cog(Emotes(bot))