import discord
import colors
import random

from discord.ext import commands
from bs4 import BeautifulSoup
from .core import converter as conv
from .core.s import lsqc, lstv, get_lifepath, BirthTime, tarot

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

        embed = colors.embed(title=f'Lá số Quỷ Cốc {dob} {birthtime}h')
        embed.url = lsqc.compile_url(dob, birthtime)
        qc.add_details_as_field(embed)
        await context.send(text, embed=embed)
    
    @commands.command()
    async def tarot(self, context):
        card = random.choice(tarot.CARDS)
        name, image, url = card
        embed = colors.embed(title=name, url=url)
        embed.set_image(url=image)
        embed.set_footer(text='Tip: Click the title to see the meaning!')
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(S(bot))