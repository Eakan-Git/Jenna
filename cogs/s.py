import discord
import base64
import colors
import typing
import converter as conv

from discord.ext import commands


LSTV_URL = 'https://tuvilyso.vn/lasotuvi/%s.png'
LSTV_SETTINGS = '1|5|0|1|1|0|0|%s|00|1|7|2'
DEFAULT_NAME = 'Psychic Ritord'

def BirthTime(hour):
    try:
        hour = int(hour)
        if hour == 24:
            hour = 0
    except:
        hour = -1
    if not 0 <= hour <= 24:
        raise commands.BadArgument('`BirthTime` must be in 24-hour format')
    return hour

def get_lifepath(dob):
    lifepath = sum(dob.numbers) % 9
    if lifepath == 0:
        lifepath = 9
    return lifepath

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
        name = name or DEFAULT_NAME

        day, month, year = dob.numbers
        horoscope_hour = compute_horoscope_hour(birthtime)

        data = [year, month, day, horoscope_hour, gender, name, LSTV_SETTINGS % birthtime]
        data = '|'.join(str(d) for d in data)
        data = base64.b64encode(bytes(data, 'utf-8')).decode('ascii')

        image_url = LSTV_URL % data

        embed = colors.embed()
        embed.set_image(url = image_url)

        await context.send(embed=embed)

def compute_horoscope_hour(hour):
    hh = (hour + 1) // 2 + 1
    if hh == 13:
        hh = 1
    return hh

def setup(bot):
    bot.add_cog(S(bot))