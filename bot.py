import os
import discord
import colors
import env

from discord.ext import commands

prefixes = ['j ', 'jenna ', 'jen ']
for p in prefixes[::]:
    prefixes.append(p.capitalize())
bot = commands.Bot(command_prefix=prefixes, case_insensitive=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('j help'))
    print('Logged in as', bot.user)

extensions = [
    'dank_helper',
    'help',
    'alpha',
    'react',

    'texts',
    'images',
    's',
    'snipe',
    'emotes',
    'games',

    'misc',
]

extensions = ['cogs.' + ext for ext in extensions]

if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)
    bot.run(env.BOT_TOKEN)