import logging
import logging.config
import os
from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES

logging.config.fileConfig('./vivinyl/logging.conf')
logger = logging.getLogger('vivinyl')


def get_files(folder='./data'):
    for file in os.listdir(folder):
        if file.endswith('.jpg'):
            yield os.path.join(folder, file)


def add_files():
    es = Elasticsearch()
    ses = SignatureES(es)
    n = 0
    for file in get_files():
        logger.info('{0} Adding file {1}'.format(n, file))
        ses.add_image(file)
        n += 1


def main():
    add_files()


if __name__ == '__main__':
    logger.info('started')
    main()
