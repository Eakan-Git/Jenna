import discord
import re
import const

from discord.ext import commands

class Alpha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rl'], hidden=True)
    @commands.is_owner()
    async def reload(self, context, cog_name):
        await context.trigger_typing()
        cog = 'cogs.' + cog_name
        self.bot.reload_extension(cog)
        await context.send(f'Cog `{cog_name}` reloaded!')
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def repeat(self, context, msg_id:int, channel:discord.TextChannel=None):
        if not channel:
            channel = context.channel
        
        async with context.typing():
            async for msg in channel.history(limit=None):
                if msg.id == msg_id:
                    embed = msg.embeds[0] if msg.embeds else None
                    await context.send(msg.content, embed=embed)
                    return
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def clean(self, context, count:int=1):
        async with context.typing():
            deleted = 0
            async for message in context.history(limit=None):
                if message.author == self.bot.user:
                    await message.delete()
                    deleted += 1
                if deleted >= count:
                    return

def setup(bot):
    bot.add_cog(Alpha(bot))
