import os
import sys
import glob
import argparse
import re
import shutil

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from open import FileOpener

class LatexCompiler(object):

    def __init__(self, tex=None,
        batch=False, shell=False, twice=False, fully=False, keep_aux=False, clear=False,
        view=False, compile=True, bibtex=False, luatex=False,
        index=False, language='korean', komkindex=False, index_style='kotex.ist',
        bookmark_index=False, bookmark_python=False, 
        final=False, draft=False, python=False):
        
        self.tex = tex
        self.batch_bool = batch
        self.shell_bool = shell
        self.twice_bool = twice
        self.fully_bool = fully
        self.keep_aux_bool = keep_aux
        self.clear_bool = clear
        self.view_bool = view
        self.compile_bool = compile
        self.bibtex_bool = bibtex
        self.luatex_bool = luatex
        self.index_bool = index
        self.lang = language
        self.komkindex_bool = komkindex
        self.index_style = index_style
        self.bm_index_bool = bookmark_index
        self.bm_python_bool = bookmark_python
        self.final_bool = final
        self.draft_bool = draft
        self.python_bool = python

    def get_ready(self):        
        if self.luatex_bool:
            self.compiler = 'lualatex.exe'
        else:
            self.compiler = 'xelatex.exe'

        # Compile mode
        if self.batch_bool or self.fully_bool:
            self.compile_mode = '-interaction=batchmode '
        else:
            self.compile_mode = '-synctex=1 '
        if self.shell_bool:
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
        if os.path.splitext(self.index_style)[1] == '.xdy':
            self.xindy = self.index_style
        else:
            try:
                self.xindy = index_modules[self.lang[:3].lower()]
            except:
                self.xindy = index_modules['kor']

        if self.tex is not None:   
            basename = os.path.basename(self.tex)
            filename = os.path.splitext(basename)[0]
            self.tex = filename + '.tex'
            self.aux = filename + '.aux'
            self.idx = filename + '.idx'
            self.ind = filename + '.ind'
            self.pdf = filename + '.pdf'
            self.py = filename + '.pytxcode'
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
            dest = 'compile',
            action = 'store_false',
            default = True,
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
            '-L',
            dest = 'language',
            default = 'korean',
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
            '-I',
            dest = 'index_style',
            default = 'kotex.ist',
            help = 'Specify an index style for komkindex or texindy. The dafault is kotex.ist.'
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
            '-B',
            dest = 'bibtex',
            action = 'store_true',
            default = False,
            help = 'Run bibtex.'
        )
        parser.add_argument(
            '-F',
            dest = 'final',
            action = 'store_true',
            default = False,
            help = 'Find \\FinalizerOff to replace it with \\FinalizerOn in the tex file.'    
        )
        parser.add_argument(
            '-D',
            dest = 'draft',
            action = 'store_true',
            default = False,
            help = 'Find \\FinalizerON to replace it with \\FinalizerOff in the tex file.'    
        )
        parser.add_argument(
            '-P',
            dest = 'python',
            action = 'store_true',
            default = False,
            help = 'Run pythontex.exe.'    
        )

        args = parser.parse_args(argv)

        if args.tex is not None:
            self.tex = args.tex
        self.batch_bool = args.batch
        self.shell_bool = args.shell
        self.twice_bool = args.twice
        self.fully_bool = args.fully
        self.keep_aux_bool = args.keep_aux
        self.clear_bool = args.clear
        self.view_bool = args.view
        self.compile_bool = args.compile
        self.bibtex_bool = args.bibtex
        self.luatex_bool = args.luatex
        self.index_bool = args.index
        self.lang = args.language
        self.komkindex_bool = args.komkindex
        self.index_style = args.index_style
        self.bm_index_bool = args.bookmark_index
        self.bm_python_bool = args.bookmark_python
        self.final_bool = args.final
        self.draft_bool = args.draft
        self.python_bool = args.python

    def compile_once(self, cmd_tex):
        os.system(cmd_tex)
        if self.bibtex_bool:
            self.run_bibtex()
        if self.index_bool:
            self.sort_index()
        if self.python_bool:
            self.pythontex()    

    def compile_twice(self, cmd_tex):
        os.system(cmd_tex)
        if self.bibtex_bool:
            self.run_bibtex()
        if self.index_bool:
            self.sort_index()
        if self.python_bool:
            self.pythontex() 
        os.system(cmd_tex) 

    def compile_fully(self, cmd_tex):
        os.system(cmd_tex)
        if self.bibtex_bool:
            self.run_bibtex()
        if self.python_bool:
            self.pythontex()
        os.system(cmd_tex)
        self.sort_index()       
        if os.path.exists(self.ind):
            os.system(cmd_tex)
        os.system(cmd_tex)
        if not self.keep_aux_bool:
            self.clear_aux()

    def run_bibtex(self):    
        os.system('bibtex.exe %s' %(self.aux))

    def sort_index(self):
        if not os.path.exists(self.idx):
            print('%s is not found' % (self.idx))
            return
        if self.komkindex_bool:
            cmd = 'komkindex.exe -s %s %s' %(self.index_style, self.idx)
        else:
            cmd = 'texindy.exe --module %s %s' %(self.xindy, self.idx) 
        os.system(cmd)    
        if self.bm_index_bool or self.bm_python_bool:
            self.bookmark_index()

    def bookmark_index(self):
        tmp = 't@mp.ind'
        if os.path.exists(tmp):
            os.remove(tmp)
        with open(tmp, mode = 'w', encoding = 'utf-8') as new_file, open(self.ind, mode = 'r', encoding = 'utf-8') as old_file:
            if self.bm_python_bool:
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
            entry = entry.group(1).replace('\\spxentry{', '')
            page = re.findall(r'\\hyperpage\{(\d+)\}', line)
            append = ''
            for i in range(len(page)):
                append +=  '\t\\bookmark[level=2, page=%s]{%s}\n' %(page[i], entry)
            line +=  append
        return line

    def clear_aux(self):
        extensions = ("aux", "bbl", "blg", "idx", "ilg", "ind", "loe", "lof", "log", "lop", "loq", "lot", "minted*", "mw", "nav", "out", "synctex*", "snm", "toc*", "upa", "upb", "pyg.lst", "pyg.sty", "vrb", "pytxcode")
        for ext in extensions:
            fnpattern = '*.' + ext
            for afile in glob.glob(fnpattern):
                os.remove(afile)        
        for dir in glob.glob('pythontex-files-*'):        
            shutil.rmtree(dir)

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

    def pythontex(self):
        os.system('pythontex.exe --runall=true %s' %(self.py))

    def compile(self):
        self.get_ready()
        if self.tex:
            if self.final_bool:
                self.finalizer_on()
            if self.draft_bool:
                self.finalizer_off()

        if not self.compile_bool:
            if self.tex:
                if self.index_bool or self.komkindex_bool:
                    self.sort_index()
                if self.bibtex_bool:
                    self.run_bibtex()            
        else:
            if self.tex:
                cmd_tex = '%s %s "%s"' %(self.compiler, self.compile_mode, self.tex)
                if self.fully_bool:
                    self.compile_fully(cmd_tex)
                elif self.twice_bool:
                    self.compile_twice(cmd_tex)
                else:
                    self.compile_once(cmd_tex)            

        if self.clear_bool:
            self.clear_aux()  

        if self.view_bool:
            if os.path.exists(self.pdf):                 
                opener = FileOpener()
                opener.OpenPDF(self.pdf)
    
if __name__ == "__main__":
    texer = LatexCompiler()
    texer.parse_args()
    texer.compile()