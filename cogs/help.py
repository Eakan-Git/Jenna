import discord
import colors
import const

from discord.ext import commands

BRIEFS = {
    'snipe': 'Show the `i`th last deleted message in channel',
    'snipe edit': 'Show the `i`th last edited message in channel',
    'snipelog': 'Show all logged deleted messages in `channel`',
    'editlog': 'Show all logged edited messages in `channel`',
    'life path': 'Get life path number from `DOB`',
    'avatar': 'Zoom in on someone\'s avatar before they yeet it',
    'do math': 'Compute big numbers for you',
    'whos': '*Who is this guy?*',
}

HIDDEN_PARAMS = {
    'snipe': ['subindex']
}

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
    
    @commands.command(hidden=True)
    async def help(self, context):
        embed = discord.Embed(title=f'{self.bot.user.name} Command List', color=colors.random())
        embed.set_footer(text='Nag DJ for more features', icon_url=self.bot.user.avatar_url)

        done = []
        cogs_to_fields = {}
        for cog_name, cog in self.bot.cogs.items():
            fields = []
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
                        if p not in HIDDEN_PARAMS.get(command.qualified_name, []):
                            params += [p]

                    params = ', '.join(params)
                    name += f' [{params}]'

                brief = BRIEFS.get(command.qualified_name)
                fields += [(name, brief)]
            
            if fields:
                cogs_to_fields[cog_name] = fields
            
        longest_name_len = max([len(name) for fields in cogs_to_fields.values() for name, _ in fields])
        for cog_name, fields in cogs_to_fields.items():
            lines = []
            for name, brief in fields:
                name = f'`{name}`'
                pad_count = (longest_name_len - len(name)) * 2 + 4
                pad = const.INVISBLE * pad_count
                name = name + pad
                lines += [f'{name} {brief}']
            lines = '\n\n'.join(lines)

            embed.add_field(name=cog_name, value=lines, inline=False)

        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))