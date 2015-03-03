import os
from os.path import split, abspath

dirname, filename = split(abspath(__file__))
def get_file_path(file_name):
    for root, dirs, files in os.walk(dirname+"/../.."):
        for name in files:
            if name == file_name or name == file_name + ".txt":
                return os.path.abspath(os.path.join(root, name))
    else:
        raise Exception("File not found")