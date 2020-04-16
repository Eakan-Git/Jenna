import discord
import typing
import colors
import const
import timedisplay
import time

from discord.ext import commands, tasks
from datetime import datetime
from .core import converter
from .core.misc import covid, math, reddit

MATH_BRIEF = 'Compute big numbers for you'
INVITE_LINK = 'https://discordapp.com/api/oauth2/authorize?client_id=664109951781830666&permissions=1342565440&scope=bot'

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.corona_status = covid.CoronaStatus()
    
    @commands.group(hidden=True)
    async def do(self, context, subcommand, *, expr):
        if subcommand in ['math', 'meth']:
            await math.compute(context, expr)

    @commands.command(aliases=['meth'])
    async def math(self, context, *, expr):
        await math.compute(context, expr)

    @commands.command()
    @commands.guild_only()
    async def whos(self, context, *, member:typing.Optional[converter.Member]=None):
        member = member or context.author
        
        response = f'It\'s **{member}**'
        embed = colors.embed()
        embed.description = member.mention
        created_at = timedisplay.to_ict(member.created_at, timedisplay.DAYWEEK_DAY_IN_YEAR)
        joined_at = timedisplay.to_ict(member.joined_at, timedisplay.DAYWEEK_DAY_IN_YEAR)
        embed \
            .set_thumbnail(url=member.avatar_url) \
            .add_field(name='On Discord since', value=created_at, inline=False) \
            .add_field(name='Joined on', value=joined_at)

        await context.send(response, embed=embed)
    
    @commands.command()
    async def invite(self, context):
        worryluv = discord.utils.get(self.bot.emojis, name='worryluv')
        embed = colors.embed()
        embed.description = f'{worryluv} [Click here]({INVITE_LINK}) to invite {self.bot.user.name}!'
        await context.send(embed=embed)
    
    @commands.command(aliases=['cv', 'ncov', 'corona', 'morning'])
    async def covid(self, context, region='server'):
        await context.trigger_typing()
        await self.corona_status.update()
        data = self.corona_status.data

        emotes = ['khabanhquay']
        emotes = [str(discord.utils.get(self.bot.emojis, name=e)) for e in emotes]
        covid.set_emotes(*emotes)

        embed = covid.embed_countries(data) if region == 'server' \
            else covid.embed_region(data, region)
        await context.send(embed=embed)
    
    @commands.group(name='reddit', aliases=['rd'], hidden=True)
    async def _reddit(self, context): pass

    @_reddit.command(aliases=['t'])
    async def top(self, context, sub:typing.Optional[reddit.subname]='popular', posts:int=1):
        await context.trigger_typing()

        for i in range(posts):
            post = await reddit.top(sub, i)
            embed = colors.embed(title=post.titles[0], url=post.url, description=post.text) \
                .set_author(name=post.sub, url=reddit.get_sub_url(sub), icon_url=post.sub_logo) \
                .set_thumbnail(url=post.thumbnail or '') \
                .set_image(url=post.image) \
                .set_footer(text='Reddit', icon_url=reddit.ICON_URL)
            if len(post.titles) == 2:
                embed.add_field(name='More Title', value=post.titles[1])
            if post.content_url:
                embed.add_field(name='Link', value=post.content_url_field)
            await context.send(embed=embed)

            if reddit.is_special_website(post.content_url):
                await context.send(post.content_url)

def setup(bot):
    bot.add_cog(Misc(bot))
