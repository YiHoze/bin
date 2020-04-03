import os
import sys 
import re
import argparse
import subprocess

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from open import FileOpener
from mytex import LatexTemplate

class FontInfo(object):
    def __init__(self, font=None, info=False, list='fonts_list.txt'):
        self.font = font
        self.info_bool = info
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
            '-i',
            dest = 'info',
            action = 'store_true',
            default = False,
            help = 'Show the font name.'
        )
        parser.add_argument(
            '-l',
            dest = 'fonts_list',    
            default = 'fonts_list.txt',
            help = 'Specify a filename for the list of fonts (default: fonts_list.txt).'
        )
        args = parser.parse_args()
        self.font = args.font
        self.info_bool = args.info
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
        cmd = 'fc-list -f "%%{file} : %%{family} \\n" > %s' %(self.fonts_list) # %%{family} %%{fullname} %%{style}
        os.system(cmd)
        with open(self.fonts_list, mode='r', encoding='utf-8') as f:
            content = f.readlines()                    
        content = set(content)
        content = ''.join(sorted(content, key=str.lower))    
        with open(self.fonts_list, mode='w', encoding='utf-8') as f:
            f.write(content)
        opener = FileOpener()
        opener.OpenTxt(self.fonts_list)

    def find_path(self, fonts):
        p = '.*' + self.font
        font = re.search(p, fonts)
        if font is not None:
            return(font.group())
        else:
            fonts = fonts.split('\n')
            print('')
            i = 1
            while i < len(fonts):        
                print('{}: {}'.format(i, fonts[i-1]))
                i = i + 1 
            index = input('\nSelect a font by entering its number to see the details: ')
            try:
                index = int(index)
            except:
                return False
            index = index - 1
            if index < len(fonts):
                return(fonts[index])
            else:
                return False

    def get_info(self):  
        # ext = os.path.splitext(self.font)[1]
        # if ext == '':
        cmd = 'fc-list -f "%{{file}}\n" "{}"'.format(self.font)
        fonts = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        fonts = fonts.decode(encoding='utf-8')        
        if fonts == '':
            print('No relevant fonts are found.')
            return
        else:
            font = self.find_path(fonts)
            if font is not False:
                cmd = 'otfinfo -i {}'.format(font)
                print('')
                os.system(cmd)
                print('')

if __name__ == '__main__':
    fi = FontInfo()
    fi.parse_args()
    if fi.font is None:
        fi.enumerate_fonts()
    else:
        if fi.info_bool:
            fi.get_info()
        else:
            fi.multilingual()