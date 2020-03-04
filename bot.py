import os
import discord
import colors
import env

from discord.ext import commands

prefixes = ['j ']
for p in prefixes[::]:
    prefixes.append(p.capitalize())
bot = commands.Bot(command_prefix=prefixes)

extensions = [
    # 'cogs.images',
    # 'cogs.s',
    # 'cogs.snipe',
    # 'cogs.misc',

    # 'cogs.dank_helper',
    # 'cogs.help',
    'cogs.alpha'
]

if __name__ == '__main__':
    for ex in extensions:
        bot.load_extension(ex)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('j help'))
    print('Logged in as', bot.user)

if __name__ == '__main__':
    bot.run(env.BOT_TOKEN)