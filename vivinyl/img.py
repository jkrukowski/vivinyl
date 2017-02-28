import os
import pickle
from collections import Counter
from PIL import Image


def image_stat(file_name):
    with Image.open(file_name) as f:
        return f.size


def get_files(folder='./data'):
    for file in os.listdir(folder):
        if file.endswith('.jpg'):
            yield os.path.join(folder, file)


def main():
    data_points = Counter((image_stat(f) for f in get_files())).most_common()
    with open('outfile.dat', 'wb') as f:
        pickle.dump(data_points, f)


if __name__ == '__main__':
    main()
