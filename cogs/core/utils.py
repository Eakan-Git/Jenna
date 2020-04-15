import aiohttp
import mimetypes

def url_is_image(url):
    mimetype, encoding = mimetypes.guess_type(url)
    return 'image' in str(mimetype)

READ = 'read'
async def download(url, method='text'):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                if method:
                    return await getattr(resp, method)()
                return resp