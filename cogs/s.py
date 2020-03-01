import discord

from discord.ext import commands

class S(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(hidden=True)
    async def life(self, context):
        pass
    
    @life.command()
    async def path(self, context, *DOB):
        await self.reply_lifepath(context, *DOB)

    @commands.command(hidden=True)
    async def lifepath(self, context, *dob):
        await self.reply_lifepath(context, *dob)

    async def reply_lifepath(self, context, *dob):
        await context.trigger_typing()
        if not dob:
            await context.send('Enter a birthday duh...')
            return
        if len(dob) == 1 and '/' in dob[0]:
            dob = dob[0].split('/')
        dob_str = '/'.join(dob)
        dob = map(int, dob)
        lifepath = sum(dob) % 9
        if lifepath == 0:
            lifepath = 9
        await context.send(f'The Life Path for **{dob_str}** is **Number {lifepath}**')

def setup(bot):
    bot.add_cog(S(bot))