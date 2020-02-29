import discord
import colors
import const
import convert

from discord.ext import commands
from math import *

MATH_OPERATIONS = {
    'x': '*',
    ',': '',
    '^': '**',
}

MATH_BRIEF = 'Compute big numbers for you'

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(hidden=True)
    async def do(self, context):
        if not context.invoked_subcommand:
            await context.send('`do meth` you mean?')

    @do.command(aliases=['meth'])
    async def math(self, context, *expression):
        expr = expression
        if expr:
            expr = ''.join(expr)
            for math, code in MATH_OPERATIONS.items():
                expr = expr.replace(math, code)
        else:
            return
        try:
            value = eval(expr)
            if value:
                value = f'{value:,}'
                response = f"That's **{value}**"
                await context.send(response)
        except:
            import traceback
            traceback.print_exc()
    
    @commands.command(hidden=True)
    @commands.guild_only()
    async def whos(self, context, member_name):
        member = convert.find_member(context, member_name)

        if member:
            response = f'It\'s **{member.name}#{member.discriminator}**'
        else:
            response = 'I dunno who! ' + const.SHRUG
        await context.send(response)
    
def setup(bot):
    bot.add_cog(Misc(bot))