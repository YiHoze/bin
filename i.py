import os
import sys
import glob
import argparse
import configparser

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from ltx import LatexCompiler

class IdleTexnician(object):

    def __init__(self):

        self.exclude = ['colophone', '_kor', '_eng']        
        self.texer = LatexCompiler()


    def parse_args(self):

        example = '''examples:
    i.py
        The first found tex file is compiled.
    i.py foo
        The first file out of *foo*.tex is compiled.
    i.py -x
        Select one from the list of found tex files.
    i.py -z
        Select one from the list of found tex files and it will be compiled as specified by tex.conf, if available.
        The purpose of this option is to compile a single subfile.
    '''

        parser = argparse.ArgumentParser(
            epilog = example,  
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description = 'Find and compile a tex file using ltx.py. Options unknown to this script are passed to ltx.py.'
        )
        parser.add_argument(
            'tex',
            nargs = '?'
        )
        parser.add_argument(
            '-x',
            dest = 'list_bool',
            action = 'store_true',
            default = False,
            help = 'Enumerate every tex file for choice.'
        )
        parser.add_argument(
            '-z',
            dest = 'config_bool',
            action = 'store_true',
            default = False,
            help = 'Find and use tex.conf.'
        )        

        self.args, self.compile_option = parser.parse_known_args()

        if self.args.config_bool:
            if os.path.exists('tex.conf'):            
                self.conf = configparser.ConfigParser()
                self.conf.read('tex.conf', encoding='utf-8')
                self.content = self.conf.get('main', 'tex')        
            else:
                print('tex.conf is not found.')
                return False
        return True

    def is_excluded(self, tex):

        for i in self.exclude:
            if i in tex:
                return True
        return False

    def write_tex(self, tex):

        content = self.content.replace('\\1', tex)

        with open('t@x.tex', mode='w') as f:
            f.write(content)
        basename = os.path.basename(tex)
        filename = os.path.splitext(basename)[0]
        self.pdf = filename + '.pdf'
        self.tex = 't@x.tex'

    def compile_tex(self):

        targs = self.compile_option.copy()
        targs.insert(0, self.tex)
        # print(targs)

        self.texer.parse_args(targs)
        self.texer.compile()

        if self.args.config_bool:
            if os.path.exists('t@x.pdf'):
                if os.path.exists(self.pdf):
                    os.remove(self.pdf)
                os.rename('t@x.pdf', self.pdf)

    def determine_tex(self):

        if self.args.tex:
            for i in glob.glob('*'+self.args.tex+'*.tex'):
                self.tex = i
                self.compile_tex()
        else:
            if self.args.list_bool or self.args.config_bool:
                self.determine_from_list()
            else:
                for i in glob.glob("*.tex"):
                    if not self.is_excluded(i):
                        self.tex = i
                        break
                self.compile_tex()

    def determine_from_list(self):

        files = []
        for i in glob.glob('*.tex'):
            files.append(i)
        for i, v in enumerate(files):
            print('{}:{}'.format(i+1, v))
        choice = input('\nChoose a file by entering its number: ')
        if '-' in choice:
            range = choice.split('-')
            initial = range[0]
            final = range[1]
        else:
            initial = choice
            final = choice
        try: 
            initial = int(initial) 
            final = int(final) 
        except:
            print('Wrong selection.')
            return False
            
        initial -= 1
        final -= 1
        if initial >= 0 and final < len(files):
            while initial <= final:
                if self.args.config_bool:
                    self.write_tex(files[initial])
                else:
                    self.tex = files[initial]  
                self.compile_tex()
                initial += 1
        else:
            print('Wrong selection.')
            return False
        
            
            
        # if self.args.config_bool:    
        #     for i in glob.glob('t@x.*'):
        #         os.remove(i)

if __name__ == "__main__":
    idler = IdleTexnician()
    if idler.parse_args():
        idler.determine_tex()