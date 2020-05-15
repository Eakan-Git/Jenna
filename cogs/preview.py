from discord.ext import commands

import discord
import re
import colors

JUMP_URL_PATTERN = '(https://discord\.com/channels/\d+/\d+/\d+)'

class Preview(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_converter = commands.MessageConverter()
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.author == self.bot.user: return

        urls = re.findall(JUMP_URL_PATTERN, message.content)
        context = await self.bot.get_context(message)
        for jump_url in urls:
            quoted_message = await self.message_converter.convert(context, jump_url)
            author = quoted_message.author

            embed = colors.embed(description=quoted_message.content) \
                    .set_author(name=author.display_name, icon_url=author.avatar_url)
            
            embed.timestamp = quoted_message.created_at
            for a in quoted_message.attachments:
                embed.set_image(url=a.url)
            
            await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Preview(bot))