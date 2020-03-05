import discord
import re
import const
import aiohttp
import colors
import math

from discord.ext import commands

PEEK = 'peek'
LUV = 'worryluv'
MAD = 'worryduoi'

LOVE_WORDS = ['luv', 'love', 'iu', 'you', 'yeu', 'yêu']
HATE_WORDS = ['fuck', 'screw', 'hate', 'ghet', 'ghét']

EMOTES_PER_PAGE = 25

class Emotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['emojis'])
    async def emotes(self, context, page:int=1):
        home_guild = self.bot.get_guild(const.HOME_GUILD)
        embed = colors.random_color_embed()
        embed.set_author(name='Available Emotes')
        total_page = math.ceil(len(home_guild.emojis) / EMOTES_PER_PAGE)
        embed.set_footer(text=f'Page {page}/{total_page}')

        emojis = []
        start = EMOTES_PER_PAGE * (page - 1)
        end = EMOTES_PER_PAGE * page
        for e in home_guild.emojis[start:end]:
            emojis += [f'{e} `:{e.name}:`']
        embed.description = '\n'.join(emojis)
        await context.send(embed=embed)
    
    @commands.command()
    @commands.guild_only()
    async def react(self, context, author:discord.Member, emoji, i:int=1):
        if type(emoji) is str:
            emoji = emoji.replace(':', '')
            emoji = self.get_emoji(emoji)
            if not emoji:
                await context.message.add_reaction(const.INTERROBANG)
                return
        
        skip = 1
        async for message in context.history(limit=None):
            if message.author == author:
                if skip < i:
                    skip += 1
                    continue
                await message.add_reaction(emoji)
                return
        
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user: return
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
        match = re.findall(const.EMOJI_PATTERN, msg.content)
        msg_content = msg.content
        emojis = msg.content

        for emoji in match:
            emoji = self.get_emoji(emoji)
            if emoji:
                plain_emoji = f':{emoji.name}:'
                msg_content = msg_content.replace(plain_emoji, '')
                emojis = emojis.replace(plain_emoji, str(emoji))
        
        if emojis and not msg_content.strip():
            await msg.channel.send(emojis)
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def addemoji(self, context, name, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    image = await r.read()
                    await context.guild.create_custom_emoji(name=name, image=image)
                    emoji = self.get_emoji(name)
                    await context.message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(Emotes(bot))