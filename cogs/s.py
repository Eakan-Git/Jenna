import discord
import base64
import colors

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
MINUTE = 0

GENDERS = ['M', 'F']
LSTV_URL = 'https://tuvilyso.vn/lasotuvi/%s.png'

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
    
    @commands.command(aliases=['lstv'])
    async def lasotuvi(self, context, dob, hour:int, gender, *, name='Psychic Ritord'):
        gender = gender.upper()
        if gender not in GENDERS:
            await context.send('`gender` must be `M` or `F`')
            return
        gender = GENDERS.index(gender) + 1
        
        dob = parse_dob(dob)
        if not dob:
            await context.send('`dob` must be in `DD-MM-YYYY` format')
            return
        day, month, year = map(int, dob)
        horoscope_hour = compute_horoscope_hour(hour)

        data = [year, month, day, horoscope_hour, gender, name, LANG, COLOR, SAVE, TU_HOA, FORMAT, KHOI_VIET, IS_SOUTH, hour, MINUTE, TIET_KHI, TIMEZONE, TUOI_NHAM]
        data = '|'.join(str(d) for d in data)
        data = base64.b64encode(bytes(data, 'utf-8')).decode('ascii')

        image_url = LSTV_URL % data

        embed = colors.embed()
        embed.set_image(url = image_url)

        await context.send(embed=embed)
    
    @lasotuvi.error
    async def lstv_error(self, context, error):
        await context.send('The syntax is `j lasotuvi [dob] [hour] [gender]`')
    
def parse_dob(dob):
    try:
        dob = dob.split('-')
        d, m, y = map(int, dob)
    except:
        return
    return dob

def compute_horoscope_hour(hour):
    hh = (hour + 1) // 2 + 1
    if hh == 13:
        hh = 1
    return hh

def setup(bot):
    bot.add_cog(S(bot))