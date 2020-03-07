import discord
import convert
import colors

from discord.ext import commands
from datetime import datetime

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pfp'])
    @commands.guild_only()
    async def avatar(self, context, *member):
        if member:
            member = ' '.join(member)
            member = await convert.to_user(context, member)
        else:
            member = context.author
        if not member: return

        embed = colors.embed()
        embed.title = str(member)
        embed.set_image(url=str(member.avatar_url).replace('webp', 'png'))
        embed.timestamp = datetime.now().astimezone()
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Images(bot))