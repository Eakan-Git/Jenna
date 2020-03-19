import discord
import re
import const

from discord.ext import commands
from trivia import plstrivia

TRIVIA_QUESTION = 'trivia question'
DANK_MEMER = 'Dank Memer'

RETYPE = 'Type'
TYPING = 'typing'
COLOR = 'Color'
MEMORY = 'Memory'
REVERSE = 'Reverse'
GAMES_TO_HELP = [RETYPE, COLOR, MEMORY, REVERSE, TYPING]

WORD_PATTERN = '`(.+)`'
COLOR_WORD_PATTERN = ':(\w+):.* `([\w-]+)`'
INVISIBLE_TRAP = '﻿'
COLOR_WORD_FORMAT = ':{color}_square: `{word}` = `{color}`'

TRIVIA_OPTIONS = ' ABCD'
OPTION_EMOJIS = ' 🇦🇧🇨🇩'
EVENT_ENCOUNTERED = 'EVENT ENCOUNTERED'

GAMBLING_ADDICT = 'Gambling Addict'
RETADABAR_ID = 614712933997346817

class DankHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if type(msg.channel) is discord.DMChannel: return
        if msg.author.name not in [DANK_MEMER, self.bot.user.name]: return

        is_trivia_question = self.is_trivia(msg)
        is_minigame = any(word in msg.content for word in GAMES_TO_HELP)
        is_event = EVENT_ENCOUNTERED in msg.content

        help = None
        if is_trivia_question:
            help = self.send_answer
        elif is_minigame:
            help = self.send_minigame_assist
        elif is_event:
            help = self.ping_players

        if help:
            await help(msg)
    
    def is_trivia(self, msg):
        is_embed = msg.embeds and msg.embeds[0].author and TRIVIA_QUESTION in msg.embeds[0].author.name
        is_event_trivia = msg.content.count('\n') == msg.content.count(') ') == 4
        return is_embed or is_event_trivia

    async def ping_players(self, msg):
        if msg.guild.id != RETADABAR_ID: return
        player_role = discord.utils.get(msg.guild.roles, name=GAMBLING_ADDICT)
        await msg.channel.send(f'{player_role.mention} This is a **NOT** test!')
    
    async def send_answer(self, msg):
        await msg.channel.trigger_typing()
        trivia = plstrivia.read(msg.content or msg.embeds[0].description)
        answer = plstrivia.try_answer(trivia)
        if answer:
            no = trivia.answers.index(answer)
            letter = TRIVIA_OPTIONS[no]
            response = f'The answer is **{letter})** *{answer}*'
            emoji = OPTION_EMOJIS[no]
            await msg.add_reaction(emoji)
        else:
            response = 'I dunno man ' + const.SHRUG
            content = 'New trivia question not in database:'
            await self.bot.get_user(self.bot.owner_id).send(content, embed=msg.embeds[0])
        await msg.channel.send(response)
    
    async def send_minigame_assist(self, msg):
        await msg.channel.trigger_typing()
        content = msg.content.replace(INVISIBLE_TRAP, '')

        if COLOR in msg.content:
            lines = []
            color_word_pairs = re.findall(COLOR_WORD_PATTERN, content)
            for color, word in color_word_pairs:
                lines += [COLOR_WORD_FORMAT.format(color=color, word=word)]
            content = '\n'.join(lines)
        elif any(word in msg.content for word in [RETYPE, TYPING]):
            content = re.findall(WORD_PATTERN, content)[0]
        elif MEMORY in msg.content:
            content = ' '.join(re.findall(WORD_PATTERN, content))
        elif REVERSE in msg.content:
            content = re.findall(WORD_PATTERN, content)[0][::-1]

        await msg.channel.send(content)

def setup(bot):
    bot.add_cog(DankHelper(bot))
