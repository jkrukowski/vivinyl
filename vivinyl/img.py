from PIL import Image
import os
from collections import Counter
import matplotlib.pyplot as plt


def image_stat(file_name):
    with Image.open(file_name) as f:
        return f.size


def get_files(folder='./data'):
    for file in os.listdir(folder):
        if file.endswith('.jpg'):
            yield os.path.join(folder, file)


def main():
    data_points = Counter((image_stat(f) for f in get_files()))
    print(data_points)
    for x, y in data_points.keys():
        plt.scatter(x, y, s=data_points[(x, y)])
    plt.savefig('plot.png')


if __name__ == '__main__':
    main()
