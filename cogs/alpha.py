import discord
import typing
import re
import const
import cogs

from discord.ext import commands

ALL = 'all'

class Alpha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rl'])
    @commands.is_owner()
    async def reload(self, context, cog=ALL):
        await context.trigger_typing()
        responses = []
        cog = cogs.NAMES if cog == ALL else cog.split()
        
        for cog_name in cog:
            cog_path = 'cogs.' + cog_name
            response = 'Cog `%s`' % cog_name

            try:
                self.bot.reload_extension(cog_path)
                response = f'✅ {response} reloaded!'
            except:
                import traceback; traceback.print_exc()
                response = f'⚠️ {response} reload failed!'
            
            responses += [response]

        content = '\n'.join(responses)
        await context.send(content)
    
    @commands.command()
    async def clearto(self, context, to_id:int):
        await context.trigger_typing()
        msgs_to_clear = []
        async for msg in context.history(limit=None):
            msgs_to_clear += [msg]
            if msg.id == to_id:
                break
        await context.channel.delete_messages(msgs_to_clear)
        await context.send(f'Deleted `{len(msgs_to_clear)}` messages!', delete_after=3)

    @commands.command(aliases=['rp'])
    @commands.is_owner()
    async def repeat(self, context, msg_id:int, channel:discord.TextChannel=None):
        channel = channel or context.channel
        
        async with context.typing():
            msg = await channel.fetch_message(msg_id)
            embed = msg.embeds[0] if msg.embeds else None
            await context.send(msg.content, embed=embed)
    
    @commands.command()
    async def clean(self, context, limit:typing.Optional[int]=1, *, content=''):
        is_dm = type(context.channel) is discord.DMChannel
        is_owner = await self.bot.is_owner(context.author)
        allowed = is_owner or is_dm
        if not allowed: return

        def is_me(m):
            return m.author == self.bot.user
        progress_msg = await context.send('Deleting...')
        
        msgs_to_delete = []
        deleted = 0
        async with context.typing():
            async for m in context.history(limit=None):
                if is_me(m) and m.id != progress_msg.id and content in m.content:
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
