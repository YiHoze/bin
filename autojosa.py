import os
import argparse
import glob
import re
from itertools import product

class AutoJosa(object):
    def __init__(self, tex=None):
        self.tex = tex
        self.josas = ('은', '는', '이', '가', '을', '를', '와', '과', '로', '으로', '라', '이라')
        self.tags = (
            r'(\\ref\{.+?\})',    
            r'(\\eqref\{.+?\})',    
            r'(\\hyperref\[.+?\]\{\\.+?\}\})',
            r'(\\sphinxhref\{.+?\}\{.+?\})',
            r'(\\sphinxtitleref\{.+?\})'
        )

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Replace 조사 with 자동 조사 such as \\를.'
        )
        parser.add_argument(
            'tex',
            nargs='+',
            help='Specify TeX files.'
        )
        args = parser.parse_args()
        if args.tex is not None:
            self.tex = args.tex

    def josa_generator(self):
        for tag, josa in product(self.tags, self.josas):
            yield tag + josa, '\\1' + '\\\\' + josa

    def replace(self):
        tmp = 't@mp.tex'
        if os.path.exists(tmp):
            os.remove(tmp)
        for files in self.tex:
            for afile in glob.glob(files):
                with open(afile, mode='r', encoding='utf-8') as f:
                    content = f.read()        
                for pattern, subst in self.josa_generator():
                    content = re.sub(pattern, subst, content)
                with open(tmp, mode='w', encoding='utf-8') as f:
                    f.write(content)        
                os.remove(afile)
                os.rename(tmp, afile)      

if __name__ == '__main__':
    autojosa = AutoJosa()
    autojosa.parse_args()
    autojosa.replace()
    # for i in autojosa.josa_generator():
    #     print(i)