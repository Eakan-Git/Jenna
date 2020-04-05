import os
import discord
import colors
import env
import logging
import cogs

from discord.ext import commands

prefixes = ['j ', 'jenna '] if not env.TESTING else ['k ']
for p in prefixes[::]:
    prefixes.append(p.capitalize())
bot = commands.Bot(command_prefix=prefixes, case_insensitive=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('j help'))
    print('Logged in as', bot.user)

if __name__ == '__main__':
    for cog in cogs.LIST:
        bot.load_extension(cog)
    bot.run(env.BOT_TOKEN)