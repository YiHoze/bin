import os
import sys
import argparse
import requests
from urllib.parse import urlparse
from pathlib import Path
import shutil

class WebImage(object):

    def __init__(self, url=None, output=None):
        self.url = url
        self.output = output
        
    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Download images from the Web.'
        )
        parser.add_argument(
            'url',
            nargs = '+',
            help = 'Specify an image URL.'
        )
        parser.add_argument(
            '-o',
            dest = 'output',
            help = 'Specify a file name for output.'
        )
        args = parser.parse_args()
        self.url = args.url
        self.output = args.output

    def name_file(self, url):
        org_name = Path(urlparse(url).path).name
        if self.output is None:            
            filename = org_name
        else:
            name = os.path.splitext(self.output)[0]            
            ext = os.path.splitext(org_name)[1]
            filename = '{}{}'.format(name, ext)
        counter = 0
        while os.path.exists(filename):
            counter += 1
            filename = '{}({}){}'.format(name, counter, ext)
        return filename

    def download_image(self):
        for url in self.url:
            filename = self.name_file(url)  
            resp = requests.get(url, stream=True)
            local_file = open(filename, 'wb')
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, local_file)

if __name__ == '__main__':
    WI = WebImage()
    WI.parse_args()
    WI.download_image()