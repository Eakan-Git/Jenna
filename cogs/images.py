import discord
import colors

from discord.ext import commands
from datetime import datetime
from .core import converter as conv

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ava', 'pfp'])
    @commands.guild_only()
    async def avatar(self, context, *, member:conv.Member=None):
        member = member or context.author
        embed = colors.embed()
        embed.title = str(member)
        embed.set_image(url=str(member.avatar_url).replace('webp', 'png'))
        embed.timestamp = datetime.now().astimezone()
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Images(bot))