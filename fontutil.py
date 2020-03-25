import os, sys, re, argparse, subprocess

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from ltx import LatexCompiler
from open import FileOpener

class FontUtility(object):
    def __init__(self, font=None, list='fonts_list.txt'):
        self.example = os.path.join(dirCalled, 'fontglyph.txt')
        self.font = font
        self.fonts_list = list

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'View the list of installed fonts, or see what glyphs a font contains using an example text. This script requires TeX Live.'
        )
        parser.add_argument(
            'font',
            nargs = '?',
            help = "Specify a font's filename (foo.ttf)."
        )
        parser.add_argument(
            '-l',
            dest = 'fonts_list',    
            help = 'Specify a filename for the list of fonts (default: fonts_list.txt).'
        )
        parser.add_argument(
            '-e',
            dest = 'example',
            help = 'Specify a file as example text (default: fontglyph.txt).'
        )
        parser.add_argument(
            '-o',
            dest = 'output',  
            help = 'Specify a file name for the output of glyphs (default: font filename). The file name must have no space.'
        )
        args = parser.parse_args()
        self.font = args.font
        if args.fonts_list is not None:
            self.fonts_list = args.fonts_list
        if args.example is not None:
            self.example = args.example
        self.output = args.output

    def show_glyphs(self):
        if not os.path.exists(self.example):
            print('%s is not found.' %(self.example))
            sys.exit()
        else:
            with open(self.example, mode='r', encoding='utf-8') as f:
                text = f.readlines()
                text = ''.join(map(str, text))
        if self.output is None:
            self.output = self.font
        filename = os.path.splitext(self.output)[0] 
        filename = re.sub(' ', '', filename)    
        tex = filename + '.tex'
        if os.path.exists(tex):
            answer = input('%s already exists. Are you sure to remake it? [y/N] ' %(tex))
            if answer.lower() == 'y':
                os.remove(tex)
            else:
                return False
        content = """
        \\documentclass{minimal} 
        \\usepackage{fontspec} 
        \\setlength\\parskip{1.25\\baselineskip} 
        \\setlength\\parindent{0pt}
        \\setmainfont{%s}
        \\begin{document}
        %s
        \\end{document}""" %(self.font, text)
        with open(tex, mode='w', encoding='utf-8') as f:
            f.write(content)
        texer = LatexCompiler(tex)
        texer.parse_args(['-b', '-v'])        
        texer.compile()

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
        fu.show_glyphs()