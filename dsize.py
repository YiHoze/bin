import os
import math
import argparse

parser = argparse.ArgumentParser(
    description = 'Get the sum of all file sizes, including subdirectories.'
)
args = parser.parse_args()

def get_size(start_path='.'):
    total_size = 0
    # seen = {}
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                stat = os.stat(fp)
            except OSError:
                continue
            # try:
            #     seen[stat.st_ino]
            # except KeyError:
            #     seen[stat.st_ino] = True
            # else:
            #     continue
            total_size += stat.st_size
    print(readable(total_size))

def readable(size):

    units = ["B", "KB", "MB", "GB", "TB"]
    format = "%d %s"
    radix = 1024

    for u in units[:-1]:
        if size < radix : return format % (math.ceil(size), u)
        size /= radix

    return format % (math.ceil(size),  units[-1])

get_size()