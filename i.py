import os
import sys
import glob
import argparse
import configparser
from itertools import chain
import re

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from ltx import LatexCompiler


class IdleTexnician(object):

    def __init__(self):

        self.ini = 'i.ini'
        self.parse_args()

    def parse_args(self):

    #     example = '''examples:
    # i.py
    #     The first found tex file is compiled.
    # i.py foo
    #     The first file out of *foo*.tex is compiled.
    # i.py -z
    #     Select one from the list of found tex files.
    # i.py -P
    #     Select one from the list of found tex files and it will be compiled as specified by tex.conf, if available.
    #     The purpose of this option is to compile a single subfile.
    # '''

        parser = argparse.ArgumentParser(
            # epilog = example,  
            # formatter_class = argparse.RawDescriptionHelpFormatter,
            description = 'Find and compile a tex file using ltx.py. Options unknown to this script are passed to ltx.py.'
        )
        parser.add_argument(
            'tex',
            nargs = '?'
        )        
        parser.add_argument(
            '-z',
            dest = 'list_bool',
            action = 'store_true',
            default = False,
            help = 'Enumerate every tex file for choice.'
        )
        parser.add_argument(
            '-D',
            dest = 'draft_bool',
            action = 'store_true',
            default = False,
            help = 'Run the draft pre-processing option specified in the configuration file, i.ini.'
        )
        parser.add_argument(
            '-F',
            dest = 'final_bool',
            action = 'store_true',
            default = False,
            help = 'Run the final pre-processing option.'
        )
        parser.add_argument(
            '-P',
            dest = 'partial_bool',
            action = 'store_true',
            default = False,
            help = 'Wrap up the specified file in the main option.'
        )

        self.args, self.compile_option = parser.parse_known_args()

    def update_ini(self):

        conf = configparser.ConfigParser()

        if os.path.exists(self.ini):
            conf.read(self.ini)
            conf.set('tex', 'target', self.tex)
        else:
            conf['tex'] = {'target': self.tex}

        with open(self.ini, 'w') as f:
            conf.write(f)


    def run_preprocess(self):

        if not os.path.exists(self.ini):
            print('i.ini is not found.')  
            return

        conf = configparser.ConfigParser()
        conf.read(self.ini)
        
        if self.args.draft_bool:
            cmd = conf.get('tex', 'draft', fallback=False)
        else:
            cmd = conf.get('tex', 'final', fallback=False)

        if cmd:
            os.system(cmd)
        

    def run_postprocess(self):

        if not os.path.exists(self.ini):
            return

        conf = configparser.ConfigParser()
        conf.read(self.ini)
        cmd = conf.get('tex', 'after', fallback=False)
        if cmd:
            os.system(cmd)

    def write_tex(self):

        if os.path.exists(self.ini):
            conf = configparser.ConfigParser()
            conf.read(self.ini, encoding='utf-8')
            main = conf.get('tex', 'main', fallback=False)
            if main:
                main = main.replace('\\1', self.tex)
            
            with open('t@x.tex', mode='w') as f:
                f.write(main)

            basename = os.path.basename(self.tex)
            filename = os.path.splitext(basename)[0]
            self.pdf = filename + '.pdf'
            self.tex = 't@x.tex'


    def compile_tex(self):
        
        if self.args.draft_bool or self.args.final_bool:
            self.run_preprocess()
        
        if self.args.partial_bool:
            self.write_tex()

        self.compile_option.insert(0, self.tex)
        print(self.compile_option)

        texer = LatexCompiler()
        texer.parse_args(self.compile_option)
        texer.compile()

        if self.args.partial_bool:
            if os.path.exists('t@x.pdf'):
                if os.path.exists(self.pdf):
                    os.remove(self.pdf)
                os.rename('t@x.pdf', self.pdf)
        
        self.run_postprocess()


    def determine_from_list(self):

        files = []

        for i in glob.glob('*.tex'):
            files.append(i)
        
        if len(files) == 0:
            print('No tex files are found.')
            return False


        for i, v in enumerate(files):
            print('{}:{}'.format(i+1, v))
        choice = input('\nChoose a file by entering its number: ')
        try: 
            choice = int(choice) 
            return(files[choice-1])
        except:
            print('Wrong selection.')
            return False



    def get_target(self):

        if os.path.exists(self.ini):
            conf = configparser.ConfigParser()
            conf.read(self.ini)            
            self.tex = conf.get('tex', 'target', fallback=False)
            return self.tex
        else:
            return False
        

    def determine_tex(self):

        if self.args.list_bool:
            self.tex = self.determine_from_list()
            if self.tex:
                self.update_ini()
                self.compile_tex()
        else:
            self.tex = self.get_target()
            if self.tex:
                self.compile_tex()
            else:
                self.tex = self.determine_from_list()
                if self.tex:
                    self.update_ini()
                    self.compile_tex()


if __name__ == "__main__":
    idler = IdleTexnician()    
    idler.determine_tex()