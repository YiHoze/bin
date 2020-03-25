import os
import sys
import glob
import argparse
import csv
import re
import codecs

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from open import FileOpener

class StringFinder(object):
    def __init__(self, files=None, target=None, substitute=None, backup=False, suffix=None, pattern=None, recursive=False, detex=False):
        self.files = files
        self.target = target
        self.substitute = substitute
        self.backup_bool = recursive
        self.suffix = suffix
        self.pattern = pattern
        self.recursive_bool = recursive
        self.detex_bool = detex
        self.pattern_for_detex()

    def pattern_for_detex(self):
        if self.detex_bool and self.pattern is None:
            self.pattern = os.path.join(dirCalled, 'tex.csv')

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Search a text file to find or replace some strings with others.'
        )
        parser.add_argument(
            'files',
            nargs = '+',
            help = 'Specify one or more text files.'
        )
        parser.add_argument(
            '-t',
            dest = 'target',
            default = None,
            help = 'Specify a string to find.'

        )
        parser.add_argument(
            '-s',
            dest = 'substitute',
            default = None,
            help = 'Specify a string with which to replace found strings.'

        )
        parser.add_argument(
            '-b',
            dest = 'backup',
            action = 'store_true',
            default = False,
            help = 'Make a backup copy.'
        )
        parser.add_argument(
            '-x',
            dest = 'suffix',
            default = None,
            help = 'Specify a suffix for output. This is incompatible with -b.'
        )
        parser.add_argument(
            '-p',
            dest = 'pattern',
            default = None,
            help = 'Specify a file that includes substitution patterns. (foo.csv/tsv)'
        )
        parser.add_argument(
            '-r',
            dest = 'recursive',
            action = 'store_true',
            default = False,
            help = 'Process ones in all subdirectories.'
        )
        parser.add_argument(
            '-d',
            dest = 'detex',
            action = 'store_true',
            default = False,
            help = 'Remove macros from TeX files.'
        )
        args = parser.parse_args()
        self.files = args.files
        self.target = args.target
        self.substitute = args.substitute
        self.backup_bool = args.backup
        self.suffix = args.suffix
        self.pattern = args.pattern
        self.recursive_bool = args.recursive
        self.detex_bool = args.detex
        self.pattern_for_detex()

    def check_to_remove(self, afile):
        if os.path.exists(afile):
            answer = input('%s alread exists. Are you sure to overwrite it? [y/N] ' %(afile))
            if answer.lower() == 'y':
                os.remove(afile)
                return True
            else:
                return False
        else:
            return True

    def get_subdirs(self):
        return([x[0] for x in os.walk('.')])

    def run_recursive(self, func):
        if self.recursive_bool:
            subdirs = self.get_subdirs()
            for subdir in subdirs:
                for fnpattern in self.files:
                    fnpattern = os.path.join(subdir, fnpattern)
                    for afile in glob.glob(fnpattern):                        
                        func(afile)
        else:
            for fnpattern in self.files:
                for afile in glob.glob(fnpattern):
                    func(afile)

    def find(self, afile):
        print(afile)    
        try:
            with open(afile, mode='r', encoding='utf-8') as f:        
                    for num, line in enumerate(f):                
                        if re.search(self.target, line):
                            print('%5d:\t%s' %(num, line.replace('\n', ' ')))
        except:
            print('is not encoded in UTF-8.')
            return

    def replace(self, afile):
        tmp = 't@mp.t@mp'
        try:
            with open(afile, mode='r', encoding='utf-8') as f:
                content = f.read() 
        except:
            print('%s is not encoded in UTF-8.' %(afile))
            return        
        if self.pattern is None:
            content = re.sub(self.target, self.substitute, content)
        else:
            ptrn_ext = os.path.splitext(self.pattern)[1].lower()
            with open(self.pattern, mode='r', encoding='utf-8') as ptrn:
                if ptrn_ext == '.tsv':
                    reader = csv.reader(ptrn, delimiter='\t')
                else:
                    reader = csv.reader(ptrn)
                for row in reader:            
                    content = re.sub(row[0], row[1], content)                 
        with open(tmp, mode='w', encoding='utf-8') as f:
            f.write(content)
        if self.detex_bool:            
            filename = os.path.splitext(afile)[0]
            output = filename + '_clean.txt'
            if self.check_to_remove(output) is False:
                return
            else:
                os.rename(tmp, output)
                opener = FileOpener()
                opener.OpenTxt(output)                
        else:
            if self.backup_bool:
                filename, ext = os.path.splitext(afile)
                backup = filename + '_bak' + ext
                if os.path.exists(backup):
                    os.remove(backup)
                os.rename(afile, backup)
                os.rename(tmp, afile)
            else:
                if self.suffix is None:
                    if os.path.exists(afile):
                        os.remove(afile)
                    os.rename(tmp, afile)
                else:
                    filename, ext = os.path.splitext(afile)
                    output = filename + '_' + self.suffix + ext
                    if os.path.exists(output):
                        os.remove(output)
                    os.rename(tmp, output)

    def find_replace(self):        
        if self.pattern is None:        
            if self.target is None:
                return
            elif self.substitute is None:
                self.run_recursive(self.find)
            else:
                self.run_recursive(self.replace)
        else:
            if os.path.exists(self.pattern):
                self.run_recursive(self.replace)
            else:
                print('%s is not found.' %(self.pattern))

if __name__ == '__main__':
    strfind = StringFinder()
    strfind.parse_args()
    strfind.find_replace()
