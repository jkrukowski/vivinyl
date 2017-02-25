import aiohttp
import asyncio
from .downloader import ImageDownloader
from .parser import DataParser

headers = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Vivinyl/0.1',
}

params = {
    'token': 'QHojscpPtJfolpwGwXsmKteiACJQmjvhoAgHiujc'
}

class DataFetcher(object):
    def __init__(self, ids, data_parser, downloader):
        self.ids = ids
        self.data_parser = data_parser
        self.downloader = downloader

    async def fetch(self, session, url):
        async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                return None
            return await response.json()

    async def process(self):
        async with aiohttp.ClientSession() as session:
            for num in self.ids:
                url = self.build_url(num)
                data = await self.fetch(session=session, url=url)
                if not data:
                    continue
                image_url = self.data_parser.get_image_uri(data)
                print('url: {0}'.format(data['images']))
                await self.downloader.download(url=image_url, num=num)

    def build_url(self, num):
        return 'https://api.discogs.com/releases/{0}'.format(num)


async def main(ids):
    downloader = ImageDownloader(folder_path='./data')
    fetcher = DataFetcher(ids=ids, data_parser=DataParser(), downloader=downloader)
    await fetcher.process()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(range(100)))
