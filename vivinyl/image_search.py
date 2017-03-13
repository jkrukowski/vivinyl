import os
from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES


def get_files(folder='./data'):
    for file in os.listdir(folder):
        if file.endswith('.jpg'):
            yield os.path.join(folder, file)


def main():
    es = Elasticsearch()
    ses = SignatureES(es)
    for path in get_files():
        ses.add_image(path)


if __name__ == '__main__':
    main()
