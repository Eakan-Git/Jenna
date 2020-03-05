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
GAMES_TO_HELP = [RETYPE, COLOR, MEMORY]

TYPE_PATTERN = 'Type `(.+)`'
COLOR_WORD_PATTERN = ':(\w+):.* `(\w+)`'
INVISIBLE_TRAP = '﻿'

class DankHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.name != DANK_MEMER: return

        is_trivia_question = msg.embeds and msg.embeds[0].author and TRIVIA_QUESTION in msg.embeds[0].author.name
        
        if is_trivia_question:
            await msg.channel.trigger_typing()
            trivia = plstrivia.read(msg.embeds[0].description)
            answer = plstrivia.try_answer(trivia)
            if answer:
                no = trivia.answers.index(answer)
                response = f'The answer is ||**{no})** *{answer}*||'
            else:
                response = 'I dunno man ' + const.SHRUG
            await msg.channel.send(response)
        
        if any(word in msg.content for word in GAMES_TO_HELP):
            await msg.channel.trigger_typing()
            content = '\n'.join(msg.content.split('\n')[1:])
            content = content.replace(INVISIBLE_TRAP, '')

            if RETYPE in msg.content:
                content = re.findall(TYPE_PATTERN, content)[0]
            elif MEMORY in msg.content:
                content = content.replace('`', '').replace('\n', ' ')
            elif COLOR in msg.content:
                color_word_pairs = re.findall(COLOR_WORD_PATTERN, content)
                lines = []
                for color, word in color_word_pairs:
                    lines += [f':{color}_square: `{word}`']
                content = '\n'.join(lines)
            await msg.channel.send(content)

def setup(bot):
    bot.add_cog(DankHelper(bot))