import aiohttp
import mimetypes

def url_is_image(url):
    mimetype, encoding = mimetypes.guess_type(url)
    return 'image' in str(mimetype)

async def download(url, as_str=False):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.text() if as_str else await resp.read()