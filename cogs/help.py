import discord
import colors
import cogs
import converter
import traceback
import sys

from discord.ext import commands

INVISBLE = '‏‏‎ ‎'

BRIEFS = {
    'snipe': 'Show the `i`th last deleted message in channel',
    'snipedit': 'Show the `i`th last edited message in channel',
    'snipelog': 'Show last 10 deleted messages in `channel`',
    'editlog': 'Show last 10 edited messages in `channel`',
    'life path': 'Get life path number from `DOB`',
    'lasotuvi': 'Get your **la so tu vi** from [tuvilyso.vn](https://tuvilyso.vn)',
    'avatar': 'Zoom in on someone\'s avatar before they yeet it',
    'do math': 'Compute big numbers for you',
    'whos': '*Who is this guy?*',
    'emotes': 'Lemme drop a Nitro emoji for you',
    'drop': 'React a message with a Nitro emoji',
    'upsidedown': 'Write texts uʍop ǝpᴉsdn for your mates in the Southern Hemisphere.',
    'rps': 'Play a game of Rock Paper Scissors with your friend',
    'invite': 'Invite me to your server!',
    'mock': 'mOkK WhAt yOuR FrIeMd sAyS',
    'enlarge': 'Show a big version of an emoji',
}

COG_EMOTES = {
    'Texts': '🗨️',
    'Images': '🖼️',
    'S': 'hypertranscendence',
    'Snipe': '🕵',
    'Emotes': 'me',
    'Games': '🎲',
    'Misc': '♾️',
}

COG_FROM_EMOTES = { v: k for k, v in COG_EMOTES.items() }

GLOBE = '🌐'
HIDDEN_COGS = ['Help', 'Alpha']
DEFAULT_HELP = '_Either DJ\'s too lazy or forget to write this_'
DEFAULT_COG = 'Misc'
TITLE_FORMAT = '%s Command List'
FOOTER = 'Nag DJ for more features'

ARG_REPLACES = {
    '[': '(',
    ']': ')',
    '> <': ' ',
    '<': '[',
    '>': ']',
}

class EmbedHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command, with_args=False):
        aliases = [command.qualified_name] + command.aliases
        signature = '/'.join(aliases)
        if with_args:
            args = command.signature
            for a, b in ARG_REPLACES.items():
                args = args.replace(a, b)
            signature += ' ' + args
        return signature.strip()
    
    def create_embed(self):
        bot = self.context.bot
        bot_user = bot.user
        embed = colors.embed(title=TITLE_FORMAT % bot_user.name)
        embed.set_footer(text=FOOTER, icon_url=bot_user.avatar_url)
        return embed
    
    async def get_cog_full_name(self, cog):
        cog = cog or DEFAULT_COG
        cog_name = cog if type(cog) is str else cog.qualified_name
        emote = await converter.emoji(self.context, COG_EMOTES[cog_name])
        full_name = f'{emote} {cog_name}'
        return full_name

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
            if cog_name in HIDDEN_COGS: continue

            commands = cog.walk_commands() if cog else commands
            command_names = cog_to_commands.get(cog_name, [])
            for command in commands:
                if command.hidden or command in done: continue
                
                signature = self.get_command_signature(command)
                command_names += [signature]
                done += [command]
            
            if command_names:
                cog_to_commands[cog_name] = command_names
                
        for cog, commands in cog_to_commands.items():
            cog_name = await self.get_cog_full_name(cog)
            commands = ' '.join(f'`{c}`' for c in commands)
            embed.add_field(name=cog_name, value=commands, inline=False)
        
        return embed

    async def add_buttons(self, msg):
        React = self.context.bot.get_cog(cogs.REACT)
        await React.add_buttons(msg, COG_EMOTES.values(), self.jump_help, self.context.author)
        await React.add_button(msg, GLOBE, self.jump_help, self.context.author)
        await React.add_delete_button(msg, self.context.author)

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

        await self.add_buttons(msg)
    
    async def get_cog_help(self, cog):
        embed = self.create_embed()
        command_helps = []
        for command in set(cog.walk_commands()):
            if type(command) is not commands.Command or command.hidden: continue
            command_helps += [self.get_command_help(command)]
        
        command_helps = '\n\n'.join(command_helps)
        cog_name = await self.get_cog_full_name(cog)
        embed.add_field(name=cog_name, value=command_helps)
        return embed

    async def send_command_help(self, command):
        embed = self.create_embed()
        embed.description = self.get_command_help(command)
        msg = await self.get_destination().send(embed=embed)

        await self.add_buttons(msg)
    
    def get_command_help(self, command):
        signature = self.get_command_signature(command, with_args=True)
        brief = BRIEFS.get(command.qualified_name, DEFAULT_HELP)
        return f'`{signature}`\n{brief}'

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')
        bot.help_command = EmbedHelpCommand()
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f'Missing `{error.param.name}` argument!')
            else:
                await ctx.send(error)
            msg = await ctx.send_help(ctx.command)
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(Help(bot))