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
    'cogs.dank_helper',
    'cogs.images',
    'cogs.misc',
    'cogs.snipe',
    'cogs.s',
]

if __name__ == '__main__':
    for ex in extensions:
        bot.load_extension(ex)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('j help'))
    print('Logged in as', bot.user)

bot.remove_command('help')

@bot.command()
async def help(context):
    embed = discord.Embed(title=f'{bot.user.name} Command List', color=colors.random())
    embed.set_footer(text='Nag DJ for more features', icon_url=bot.user.avatar_url)

    done = []
    for _, cog in bot.cogs.items():
        for command in cog.walk_commands():
            if command.hidden: continue
            name = command.name

            if name in done:
                continue
            done.append(name)
            
            for a in command.aliases:
                name += '/' + a

            if command.parent:
                name = command.parent.name + ' ' + name
            
            if command.clean_params:
                params = ', '.join(command.clean_params)
                name += f' [{params}]'
            
            desc = command.brief

            if command.usage:
                desc += f'\n\n*{command.usage}*'
            
            embed.add_field(name=name, value=desc or 'No description')

    await context.send(embed=embed)

if __name__ == '__main__':
    bot.run(env.BOT_TOKEN)