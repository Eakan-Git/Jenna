import discord
import colors
import cogs
import traceback
import sys
import const
import csv
import env

from discord.ext import commands
from .core import converter as conv

BRIEFS_FILE = 'cogs/core/help_briefs.csv'
with open(BRIEFS_FILE, encoding='utf8') as file:
    reader = csv.reader(file, delimiter='|')
    BRIEFS = {row[0]: row[1].strip().replace('\\n', '\n') for row in reader if row}

COG_EMOTES = {
    'Texts': '🗨️',
    'Images': '🖼️',
    'S': 'es',
    'Snipe': '🕵',
    'Emotes': 'me',
    'Games': '🎲',
    'Bahbell': '🏋️',
    'Misc': '♾️',
}

COG_FROM_EMOTES = { v: k for k, v in COG_EMOTES.items() }

GLOBE = '🌐'
DEFAULT_HELP = ''
DEFAULT_COG = 'Misc'
TITLE_FORMAT = '%s Command List'
FOOTER = 'Requested by {}'
OWNER_CHECK = 'is_owner'

ARG_NEW_BRACKETS = {
    '[': '(',
    ']': ')',
    '<': '[',
    '>': ']',
}

def owner_only(command):
    return OWNER_CHECK in str(command.checks)

class EmbedHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command, with_args=False):
        aliases = [command.qualified_name] + command.aliases
        signature = '/'.join(aliases)
        if with_args:
            args = command.signature.split()
            for i, a in enumerate(args):
                brackets = a[0] + a[-1]
                for old, new in ARG_NEW_BRACKETS.items():
                    brackets = brackets.replace(old, new)
                args[i] = brackets[0] + a[1:-1] + brackets[1]
            signature += ' ' + ' '.join(args)
        return signature.strip()
    
    def create_embed(self):
        bot = self.context.bot
        bot_user = bot.user
        requesting_user = self.context.message.author
        embed = colors.embed(title=TITLE_FORMAT % bot_user.name)
        embed.set_footer(text=FOOTER.format(requesting_user.name), icon_url=requesting_user.avatar_url)
        return embed

    async def send_bot_help(self, mapping):
        embed = await self.get_bot_help()
        msg = await self.get_destination().send(embed=embed)
        await self.add_buttons(msg)
    
    async def get_bot_help(self):
        bot = self.context.bot
        embed = self.create_embed()
        done = []
        cog_to_commands = {}
        for cog_name, cog in bot.cogs.items():
            if cog_name not in COG_EMOTES: continue

            command_names = cog_to_commands.get(cog_name, [])
            for command in cog.walk_commands():
                if command.hidden or command in done or owner_only(command): continue
                
                signature = self.get_command_signature(command)
                command_names += [signature]
                done += [command]
            
            if command_names:
                cog_to_commands[cog_name] = command_names
                
        for cog, commands in cog_to_commands.items():
            cog_name = await self.get_cog_emoted_name(cog)
            commands = const.BULLET.join(f'`{c}`' for c in commands)
            embed.add_field(name=cog_name, value=commands, inline=False)
        
        return embed

    async def get_cog_emoted_name(self, cog):
        cog = cog or DEFAULT_COG
        cog_name = cog if type(cog) is str else cog.qualified_name
        emote = await conv.emoji(self.context, COG_EMOTES[cog_name])
        full_name = f'{emote} {cog_name}'
        return full_name

    async def add_close_button(self, msg):
        await self.add_buttons(msg, full=False)

    async def add_buttons(self, msg, full=True):
        React = self.context.bot.get_cog(cogs.REACT)
        if full:
            await React.add_buttons(msg, COG_EMOTES.values(), self.jump_help, self.context.author)
            await React.add_button(msg, GLOBE, self.jump_help, self.context.author)
        await React.add_delete_button(msg, user=self.context.author)

    async def jump_help(self, reaction, user):
        emoji = reaction.emoji if type(reaction.emoji) is str else reaction.emoji.name
        if emoji == GLOBE:
            embed = await self.get_bot_help()
        else:
            cog = COG_FROM_EMOTES[emoji]
            cog = self.context.bot.get_cog(cog)
            embed = await self.get_cog_help(cog)
        
        message = reaction.message
        embed.color = message.embeds[0].color
        await message.edit(embed=embed)
        await message.remove_reaction(reaction, user)

    async def send_cog_help(self, cog):
        embed = await self.get_cog_help(cog)
        msg = await self.get_destination().send(embed=embed)

        await self.add_close_button(msg)
    
    async def get_cog_help(self, cog):
        embed = self.create_embed()
        command_helps = []
        for command in set(cog.walk_commands()):
            if command.hidden or owner_only(command): continue
            command_helps += [self.get_command_help(command)]
        
        command_helps = '\n\n'.join(command_helps)
        cog_name = await self.get_cog_emoted_name(cog)
        embed.add_field(name=cog_name, value=command_helps)
        return embed

    async def send_command_help(self, command):
        embed = self.create_embed()
        cog = await self.get_cog_emoted_name(command.cog_name)
        command_help = self.get_command_help(command)
        embed.add_field(name=cog, value=command_help)
        msg = await self.get_destination().send(embed=embed)

        await self.add_close_button(msg)
        return msg
    
    async def send_group_help(self, group):
        embed = self.create_embed()
        cog = await self.get_cog_emoted_name(group.cog_name)
        command_helps = []
        if not group.hidden:
            command_helps += [self.get_command_help(group)]
        command_helps += [self.get_command_help(c) for c in group.commands if not c.hidden]
        command_helps = '\n\n'.join(command_helps)
        embed.add_field(name=cog, value=command_helps)
        msg = await self.get_destination().send(embed=embed)
        await self.add_close_button(msg)
    
    def get_command_help(self, command):        
        signature = self.get_command_signature(command, with_args=True)
        brief = BRIEFS.get(command.qualified_name, DEFAULT_HELP)
        if brief: brief = '\n' + brief
        return f'`{signature}`{brief}'

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')
        bot.help_command = EmbedHelpCommand()
    
    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        if isinstance(error, commands.UserInputError):
            if type(error) in [commands.BadArgument, commands.BadUnionArgument]:
                error.args = (error.args[0].replace('"', '`'),)
            if type(error) is commands.MissingRequiredArgument:
                await context.send(f'Missing `{error.param.name}` argument!')
            else:
                await context.send(error)
        else:
            original = error.original if hasattr(error, 'original') else error
            exception = traceback.format_exception(type(original), original, original.__traceback__)
            exception = '\n'.join(exception)
            print(exception)
            if isinstance(error, ignored_errors): return

            msg = context.message
            source = (
                f'by {msg.author.mention} ({msg.author.display_name})\n'
                f'in {msg.channel.mention} of `{msg.guild}`\n'
                f'[Jump]({msg.jump_url})'
            )
            embed = colors.embed(description=msg.content) \
                .add_field(name='Source', value=source)
            content = f'```{exception}```'
            if context.author == self.bot.owner:
                await context.send(content, embed=embed)
            else:
                await self.bot.owner.send(content, embed=embed)

ignored_errors = (commands.CommandNotFound,)

def setup(bot):
    bot.add_cog(Help(bot))