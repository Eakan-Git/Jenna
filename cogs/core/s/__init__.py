from discord.ext import commands

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