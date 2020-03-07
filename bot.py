import os
import discord
import colors
import env

from discord.ext import commands

prefixes = ['j ', 'jenna ', 'jen ']
for p in prefixes[::]:
    prefixes.append(p.capitalize())
bot = commands.Bot(command_prefix=prefixes)

extensions = [
    'dank_helper',
    'help',
    'alpha',
    
    'images',
    's',
    'snipe',
    'emotes',

    'misc',
]

extensions = ['cogs.' + ext for ext in extensions]

if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('j help'))
    print('Logged in as', bot.user)

if __name__ == '__main__':
    bot.run(env.BOT_TOKEN)