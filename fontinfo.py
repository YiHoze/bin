import os, sys, re, argparse, subprocess

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from ltx import LatexCompiler
from open import FileOpener
from mytex import LatexTemplate

class FontUtility(object):
    def __init__(self, font=None, list='fonts_list.txt'):
        self.font = font
        self.fonts_list = list

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'View the list of installed fonts, or see what glyphs a font contains using an example text. This script requires TeX Live.'
        )
        parser.add_argument(
            'font',
            nargs = '?',
            help = 'Specify a font name or filename.'
        )
        parser.add_argument(
            '-l',
            dest = 'fonts_list',    
            default = 'fonts_list.txt',
            help = 'Specify a filename for the list of fonts (default: fonts_list.txt).'
        )
        args = parser.parse_args()
        self.font = args.font
        self.fonts_list = args.fonts_list

    def multilingual(self):
        filename = os.path.splitext(self.font)[0]
        filename = ''.join(filename.split())
        mytex = LatexTemplate(template='multilingual', substitutes=[self.font], output=filename)
        if mytex.ini_bool:
            mytex.make()

    def enumerate_fonts(self):
        if os.path.exists(self.fonts_list):
            os.remove(self.fonts_list)
        cmd = 'fc-list : -f "%%{file} > %%{family}  \\n" > %s' %(self.fonts_list) # %%{family} %%{fullname} %%{style}
        os.system(cmd)
        with open(self.fonts_list, mode='r', encoding='utf-8') as f:
            content = f.readlines()        
        content = set(content)
        content = ''.join(sorted(content, key=str.lower))    
        with open(self.fonts_list, mode='w', encoding='utf-8') as f:
            for line in content:
                f.write(line)
        opener = FileOpener()
        opener.OpenTxt(self.fonts_list)

if __name__ == '__main__':
    fu = FontUtility()
    fu.parse_args()
    if fu.font is None:
        fu.enumerate_fonts()
    else:
        fu.multilingual()