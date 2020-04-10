from discord.ext import commands
import aiohttp

async def to_partial_emoji(context, s):
    return await commands.PartialEmojiConverter().convert(context, s)

async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()