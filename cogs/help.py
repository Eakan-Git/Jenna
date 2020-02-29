import discord
import colors

from discord.ext import commands

briefs = {
    'snipe': 'Show the `i`th last deleted message',
    'snipe edit': 'Show the `i`th last edited message',
    'snipelog': 'Show all logged deleted messages in channel',
    'editlog': 'Show all logged edited messages in channel',
    'life path': 'Get your life path number from a birthday. Ask S for further info.\n`dob`: separated by space or /',
    'avatar': 'Zoom in on someone\'s avatar before they yeet it',
    'do math': 'Compute big numbers for you',
    'help': 'Show this message',
}

default_params = {
    'snipe': [1],
    'snipe edit': [1],
    'avatar': ['you'],
    'snipelog': ['current'],
    'editlog': ['current'],
}

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
    
    @commands.command()
    async def help(self, context):
        embed = discord.Embed(title=f'{self.bot.user.name} Command List', color=colors.random())
        embed.set_footer(text='Nag DJ for more features', icon_url=self.bot.user.avatar_url)

        done = []
        for _, cog in self.bot.cogs.items():
            for command in cog.walk_commands():
                if command.hidden: continue
                name = command.qualified_name

                if name in done:
                    continue
                done.append(name)
                
                for a in command.aliases:
                    name += '/' + a
                
                if command.clean_params:
                    params = []
                    for i, p in enumerate(command.clean_params):
                        if p.startswith('_'): continue
                        defaults = default_params.get(name)
                        if defaults:
                            p += f'={defaults[i]}'
                        params += [p]

                    params = ', '.join(params)
                    name += f' [{params}]'

                brief = briefs.get(command.qualified_name)
                embed.add_field(name=name, value=brief or 'No description')

        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))