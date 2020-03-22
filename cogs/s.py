import discord
import base64
import colors
import typing
import converter as conv

from discord.ext import commands

LANG = 1
COLOR = 5
SAVE = 0
TU_HOA = 1
FORMAT = 1
KHOI_VIET = 0
IS_SOUTH = 0
TIET_KHI = 1
TIMEZONE = 7
TUOI_NHAM = 2
MINUTE = '00'

LSTV_SETTINGS_1 = [LANG, COLOR, SAVE, TU_HOA, FORMAT, KHOI_VIET, IS_SOUTH]
LSTV_SETTINGS_2 = [MINUTE, TIET_KHI, TIMEZONE, TUOI_NHAM]

LSTV_URL = 'https://tuvilyso.vn/lasotuvi/%s.png'
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

class S(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(hidden=True)
    async def life(self, context):
        pass
    
    @life.command()
    async def path(self, context, dob:conv.DOB):
        await self.reply_lifepath(context, dob)

    @commands.command(hidden=True)
    async def lifepath(self, context, dob:conv.DOB):
        await self.reply_lifepath(context, dob)

    async def reply_lifepath(self, context, dob):
        await context.trigger_typing()
        lifepath = sum(dob.numbers) % 9
        if lifepath == 0:
            lifepath = 9
        await context.send(f'The Life Path for **{dob}** is **Number {lifepath}**')
    
    @commands.command(aliases=['lstv'])
    async def lasotuvi(self, context, dob:conv.DOB, birthtime:BirthTime, gender:conv.Gender, *, name=None):
        name = name or DEFAULT_NAME

        day, month, year = dob.numbers
        horoscope_hour = compute_horoscope_hour(birthtime)

        data = [year, month, day, horoscope_hour, gender, name] + LSTV_SETTINGS_1 + [birthtime] + LSTV_SETTINGS_2
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