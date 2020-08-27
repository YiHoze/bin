import os 
import sys
import argparse
import glob
import re
import shutil
from datetime import datetime
import exifread

class FileUtility(object):

    def __init__(self):

        now = datetime.now()
        self.suffix = now.strftime('_%Y-%m-%d')


    def parse_args(self):

        parser = argparse.ArgumentParser(
            description = 'Append a date or suffix to filenames'
        )
        parser.add_argument(
            'files',
            nargs = '+',
            help = 'Specify one or more files'
        )
        parser.add_argument(
            '-s',
            dest = 'suffix',
            help = 'Specify a date or suffix. The dafult is the current date.'
        )
        parser.add_argument(
            '-r',
            dest = 'remove',
            action = 'store_true',
            default = False,
            help = 'Remove a suffix from filenames.'
        )
        parser.add_argument(
            '-n',
            dest = 'nospace',
            action = 'store_true',
            default = False,
            help = 'Remove spaces from filenames.'
        )
        parser.add_argument(
            '-u',
            dest = 'uppercase',
            action = 'store_true',
            default = False,
            help = 'Rename files to uppercase.'
        )
        parser.add_argument(
            '-l',
            dest = 'lowercase',
            action = 'store_true',
            default = False,
            help = 'Rename files to lowercase.'
        )
        parser.add_argument(
            '-c',
            dest = 'copy',
            action = 'store_true',
            default = False,
            help = 'Copy fiels from multiple folders to one folder.'
        )
        parser.add_argument(
            '-t',
            dest = 'target_folder',
            help = 'Specify a directory into which to copy files.'
        )
        parser.add_argument(
            '-d',
            dest = 'original_date',
            action = 'store_true',
            default = False,
            help = "Change images' filenames to their creation dates, extracting from the metadata."
        )
        self.args = parser.parse_args()
        if self.args.suffix is not None:
            self.suffix = self.args.suffix


    def rename_uppercase(self):

        for fnpattern in self.args.files:
            for afile in glob.glob(fnpattern):
                filename = os.path.splitext(afile)
                newname = filename[0].upper() +  filename[1].upper()            
                os.rename(afile, newname)


    def rename_lowercase(self):

        for fnpattern in self.args.files:
            for afile in glob.glob(fnpattern):
                filename = os.path.splitext(afile)
                newname = filename[0].lower() +  filename[1].lower()            
                os.rename(afile, newname)


    def append_suffix(self):    

        for fnpattern in self.args.files:
            for afile in glob.glob(fnpattern):
                filename = os.path.splitext(afile)
                newname = filename[0] + self.suffix + filename[1]
                os.rename(afile, newname)
              

    def remove_suffix(self):

        for fnpattern in self.args.files:
            for afile in glob.glob(fnpattern):
                newname = re.sub(self.suffix, '', afile)
                os.rename(afile, newname)


    def remove_spaces(self):

        for fnpattern in self.args.files:
            for afile in glob.glob(fnpattern):
                if afile.count(' ') > 0:
                    newname = re.sub(' ', '', afile)
                    if os.path.exists(newname):
                        os.remove(newname)
                    os.rename(afile, newname)                


    def get_subdirs(self, fnpattern):

        curdir = os.path.dirname(fnpattern)
        if curdir == '':
            curdir = '.'
        return([x[0] for x in os.walk(curdir)])

    def rename_to_original_date(self):    

        for fnpattern in self.args.files:
            for afile in glob.glob(fnpattern):
                try:
                    with open(afile, 'rb') as f:
                        tags = exifread.process_file(f, stop_tag='EXIF DateTimeOriginal')
                        date = str(tags['EXIF DateTimeOriginal'])[:10]
                        date = date.replace(':', '-')
                except:
                    date = datetime.fromtimestamp(os.path.getmtime(afile))
                    date = date.strftime('%Y-%m-%d')
                
                newname = self.date_increment(date, os.path.splitext(afile)[1])
                os.rename(afile, newname)

    def date_increment(self, filename, ext):

        cnt = 0
        basename = filename + ext
        while os.path.exists(basename):
            cnt += 1
            basename = filename + "_" + str(cnt) + ext
        return basename

    def copy_into(self):

        if not os.path.exists(self.args.target_folder):
            answer = input('The %s folder is not found. If you want to create it, Enter Y. ' % (self.args.target_folder))
            if (answer.lower() == 'y'):
                os.mkdir(self.args.target_folder)
            else:
                return False
        for fnpattern in self.args.files:
            basename = os.path.basename(fnpattern)
            subdirs = self.get_subdirs(fnpattern)
            for subdir in subdirs:   
                subfile = os.path.join(subdir, basename)
                for afile in glob.glob(subfile):
                    shutil.copy(afile, self.args.target_folder)


if __name__ == '__main__':
    fu = FileUtility()
    fu.parse_args()
    if fu.args.nospace:
        fu.remove_spaces()
    elif fu.args.uppercase:
        fu.rename_uppercase()
    elif fu.args.lowercase:
        fu.rename_lowercase()
    elif fu.args.remove:
        fu.remove_suffix()
    elif fu.args.copy:
        fu.copy_into()
    elif fu.args.original_date:
        fu.rename_to_original_date()
    else:
        fu.append_suffix() 