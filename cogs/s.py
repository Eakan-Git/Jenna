import discord
import colors
import converter as conv

from discord.ext import commands
from bs4 import BeautifulSoup
from s import lsqc, lstv, BirthTime, get_lifepath

class S(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(hidden=True)
    async def life(self, context):
        pass
    
    @life.command()
    async def path(self, context, dob:conv.DOB):
        await self.send_lifepath(context, dob)

    @commands.command(hidden=True)
    async def lifepath(self, context, dob:conv.DOB):
        await self.send_lifepath(context, dob)

    async def send_lifepath(self, context, dob):
        lifepath = get_lifepath(dob)
        await context.send(f'The Life Path for **{dob}** is **Number {lifepath}**')
    
    @commands.command(aliases=['lstv'])
    async def lasotuvi(self, context, dob:conv.DOB, birthtime:BirthTime, gender:conv.Gender, *, name=None):
        image_url = lstv.compile_url(dob, birthtime, gender, name)
        gender = '♂️' if gender == conv.MALE else '♀️'
        embed = colors.embed(title=f'{gender} {dob} {birthtime}h')
        embed.set_image(url = image_url)

        await context.send(embed=embed)
    
    @commands.command(aliases=['lsqc'])
    async def lasoquycoc(self, context, dob:conv.DOB, birthtime:BirthTime):
        await context.trigger_typing()
        qc = lsqc.lookup(dob, birthtime)
        text = qc.format_laso()
        print(text)

        embed = colors.embed(title=f'Lá số Quỷ Cốc {dob} {birthtime}h')
        embed.url = lsqc.compile_url(dob, birthtime)
        qc.add_details_as_field(embed)
        await context.send(text, embed=embed)

def setup(bot):
    bot.add_cog(S(bot))