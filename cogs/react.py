import discord
import typing
import converter

from discord.ext import commands
from collections.abc import Iterable

X = '❌'
OK = '✅'

class Reactable:
    def __init__(self, msg, user=[]):
        if not isinstance(user, Iterable):
            user = [user]
        self.msg = msg
        self.user = user
        self.callbacks_by_emoji = {}
    
    def add_button(self, emoji, callback):
        self.callbacks_by_emoji[emoji] = callback
    
    def get_callback(self, reaction, user):
        for emoji, callback in self.callbacks_by_emoji.items():
            if reaction.emoji == emoji and user in self.user:
                return callback

class React(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactables = {}
    
    async def delete(self, reaction, user):
        message = reaction.message
        await message.delete()
        self.remove_reactable(message)
    
    def remove_reactable(self, message):
        if message.id in self.reactables:
            self.reactables.pop(message.id)
        
    async def add_delete_button(self, message, user=[]):
        await self.add_button(message, OK, self.delete, user)

    async def add_buttons(self, message, emojis, callback, user=[]):
        try:
            for e in emojis:
                await self.add_button(message, e, callback, user)
        except:
            pass # message deleted while adding

    async def add_button(self, message, emoji, callback, user=[]):
        if message.id not in self.reactables:
            self.reactables[message.id] = Reactable(message, user)
        reactable = self.reactables[message.id]
        emoji = await self.add_reaction(message, emoji)
        reactable.add_button(emoji, callback)
    
    async def add_reaction(self, message, emoji):
        context = await self.bot.get_context(message)
        emoji = await converter.emoji(context, emoji)
        await message.add_reaction(emoji)
        return emoji

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user: return
        reactable = self.reactables.get(reaction.message.id)
        if not reactable: return
        callback = reactable.get_callback(reaction, user)
        if callback:
            await callback(reaction, user)

def setup(bot):
    bot.add_cog(React(bot))