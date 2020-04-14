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
        self.reddit_rss = reddit.RedditRSS()
    
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
    
    @commands.command(aliases=['ncov', 'corona'])
    async def covid(self, context):
        msg = await context.send('`Downloading data...`')
        await self.corona_status.update()
        
        RECOVERED_EMOTE = discord.utils.get(self.bot.emojis, name='khabanhquay')
        embed = colors.embed()
        embed.description = ':microbe: **Total(+New Cases)**\n:skull: **Deaths(+New Deaths)**'
        embed.description += f'\n{RECOVERED_EMOTE} **Recovered**'
        embed.title = 'Worldometer Coronavirus Update'
        embed.url = covid.URL
        embed.timestamp = datetime.now().astimezone()

        for country in self.corona_status.data:
            name, total, new_cases, deaths, new_deaths, recovered = country[:6]
            if name not in covid.COUNTRIES: continue

            flag_emote = covid.FLAG_EMOTES_BY_COUNTRY[name]
            name = f'{flag_emote} {name}'
            if new_cases:
                new_cases = new_cases.replace('+', '')
                new_cases = f'(+{new_cases})'
            if new_deaths:
                new_deaths = new_deaths.replace('+', '')
                new_deaths = f'(+{new_deaths})'

            deaths = deaths or 0
            recovered = recovered or 0

            lines = [f':microbe: **{total}{new_cases}**']
            lines += [f':skull: **{deaths}{new_deaths}**']
            lines += [f'{RECOVERED_EMOTE} **{recovered}**']
            lines += ['__']
            content = '\n'.join(lines)
            embed.add_field(name=name, value=content)
        await msg.edit(content='', embed=embed)
    
    @commands.group(name='reddit', hidden=True)
    async def _reddit(self, context): pass

    @_reddit.command()
    async def top(self, context, sub:typing.Optional[reddit.valid_subname]='popular', posts:int=1):
        await context.trigger_typing()

        for i in range(posts):
            post = await self.reddit_rss.top(sub, i)
            embed = colors.embed(title=post.title, url=post.url, description=post.text) \
                .set_author(name=post.sub, url=reddit.get_sub_url(sub), icon_url=post.sub_logo) \
                .set_thumbnail(url=post.thumbnail or '') \
                .set_image(url=post.image) \
                .set_footer(text='Reddit', icon_url=reddit.ICON_URL)
            if post.content_url:
                embed.add_field(name='Link', value=post.content_url_field)
            await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))