import os
import sys
import glob
import argparse
import re

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from open import FileOpener

class TeXCompiler(object):
    def __init__(self, tex=None,
        batch=False, shell=False, twice=False, fully=False, keep_aux=False, clear=False,
        view=False, no_compile=False, bibtex=False, luatex=False,
        index=False, language='korean', komkindex=False, index_style='kotex.ist',
        bookmark_index=False, bookmark_python=False, 
        final=False, draft=False):
        self.tex = tex
        self.batch = batch
        self.shell = shell
        self.twice = twice
        self.fully = fully
        self.keep_aux = keep_aux
        self.clear = clear
        self.view = view
        self.no_compile = no_compile
        self.bibtex = bibtex
        self.luatex = luatex
        self.index = index
        self.lang = language
        self.komkindex = komkindex
        self.index_style = index_style
        self.bm_index = bookmark_index
        self.bm_python = bookmark_python
        self.final = final
        self.draft = draft

    def get_ready(self):        
        if self.luatex:
            self.compiler = 'lualatex.exe'
        else:
            self.compiler = 'xelatex.exe'

        # Compile mode
        if self.batch or self.fully:
            self.compile_mode = '-interaction=batchmode '
        else:
            self.compile_mode = '-synctex=1 '
        if self.shell:
            self.compile_mode +=  '-shell-escape'

        # language by which to sort index
        index_modules = {
            'eng': 'lang/english/utf8-lang ',
            'fre': 'lang/french/utf8-lang ',
            'ger': 'lang/german/din5007-utf8-lang ',
            'ita': 'lang/italian/utf8-lang ',
            'kor': 'lang/korean/utf8-lang ',
            'rus': 'lang/russian/utf8-lang ',
            'spa': 'lang/spanish/modern-utf8-lang '
        }
        try:
            self.xindy = index_modules[self.lang[:3].lower()]
        except:
            self.xindy = index_modules['kor']

        if self.tex is not None:            
            filename = os.path.basename(self.tex)
            basename = os.path.splitext(filename)[0]
            self.tex = basename + '.tex'
            self.aux = basename + '.aux'
            self.idx = basename + '.idx'
            self.ind = basename + '.ind'
            self.pdf = basename + '.pdf'
            if not os.path.exists(self.tex):                
                print('%s is not found.' %(self.tex))
                self.tex = None

    def parse_args(self, argv=None):
        parser = argparse.ArgumentParser(
            description = 'Convert a TeX file to PDF using XeLaTeX or LuaLaTeX.'
        )
        parser.add_argument(
            'tex',
            type = str,
            nargs = '?',
            help = 'Specify a TeX file.'
        )
        parser.add_argument(
            '-b',
            dest = 'batch',
            action = 'store_true',
            default = False,
            help = 'Do not halt even with syntax errors. (batch-mode)'
        )
        parser.add_argument(
            '-s',
            dest = 'shell',
            action = 'store_true',
            default = False,
            help = 'Allow an external program to run during a XeLaTeX run. (shell-escape)'
        )
        parser.add_argument(
            '-w',
            dest = 'twice',
            action = 'store_true',
            default = False,
            help = 'Compile twice.'
        )
        parser.add_argument(
            '-f',
            dest = 'fully',
            action = 'store_true',
            default = False,
            help = 'Compile fully.'
        )
        parser.add_argument(
            '-v',
            dest = 'view',
            action = 'store_true',
            default = False,
            help = 'Open the resulting PDF file to view.'
        )
        parser.add_argument(
            '-n',
            dest = 'no_compile',
            action = 'store_true',
            default = False,
            help = 'Pass over compilation but do other processes such as index sorting.'
        )
        parser.add_argument(
            '-i',
            dest = 'index',
            action = 'store_true',
            default = False,
            help = 'Sort index using TeXindy.'
        )
        parser.add_argument(
            '-l',
            dest = 'luatex',
            action = 'store_true',
            default = False,
            help = 'Use LuaLaTeX instead of XeLaTeX.'
        )
        parser.add_argument(
            '-lang',
            dest = 'language',
            help = 'Specify a language to sort index entries. For example, \"german\" or \"ger\" for German. The default is \"korean\".'
        )
        parser.add_argument(
            '-k',
            dest = 'komkindex',
            action = 'store_true',
            default = False,
            help = 'Use komkindex instead of TeXindy.'
        )
        parser.add_argument(
            '-ist',
            dest = 'index_style',
            help = 'Specify an index style for komkindex. The dafault is kotex.ist.'
        )
        parser.add_argument(
            '-a',
            dest = 'keep_aux',
            action = 'store_true',
            default = False,
            help = 'After a full compilation (-f), auxiliary files are deleted. Use this option to keep them.'    
        )
        parser.add_argument(
            '-m',
            dest = 'bookmark_index',
            action = 'store_true',
            default = False,
            help = 'Bookmark index entries. This option is available only with -f or -i options. This feature does not support komkindex.'
        )
        parser.add_argument(
            '-p',
            dest = 'bookmark_python',
            action = 'store_true',
            default = False,
            help = 'Bookmark index entries which are Python functions extracted from docstrings. This option is available only with -f or -i options.'
        )
        parser.add_argument(
            '-c',
            dest = 'clear',
            action = 'store_true',
            default = False,
            help = 'Remove auxiliary files after compilation.'
        )
        parser.add_argument(
            '-bib',
            dest = 'bibtex',
            action = 'store_true',
            default = False,
            help = 'Run bibtex.'
        )
        parser.add_argument(
            '-fin',
            dest = 'final',
            action = 'store_true',
            default = False,
            help = 'Find \\FinalizerOff to replace it with \\FinalizerOn in the tex file.'    
        )
        parser.add_argument(
            '-d',
            dest = 'draft',
            action = 'store_true',
            default = False,
            help = 'Find \\FinalizerON to replace it with \\FinalizerOff in the tex file.'    
        )
        args = parser.parse_args(argv)
        if args.tex is not None:
            self.tex = args.tex
        self.batch = args.batch
        self.shell = args.shell
        self.twice = args.twice
        self.fully = args.fully
        self.keep_aux = args.keep_aux
        self.clear = args.clear
        self.view = args.view
        self.no_compile = args.no_compile
        self.bibtex = args.bibtex
        self.luatex = args.luatex
        self.index = args.index
        if args.language is not None:            
            self.lang = args.language
        self.komkindex = args.komkindex
        if args.index_style is not None:
            self.index_style = args.index_style
        self.bm_index = args.bookmark_index
        self.bm_python = args.bookmark_python
        self.final = args.final
        self.draft = args.draft

    def compile_once(self, cmd_tex):
        os.system(cmd_tex)
        if self.bibtex:
            self.run_bibtex()
        if self.index:
            self.sort_index()

    def compile_twice(self, cmd_tex):
        os.system(cmd_tex)
        if self.bibtex:
            self.run_bibtex()
        if self.index:
            self.sort_index()
        os.system(cmd_tex) 

    def compile_fully(self, cmd_tex):
        os.system(cmd_tex)
        if self.bibtex:
            self.run_bibtex()
        os.system(cmd_tex)
        self.sort_index()       
        if os.path.exists(self.ind):
            os.system(cmd_tex)
        os.system(cmd_tex)
        if not self.keep_aux:
            self.clear_aux()

    def run_bibtex(self):    
        os.system('bibtex %s' %(self.aux))

    def sort_index(self):
        if not os.path.exists(self.idx):
            print('%s is not found' % (self.idx))
            return
        if self.komkindex:
            cmd = 'komkindex.exe -s %s %s' %(self.index_style, self.idx)
        else:
            cmd = 'texindy.exe --module %s %s' %(self.xindy, self.idx) 
        os.system(cmd)    
        if self.bm_index or self.bm_python:
            self.bookmark_index()

    def bookmark_index(self):
        tmp = 't@mp.ind'
        if os.path.exists(tmp):
            os.remove(tmp)
        with open(tmp, mode = 'w', encoding = 'utf-8') as new_file, open(self.ind, mode = 'r', encoding = 'utf-8') as old_file:
            if self.bm_python:
                for line in old_file.readlines():
                    new_file.write(self.bookmark_item(line, r'\\item (.+?)\(\)'))
            else:
                for line in old_file.readlines():
                    new_file.write(self.bookmark_item(line, r'\\item (.+?),'))         
        os.remove(self.ind)
        os.rename(tmp, self.ind)

    def bookmark_item(self, line, pattern):
        entry = re.search(pattern, line)
        if entry: 
            page = re.findall(r'\\hyperpage\{(\d+)\}', line)
            append = ''
            for i in range(len(page)):
                append +=  '\t\\bookmark[level=2, page=%s]{%s}\n' %(page[i], entry.group(1))                    
            line +=  append
        return(line)  

    def clear_aux(self):
        extensions = ("aux", "bbl", "blg", "idx", "ilg", "ind", "loe", "lof", "log", "lop", "loq", "lot", "minted*", "mw", "nav", "out", "synctex*", "snm", "toc*", "upa", "upb", "pyg.lst", "pyg.sty", "vrb")
        for ext in extensions:
            fnpattern = '*.' + ext
            for afile in glob.glob(fnpattern):
                os.remove(afile)

    def finalizer_on(self):
        with open(self.tex, mode = 'r', encoding = 'utf-8') as f:
            content = f.read()
        content = re.sub("\\\\FinalizerOff", "\\\\FinalizerOn", content)
        with open(self.tex, mode = 'w', encoding = 'utf-8') as f:
            f.write(content)

    def finalizer_off(self):
        with open(self.tex, mode = 'r', encoding = 'utf-8') as f:
            content = f.read()
        content = re.sub("\\\\FinalizerOn", "\\\\FinalizerOff", content)
        with open(self.tex, mode = 'w', encoding = 'utf-8') as f:
            f.write(content)

    def compile(self):
        self.get_ready()
        if self.tex:
            if self.final:
                self.finalizer_on()
            if self.draft:
                self.finalizer_off()

        if self.no_compile:
            if self.tex:
                if self.index or self.komkindex:
                    self.sort_index()
                if self.bibtex:
                    self.run_bibtex()            
        else:
            if self.tex:
                cmd_tex = '%s %s %s' %(self.compiler, self.compile_mode, self.tex)
                if self.fully:
                    self.compile_fully(cmd_tex)
                elif self.twice:
                    self.compile_twice(cmd_tex)
                else:
                    self.compile_once(cmd_tex)            

        if self.clear:
            self.clear_aux()  

        if self.view:
            if os.path.exists(self.pdf):                 
                opener = FileOpener()
                # opener.open([self.pdf])
                opener.OpenPDF(self.pdf)
    
if __name__ == "__main__":
    texer = TeXCompiler()
    texer.parse_args()
    texer.compile()