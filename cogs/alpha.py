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
    async def clean(self, context, limit:int=1):
        is_dm = type(context.channel) is discord.DMChannel
        is_owner = await self.bot.is_owner(context.author)
        allowed = is_owner or is_dm
        if not allowed: return

        def is_me(m):
            return m.author == self.bot.user
        progress_msg = await context.send('Deleting...')
        
        msgs_to_delete = []
        deleted = 0
        async for m in context.history(limit=None):
            if is_me(m) and m.id != progress_msg.id:
                msgs_to_delete += [m]
                deleted += 1
                if deleted >= limit:
                    break
        
        if is_dm:
            for i, m in enumerate(msgs_to_delete):
                await m.delete()
                await progress_msg.edit(content=f'Deleted `{i+1}/{len(msgs_to_delete)}` messages!')
        else:
            await context.channel.delete_messages(msgs_to_delete)
            await progress_msg.edit(content=f'Deleted `{len(msgs_to_delete)}` messages!')
        
        await progress_msg.edit(delete_after=3)


def setup(bot):
    bot.add_cog(Alpha(bot))
