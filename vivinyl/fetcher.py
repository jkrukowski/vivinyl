import logging
import logging.config
import argparse
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
    def __init__(self, data_parser, downloader, datalogger):
        self.data_parser = data_parser
        self.downloader = downloader
        self.datalogger = datalogger
        self.remaining = 240
        self.min_remaining = 60

    def get_header_values(self, response):
        limit = response.headers.get('X-Discogs-Ratelimit')
        used = response.headers.get('X-Discogs-Ratelimit-Used')
        remaining = response.headers.get('X-Discogs-Ratelimit-Remaining', self.remaining)
        return limit, used, int(remaining)

    async def fetch(self, url, num):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                limit, used, self.remaining = self.get_header_values(response)
                logger.info('{0}: Limit {1} Used {2} Remaining {3}'.format(num, limit, used, self.remaining))
                if response.status != 200:
                    logger.info('{0}: Response status {1} for release'.format(num, response.status))
                    return None
                return await response.json()

    async def process(self, num):
        logger.info('{0}: Started...'.format(num))
        url = self.build_url(num)
        if self.remaining <= self.min_remaining:
            logger.info('{0}: Remaining {1} sleeping'.format(num, self.remaining))
            await asyncio.sleep(1)
        data = await self.fetch(url=url, num=num)
        if not data:
            return
        self.datalogger.save(data=data.get('images'), num=num)
        image_url = self.data_parser.get_image_uri(data=data, num=num)
        if not image_url:
            logger.info('{0}: No image url'.format(num))
            return
        await self.downloader.download(url=image_url, num=num)

    def build_url(self, num):
        return 'https://api.discogs.com/releases/{0}'.format(num)


async def main(start, stop, workers, loop):
    downloader = ImageDownloader(folder_path='./data')
    datalogger = DataLogger(folder_path='./logs')
    fetcher = DataFetcher(data_parser=DataParser(),
                          downloader=downloader,
                          datalogger=datalogger)
    ids = range(start, stop, workers)
    for release_id in ids:
        tasks = [fetcher.process(release_id + i) for i in range(workers)]
        await asyncio.wait(tasks, loop=loop)


if __name__ == '__main__':
    logger.info('started')
    parser = argparse.ArgumentParser()
    parser.add_argument('start', type=int)
    parser.add_argument('stop', type=int)
    parser.add_argument('workers', type=int, default=3)
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(start=args.start, stop=args.stop, workers=args.workers, loop=loop))
    loop.close()
