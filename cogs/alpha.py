import discord

from discord.ext import commands

class Alpha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def repeat(self, context, msg_id:int, limit:int=100):
        await context.trigger_typing()
        history = await context.history(limit=limit).flatten()
        msg = discord.utils.get(history, id=msg_id)
        if msg:
            embed = msg.embeds[0] if msg.embeds else None
            await context.send(msg.content, embed=embed)
        else:
            await context.send('History limit 2 smol!')
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def c(self, context, channel:discord.TextChannel=None, limit:int=200):
        if not channel:
            channel = context.channel

        self.spams = await channel.history(limit=limit).flatten()
        total_len = sum(len(m.content) for m in self.spams)
        print('Total Length:', total_len)
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def p(self, context):
        msg_count = len(self.spams)
        for i, m in enumerate(self.spams[::-1]):
            if m.content:
                await context.send(m.content)
            i += 1
            if i % 5 == 0:
                progress = i / msg_count * 100
                print(f'Progress: {progress:.2f}% ({i}/{msg_count})')
    
    @commands.command(aliases=['rl'], hidden=True)
    @commands.is_owner()
    async def reload(self, context, cog_name):
        cog = 'cogs.' + cog_name
        self.bot.unload_extension(cog)
        self.bot.load_extension(cog)
        await context.send(f'Cog `{cog_name}` reloaded!')
    
    @commands.command(hidden=True)
    async def e(self, context, emoji):
        await context.send(f':{emoji}:')

def setup(bot):
    bot.add_cog(Alpha(bot))