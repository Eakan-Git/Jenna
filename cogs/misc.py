import discord
import colors
import const
import convert
import timedisplay

from discord.ext import commands
from math import *

MATH_OPERATIONS = {
    'x': '*',
    ',': '',
    '^': '**',
}

MATH_BRIEF = 'Compute big numbers for you'
INVITE_LINK = 'https://discordapp.com/api/oauth2/authorize?client_id=664109951781830666&permissions=1342565440&scope=bot'

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(hidden=True)
    async def do(self, context):
        if not context.invoked_subcommand:
            await context.send('`do meth` you mean?')

    @do.command(aliases=['meth'])
    async def math(self, context, *expr):
        if expr:
            expr = ''.join(expr)
            for math, code in MATH_OPERATIONS.items():
                expr = expr.replace(math, code)
        else:
            return
        try:
            value = eval(expr)
            if value is not None:
                value = f'{value:,}'
                response = f"That's **{value}**"
                await context.send(response)
        except Exception as e:
            await context.send("That's *bruh!*")
            import traceback
            traceback.print_exc()

    @commands.command()
    @commands.guild_only()
    async def whos(self, context, *, name=None):
        member = await convert.to_user(context, name)

        embed = None
        if member:
            response = f'It\'s **{member}**'
            embed = colors.embed()
            embed.description = member.mention
            created_at = timedisplay.to_ict(member.created_at, timedisplay.DAYWEEK_DAY_IN_YEAR)
            joined_at = timedisplay.to_ict(member.joined_at, timedisplay.DAYWEEK_DAY_IN_YEAR)
            embed \
                .set_thumbnail(url=member.avatar_url) \
                .add_field(name='On Discord since', value=created_at, inline=False) \
                .add_field(name='Joined on', value=joined_at)
        else:
            response = 'I dunno who! ' + const.SHRUG
        await context.send(response, embed=embed)
    
    @commands.command(aliases=['usd'])
    async def upsidedown(self, context, *, text=None):
        if not text:
            text = 'Enter some text!'
        import upsidedown
        text = text.replace('||', '')
        text = upsidedown.transform(text)
        await context.send(text)
    
    @commands.command()
    async def invite(self, context):
        worryluv = discord.utils.get(self.bot.emojis, name='worryluv')
        embed = colors.embed()
        embed.description = f'{worryluv} [Click here]({INVITE_LINK}) to invite Jenna!'
        await context.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Misc(bot))