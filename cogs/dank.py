import discord
import re
import const
import env

from discord.ext import commands
from .core.dank import plstrivia
from .core.dank.unscramble import unscramble

TRIVIA_QUESTION = 'trivia question'
DANK_MEMER = 'Dank Memer'

RETYPE = 'Type'
TYPING = 'typing'
COLOR = 'Color'
MEMORY = 'Memory'
REVERSE = 'Reverse'
SCRAMBLE = 'Scramble'
PUNCH = 'punch'
GAMES_TO_HELP = [RETYPE, COLOR, MEMORY, REVERSE, TYPING, SCRAMBLE]

WORD_PATTERN = '`(.+)`'
COLOR_WORD_PATTERN = ':(\w+):.* `([\w-]+)`'
INVISIBLE_TRAP = '﻿'
COLOR_WORD_FORMAT = ':{color}_square: `{word}` = `{color}`'

TRIVIA_OPTIONS = ' 🇦🇧🇨🇩'
TRIVIA_LETTERS = ' ABCD'
EVENT_ENCOUNTERED = 'EVENT ENCOUNTERED'
UNSCRAMBLE_ERROR = ':warning: Could not unscramble word'

GAMBLING_ADDICT = 'Gambling Addict'
RETADABAR_ID = 614712933997346817

class DankHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if env.TESTING: return
        not_dank_memer_or_self = msg.author.name not in [DANK_MEMER, self.bot.user.name]
        in_dm = isinstance(msg.channel, discord.DMChannel)
        if not_dank_memer_or_self or in_dm: return

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
            letter = TRIVIA_LETTERS[no]
            response = f'The answer is **{letter}**) *{answer}*'
            emoji = TRIVIA_OPTIONS[no]
            await msg.add_reaction(emoji)
        else:
            response = 'I dunno man ' + const.SHRUG
            content = 'New trivia question not in database:'
            await self.bot.owner.send(content, embed=msg.embeds[0])
        await msg.channel.send(response)
    
    async def send_minigame_assist(self, msg):
        content = msg.content.replace(INVISIBLE_TRAP, '')
        words_in_backticks = re.findall(WORD_PATTERN, content)

        if COLOR in msg.content:
            lines = []
            color_word_pairs = re.findall(COLOR_WORD_PATTERN, content)
            for color, word in color_word_pairs:
                lines += [COLOR_WORD_FORMAT.format(color=color, word=word)]
            content = '\n'.join(lines)
        elif REVERSE in msg.content:
            content = words_in_backticks[0][::-1]
        elif SCRAMBLE in msg.content:
            word = words_in_backticks[0]
            anagrams = await unscramble(word)
            content = UNSCRAMBLE_ERROR
            if len(anagrams) == 1:
                content = anagrams[0]
            elif len(anagrams) >= 2:
                anagrams = ' '.join(f'`{a}`' for a in anagrams)
                content = '**Anagrams**: ' + anagrams
            else:
                content = '**Anagrams**: Not found!'
        elif any(word in msg.content for word in [RETYPE, TYPING]) and PUNCH not in msg.content:
            content = words_in_backticks[0]
        elif MEMORY in msg.content:
            content = content.split('`')[1].replace('\n', ' ')
        else:
            return

        await msg.channel.send(content)

def setup(bot):
    bot.add_cog(DankHelper(bot))
