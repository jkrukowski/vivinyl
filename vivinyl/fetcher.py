import logging
import logging.config
import aiohttp
import asyncio
from downloader import ImageDownloader
from parser import DataParser
from logger import DataLogger

headers = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Vivinyl/0.1',
}

params = {
    'token': 'QHojscpPtJfolpwGwXsmKteiACJQmjvhoAgHiujc'
}

logging.config.fileConfig('./vivinyl/logging.conf')
logger = logging.getLogger('vivinyl')

class DataFetcher(object):
    def __init__(self, ids, data_parser, downloader, datalogger):
        self.ids = ids
        self.data_parser = data_parser
        self.downloader = downloader
        self.datalogger = datalogger

    async def fetch(self, session, url, num):
        async with session.get(url, headers=headers, params=params) as response:
            limit = response.headers.get('X-Discogs-Ratelimit')
            used = response.headers.get('X-Discogs-Ratelimit-Used')
            remaining = response.headers.get('X-Discogs-Ratelimit-Remaining')
            logger.info('{0}: Limit {1} Used {2} Remaining {3}'.format(num, limit, used, remaining))
            if response.status != 200:
                logger.info('{0}: Response status {1} for release'.format(num, response.status))
                return None
            return await response.json()

    async def process(self):
        async with aiohttp.ClientSession() as session:
            for num in self.ids:
                logger.info('{0}: Started...'.format(num))
                url = self.build_url(num)
                data = await self.fetch(session=session, url=url, num=num)
                if not data:
                    continue
                self.datalogger.save(data=data.get('images'), num=num)
                image_url = self.data_parser.get_image_uri(data=data, num=num)
                if not image_url:
                    logger.info('{0}: No image url'.format(num))
                    continue
                await self.downloader.download(url=image_url, num=num)

    def build_url(self, num):
        return 'https://api.discogs.com/releases/{0}'.format(num)


async def main(ids):
    downloader = ImageDownloader(folder_path='./data')
    datalogger = DataLogger(folder_path='./logs')
    fetcher = DataFetcher(ids=ids,
                          data_parser=DataParser(),
                          downloader=downloader,
                          datalogger=datalogger)
    await fetcher.process()


if __name__ == '__main__':
    logger.info('started')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(range(100)))
