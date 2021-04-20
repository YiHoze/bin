import os
import sys
import glob
import argparse
import configparser
import re

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from ltx import LatexCompiler
from open import FileOpener

class IdleTexnician(object):

    def __init__(self):

        self.ini = 'i.ini'
        self.ini_template = '''[tex]
target = foo.tex
compiler =
draft = wordig.py -a "..." -s "..." %(target)s
final = wordig.py -a "..." -s "..." %(target)s
final_compiler =
after =
main = \\input{preamble}
    \\begin{document}
    \\maketitle
    \\input{\\1}
    \\end{document}'''
        self.parse_args()
        self.determine_tex()


    def parse_args(self):

        about = 'i.ini should be like:\n{}'.format(self.ini_template)

        parser = argparse.ArgumentParser(
            epilog = about,
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description = 'Find and compile a tex file using ltx.py. Options unknown to this script are passed to ltx.py.'
        )
        parser.add_argument(
            'tex',
            nargs = '?'
        )
        parser.add_argument(
            '-U',
            dest = 'list_bool',
            action = 'store_true',
            default = False,
            help = 'Enumerate every tex file to select and update i.ini.'
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
            '-W',
            dest = 'wrap_bool',
            action = 'store_true',
            default = False,
            help = "Wrap up the specified file with the main option's."
        )
        parser.add_argument(
            '-N',
            dest = 'run_bool',
            action = 'store_false',
            default = True,
            help = "Don't compile only to update i.ini."
        )
        parser.add_argument(
            '-C',
            dest = 'create_ini_bool',
            action = 'store_true',
            default = False,
            help = 'Create i.ini.'
        )

        self.args, self.compile_option = parser.parse_known_args()


    def run_preprocess(self, target):

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
            if '.tex' not in cmd:
                cmd = '{} {}'.format(cmd, target)
            os.system(cmd)

        if self.args.final_bool:
            compiler = conf.get('tex', 'final_compiler', fallback=False)
            if compiler:
                compiler = compiler.split(' ')
                for i in compiler:
                    self.compile_option.append(i)


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
            fnpattern = os.path.splitext(basename)[0]
            self.pdf = fnpattern + '.pdf'
            self.tex = 't@x.tex'


    def compile_tex(self):

        if not self.args.run_bool:
            return

        if os.path.exists(self.ini):
            conf = configparser.ConfigParser()
            conf.read(self.ini)
            compiler = conf.get('tex', 'compiler', fallback=False)
            if compiler:
                compiler = compiler.split(' ')
                for i in compiler:
                    self.compile_option.append(i)

        if type(self.tex) is list:
            for i in self.tex:
                self.do_compile(i)
        else:
            self.do_compile(self.tex)


    def do_compile(self, tex):

        if self.args.draft_bool or self.args.final_bool:
            self.run_preprocess(tex)

        if self.args.wrap_bool:
            self.write_tex()

        print('{} {}'.format(tex, self.compile_option))

        LatexCompiler(tex, self.compile_option)

        if self.args.wrap_bool:
            if os.path.exists('t@x.pdf'):
                if os.path.exists(self.pdf):
                    os.remove(self.pdf)
                os.rename('t@x.pdf', self.pdf)

        self.run_postprocess()


    def update_ini(self, fnpattern):

        conf = configparser.ConfigParser()

        if os.path.exists(self.ini):
            conf.read(self.ini)
            conf.set('tex', 'target', fnpattern)
        else:
            conf['tex'] = {'target': fnpattern}

        with open(self.ini, 'w') as f:
            conf.write(f)


    def get_target(self):

        count, existing_files = self.count_tex_files()

        if count == 0:
            sys.exit()
        elif count == 1:
            return existing_files[0]
        else:
            if os.path.exists(self.ini):
                conf = configparser.ConfigParser()
                conf.read(self.ini)
                registered_files = conf.get('tex', 'target', fallback=False)
                if registered_files:
                    registered_files = registered_files.split('\n')
                    if len(registered_files) == 1:
                        return registered_files[0]
                    else:
                        return self.enumerate_list(registered_files)
                else:
                    return False
            else:
                return False


    def count_tex_files(self):

        files = []

        if self.args.tex is None:
            fnpattern = '*.tex'
        else:
            fnpattern = os.path.splitext(self.args.tex)[0]
            if not '*' in fnpattern:
                fnpattern = '*{}*'.format(fnpattern)
            fnpattern += '.tex'

        for i in glob.glob(fnpattern):
            files.append(i)

        if len(files) == 0:
            print('No tex files are found.')

        return len(files), files


    def enumerate_list(self, files):

        if self.args.tex is not None:
            tmp = files.copy()
            files.clear()
            for i in tmp:
                if self.args.tex in i:
                    files.append(i)
            if len(files) == 1:
                return files[0]

        for i, v in enumerate(files):
            print('{}:{}'.format(i+1, v))
        selection = input('\nSelect a file by entering its number, or enter "0" for all: ')

        if selection == '':
            sys.exit()
        if selection == '0':
            return files

        tmp = selection.split()
        selection = []
        for i in tmp:
            if '-' in i:
                x = i.split('-')
                try:
                    x = range(int(x[0]), int(x[1])+1)
                    for n in x:
                        selection.append(n)
                except:
                    print('Wrong selection.')
                    return False
            else:
                try:
                    selection.append(int(i))
                except:
                    print('Wrong selection.')
                    return False

        if len(selection) > 0:
            for i, v in enumerate(selection):
                selection[i] = files[v-1]
            return selection
        else:
            return False


    def determine_from_list(self):

        count, files = self.count_tex_files()

        if count == 0:
            return False
        elif count == 1:
            return files[0]

        selection = self.enumerate_list(files)
        if selection:
            self.update_ini('\n'.join(selection))
            return selection
        else:
            return False


    def create_ini(self):

        if os.path.exists(self.ini):
            answer = input('{} already exists. Are you sure to overwrite it? [y/N] '.format(self.ini))
            if answer.lower() == 'y':
                os.remove(self.ini)
            else:
                return

        with open(self.ini, mode='w', encoding='utf-8') as f:
            f.write(self.ini_template)
        opener = FileOpener()
        opener.open_txt(self.ini)

    def determine_tex(self):

        if self.args.create_ini_bool:
            self.create_ini()
        elif self.args.list_bool:
            self.tex = self.determine_from_list()
            if self.tex:
                self.compile_tex()
        else:
            self.tex = self.get_target()
            if self.tex:
                self.compile_tex()
            else:
                self.tex = self.determine_from_list()
                if self.tex:
                    self.compile_tex()


if __name__ == "__main__":
    IdleTexnician()