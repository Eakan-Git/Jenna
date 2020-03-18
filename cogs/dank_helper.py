import discord
import re
import const

from discord.ext import commands
from trivia import plstrivia

TRIVIA_QUESTION = 'trivia question'
DANK_MEMER = 'Dank Memer'

RETYPE = 'Retype'
COLOR = 'Color'
MEMORY = 'Memory'
REVERSE = 'Reverse'
GAMES_TO_HELP = [RETYPE, COLOR, MEMORY, REVERSE]

WORD_PATTERN = '`(.+)`'
COLOR_WORD_PATTERN = ':(\w+):.* `([\w-]+)`'
INVISIBLE_TRAP = '﻿'
MAINTAINER_ID = 134689471164710912

TRIVIA_OPTIONS = ' ABCD'

class DankHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if type(msg.channel) is discord.DMChannel: return
        if msg.author.name not in [DANK_MEMER, self.bot.user.name]: return

        is_trivia_question = msg.embeds and msg.embeds[0].author and TRIVIA_QUESTION in msg.embeds[0].author.name
        
        if is_trivia_question:
            await msg.channel.trigger_typing()
            trivia = plstrivia.read(msg.embeds[0].description)
            answer = plstrivia.try_answer(trivia)
            if answer:
                no = trivia.answers.index(answer)
                letter = TRIVIA_OPTIONS[no]
                response = f'The answer is **{letter})** *{answer}*'
            else:
                response = 'I dunno man ' + const.SHRUG
                content = 'New trivia question not in database:'
                await self.bot.get_user(MAINTAINER_ID).send(content, embed=msg.embeds[0])
            await msg.channel.send(response)
        
        if any(word in msg.content for word in GAMES_TO_HELP):
            await msg.channel.trigger_typing()
            content = '\n'.join(msg.content.split('\n')[1:])
            content = content.replace(INVISIBLE_TRAP, '')

            if COLOR in msg.content:
                lines = []
                color_word_pairs = re.findall(COLOR_WORD_PATTERN, content)
                for color, word in color_word_pairs:
                    lines += [f':{color}_square: `{word}` = `{color}`']
                content = '\n'.join(lines)
            elif RETYPE in msg.content:
                content = re.findall(WORD_PATTERN, content)[0]
            elif MEMORY in msg.content:
                content = content.replace('`', '').replace('\n', ' ')
            elif REVERSE in msg.content:
                content = re.findall(WORD_PATTERN, content)[0][::-1]

            await msg.channel.send(content)

def setup(bot):
    bot.add_cog(DankHelper(bot))
