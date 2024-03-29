import logging
import aiohttp
import os

logger = logging.getLogger('vivinyl')
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br'
}


class ImageDownloader(object):
    def __init__(self, folder_path):
        self.folder_path = folder_path

    async def download(self, url, num):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.info('{0}: Response status {1} for image of release'.format(num, response.status))
                    return None
                data = await response.read()
                self.save(data=data, num=num)
                logger.info('{0}: Done'.format(num))

    def save(self, data, num):
        fname = self.build_file_name(num)
        with open(fname, 'wb') as f:
            f.write(data)

    def build_file_name(self, num):
        name = 'img_{0}.jpg'.format(num)
        return os.path.join(self.folder_path, name)
