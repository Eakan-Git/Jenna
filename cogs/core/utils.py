import aiohttp

async def download(url, as_str=False):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.text() if as_str else resp.read()