import os
import sys
import glob
import argparse
import configparser
import re
import subprocess
import shutil

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from open import FileOpener

# Both below are available:
# LatexCompiler('foo.tex', [options, ...])
# LatexCompiler(['foo.tex', options, ...])

class LatexCompiler(object):

    def __init__(self, tex=None, argv=None):
        
        self.tex = tex

        ini = os.path.join(dirCalled, 'docenv.ini')
        if os.path.exists(ini):
            config = configparser.ConfigParser()
            config.read(ini)            
            self.compiler = config.get('LaTeX', 'compiler', fallback='lualatex.exe')            
        else:
            self.compiler = "lualatex.exe"

        self.parse_args(argv)
        self.compile()


    def parse_args(self, argv=None):

        example = '''examples:
    ltx.py -b -s foo.xxx
        Any filename extension is ignored.
        foo.tex is compiled in batch mode and shell commands are allowed during compilation.
    ltx.py -l foo
        lualatex is used instead of xelatex.         
    ltx.py -w -i foo
        foo.tex is compiled twice and index entries (foo.idx) are sorted by texindy in between.
    ltx.py -i -L french -n foo
        foo.idx is sorted by french without compilation.
    ltx.py -k -I foo.ist foo
        foo.idx is sorted by komkindex instead of texindy with foo.ist after a compilation.
    ltx.py -i -m foo
        foo.ind is altered so that index entries are added as bookmarks. 
        Use "-M" to bookmark ones from python docstrings.
    ltx.py -f -a foo
        If foo.idx exists, foo.tex is compiled four times and foo.idx is sorted in between.
        Otherwise, it is compiled three times. 
        Without "-a", every auxiliary file is deleted after compilation is completed. 
    ltx.py -B foo
        Bibtex runs after a compilation.
    ltx.py -p foo
        Pythontex runs after a compilation.
    ltx.py -c
        Auxiliary files are cleared.    
    '''

        parser = argparse.ArgumentParser(
            epilog = example,
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description = 'Let LuaLaTeX or XeLaTeX generate a PDF file from a TeX file.'
        )
        parser.add_argument(
            'tex',
            type = str,
            nargs = '?',
            help = 'Specify a TeX file.'
        )
        parser.add_argument(
            '-l',
            dest = 'luatex_bool',
            action = 'store_true',
            default = False,
            help = 'Use LuaLaTeX.'
        )
        parser.add_argument(
            '-x',
            dest = 'xetex_bool',
            action = 'store_true',
            default = False,
            help = 'Use XeLaTeX.'
        )
        parser.add_argument(
            '-b',
            dest = 'batch_bool',
            action = 'store_true',
            default = False,
            help = 'Do not halt even with syntax errors. (batch-mode)'
        )
        parser.add_argument(
            '-s',
            dest = 'shell_bool',
            action = 'store_true',
            default = False,
            help = 'Allow an external program to run during a XeLaTeX run. (shell-escape)'
        )
        parser.add_argument(
            '-w',
            dest = 'twice_bool',
            action = 'store_true',
            default = False,
            help = 'Compile twice.'
        )
        parser.add_argument(
            '-f',
            dest = 'fully_bool',
            action = 'store_true',
            default = False,
            help = 'Compile fully.'
        )
        parser.add_argument(
            '-v',
            dest = 'view_bool',
            action = 'store_true',
            default = False,
            help = 'Open the resulting PDF file to view.'
        )
        parser.add_argument(
            '-n',
            dest = 'compile_bool',
            action = 'store_false',
            default = True,
            help = 'Pass over compilation but do other processes such as index sorting.'
        )
        parser.add_argument(
            '-i',
            dest = 'index_bool',
            action = 'store_true',
            default = False,
            help = 'Sort index using TeXindy.'
        )
        parser.add_argument(
            '-L',
            dest = 'language',
            default = 'korean',
            help = 'Specify a language to sort index entries. For example, \"german\" or \"ger\" for German. The default is \"korean\".'
        )
        parser.add_argument(
            '-k',
            dest = 'komkindex_bool',
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
            dest = 'keep_aux_bool',
            action = 'store_true',
            default = False,
            help = 'Keep auxiliary files after a full compilation. Without this option, they are altogether deleted.'            
        )
        parser.add_argument(
            '-m',
            dest = 'bookmark_index_bool',
            action = 'store_true',
            default = False,
            help = 'Bookmark index entries. This option is available only with -f or -i options. This feature does not support komkindex.'
        )
        parser.add_argument(
            '-M',
            dest = 'bookmark_python_bool',
            action = 'store_true',
            default = False,
            help = 'Bookmark index entries which are python functions extracted from docstrings. This option is available only with -f or -i options.'
        )
        parser.add_argument(
            '-c',
            dest = 'clear_bool',
            action = 'store_true',
            default = False,
            help = 'Remove auxiliary files after compilation.'
        )
        parser.add_argument(
            '-B',
            dest = 'bibtex_bool',
            action = 'store_true',
            default = False,
            help = 'Run bibtex.'
        )
        parser.add_argument(
            '-P',
            dest = 'python_bool',
            action = 'store_true',
            default = False,
            help = 'Run pythontex.exe.'    
        )

        self.args = parser.parse_args(argv)

        if self.args.tex is not None:
            self.tex = self.args.tex


    def get_ready(self):

        if self.args.luatex_bool:
            self.compiler = 'lualatex.exe'
        if self.args.xetex_bool:
            self.compiler = 'xelatex.exe'

        # Compile mode
        if self.args.batch_bool or self.args.fully_bool:
            self.compile_mode = '-interaction=batchmode '
        else:
            self.compile_mode = '-synctex=1 '
        if self.args.shell_bool:
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
        if os.path.splitext(self.args.index_style)[1] == '.xdy':
            self.xindy = self.args.index_style
        else:
            try:
                self.xindy = index_modules[self.args.lang[:3].lower()]
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
                print('{} is not found.'.format(self.tex))
                self.tex = None


    def compile_once(self, cmd_tex):

        os.system(cmd_tex)
        if self.args.bibtex_bool:
            self.run_bibtex()
        if self.args.index_bool:
            self.sort_index()
        if self.args.python_bool:
            self.pythontex()    


    def compile_twice(self, cmd_tex):

        os.system(cmd_tex)

        if self.args.bibtex_bool:
            self.run_bibtex()
        if self.args.index_bool:
            self.sort_index()
        if self.args.python_bool:
            self.pythontex() 

        os.system(cmd_tex) 


    def compile_fully(self, cmd_tex):

        os.system(cmd_tex)
        if self.args.bibtex_bool:
            self.run_bibtex()
        if self.args.python_bool:
            self.pythontex()
        os.system(cmd_tex)
        self.sort_index()       
        if os.path.exists(self.ind):
            os.system(cmd_tex)
        os.system(cmd_tex)
        if not self.args.keep_aux_bool:
            self.clear_aux()


    def run_bibtex(self):    

        os.system('bibtex.exe {}'.format(self.aux))


    def sort_index(self):

        if not os.path.exists(self.idx):
            print('{} is not found'.format(self.idx))
            return
        if self.args.komkindex_bool:
            cmd = 'komkindex.exe -s {} {}'.format(self.args.index_style, self.idx)
        else:

            result = subprocess.check_output(['kpsewhich', 'hzguide.xdy'], stderr=subprocess.STDOUT)
            if result:
                hzxdy = str(result, 'utf-8').rstrip()
                cmd = 'texindy.exe --module {} --module {} {}'.format(hzxdy, self.xindy, self.idx)             
            else:
                cmd = 'texindy.exe --module {} {}'.format(self.xindy, self.idx)        
        os.system(cmd)    
        if self.args.bookmark_index_bool or self.args.bookmark_python_bool:
            self.bookmark_index()


    def bookmark_index(self):

        tmp = 't@mp.ind'
        if os.path.exists(tmp):
            os.remove(tmp)
        with open(tmp, mode = 'w', encoding = 'utf-8') as new_file, open(self.ind, mode = 'r', encoding = 'utf-8') as old_file:
            if self.args.bookmark_python_bool:
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
                append +=  '\t\\bookmark[level=2, page={}]{{{}}}\n'.format(page[i], entry)
            line +=  append
        return line


    def clear_aux(self):

        extensions = ("aux", "bbl", "blg", "idx", "ilg", "ind", "loe", "lof", "log", "lop", "loq", "lot", "minted*", "mw", "nav", "out", "pre", "pyg.lst", "pyg.sty", "pytxcode", "synctex*", "snm", "toc", "tmp", "upa", "upb", "vrb")
        for ext in extensions:
            fnpattern = '*.' + ext
            for afile in glob.glob(fnpattern):
                os.remove(afile)        
        for dir in glob.glob('pythontex-files-*'):        
            shutil.rmtree(dir)


    def pythontex(self):

        os.system('pythontex.exe --runall=true {}'.format(self.py))


    def compile(self):

        self.get_ready()

        if not self.args.compile_bool:
            if self.tex:
                if self.args.index_bool or self.args.komkindex_bool:
                    self.sort_index()
                if self.args.bibtex_bool:
                    self.run_bibtex()            
        else:
            if self.tex:
                cmd_tex = '{} {} "{}"'.format(self.compiler, self.compile_mode, self.tex)
                if self.args.fully_bool:
                    self.compile_fully(cmd_tex)
                elif self.args.twice_bool:
                    self.compile_twice(cmd_tex)
                else:
                    self.compile_once(cmd_tex)            

        if self.args.clear_bool:
            self.clear_aux()  

        if self.args.view_bool:
            if os.path.exists(self.pdf):                 
                opener = FileOpener()
                opener.open_pdf(self.pdf)


if __name__ == "__main__":
    LatexCompiler()