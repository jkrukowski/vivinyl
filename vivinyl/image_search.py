import argparse
import os
from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES


def get_files(folder='./data'):
    for file in os.listdir(folder):
        if file.endswith('.jpg'):
            yield os.path.join(folder, file)


def add_files():
    es = Elasticsearch()
    ses = SignatureES(es)
    for path in get_files():
        ses.add_image(path)


def match_file(file_path):
    es = Elasticsearch()
    ses = SignatureES(es)
    result = ses.search_image(file_path, all_orientations=True)
    print(result)
    return result


def main(args):
    if args.a:
        add_files()
    else:
        match_file(args.match)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('a', action='store_false')
    parser.add_argument('--match', type=str, default='img_1.jpg')
    args = parser.parse_args()
    main(args)
