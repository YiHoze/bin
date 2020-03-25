# Install pywin32 to use win32com 
import os
import sys
import glob
import argparse
import winshell
from win32com.client import Dispatch 

class ShortcutToFavorite(object):
    def __init__(self, files=None, destination=r'C:\Users\yihoze\Favorites\링크', show=False):
        self.files = files
        self.destination = destination
        self.show_bool = show

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Create a shortcut into a favorite or specific directory.'
        )
        parser.add_argument(
            'files',
            nargs = '*',
            help = 'Specify a file or more to create their shortcuts.'
        )
        parser.add_argument(
            '-d',
            dest = 'destination',
            default = r'C:\Users\yihoze\Favorites\링크',
            help = 'Specify a directory where to create shortcuts for specified files.'
        )  
        parser.add_argument(
            '-s',
            dest = 'show',
            action = 'store_true',
            default = False,
            help = 'Show the destination directory.'
        )      
        args = parser.parse_args()
        self.files = args.files        
        self.destination = args.destination
        self.show_bool = args.show

    def create_shortcut(self):
        shell = Dispatch('WScript.Shell')
        for fnpattern in self.files:
            for afile in glob.glob(fnpattern):
                target_path = os.path.abspath(afile)
                filename = os.path.basename(afile) + '.lnk'
                shortcut_path = os.path.join(self.destination, filename)
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = target_path
                shortcut.save()

if __name__ == '__main__':
    shortcut = ShortcutToFavorite()
    shortcut.parse_args()
    if shortcut.show_bool:
        print(shortcut.destination)
    else:
        shortcut.create_shortcut()