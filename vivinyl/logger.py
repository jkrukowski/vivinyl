import os
import json


class DataLogger(object):
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def save(self, data, num):
        fname = self.build_file_name(num)
        with open(fname, 'w') as f:
            json.dump(data, f)

    def build_file_name(self, num):
        name = 'release_{0}.json'.format(num)
        return os.path.join(self.folder_path, name)
