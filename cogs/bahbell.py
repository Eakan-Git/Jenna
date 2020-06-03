from discord.ext import commands
from .core import converter as conv
from .cmds.bahbell import bfp, mass, wilks
from typing import Optional

import discord
import colors

class Bahbell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['bfp'])
    async def bodyfat(self, context, gender:conv.Gender, height:float, neck:float, waist:float, hip:Optional[float]):
        embed = bfp.embed(gender, height, neck, waist, hip)
        await context.send(embed=embed)

    @commands.command()
    async def kg2lbs(self, context, kg:float):
        await context.send(mass.respond_kg2lbs(kg))

    @commands.command()
    async def lbs2kg(self, context, lbs:float):
        await context.send(mass.respond_lbs2kg(lbs))
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        await mass.process_commands(message)
    
    @commands.command()
    async def wilks(self, context, gender:conv.Gender, bodyweight:float, lifted_weight:float=1):
        embed = wilks.embed(gender, bodyweight, lifted_weight)
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Bahbell(bot))